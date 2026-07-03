/**
 * floor_prices.js
 *
 * Scans ALL GU listings (ETH, GODS, USDC, native IMX) in one combined pass.
 * Non-ETH prices are converted to ETH wei before being stored.
 * getFloor() returns ETH price first, then falls back to GODS → IMX → USDC.
 *
 * Conversion formulas (all BigInt-safe, no float arithmetic on prices):
 *
 *   GODS / IMX  (both 18-decimal tokens):
 *     scaledRate = round(rateInEth × 1e12)
 *     ethWei     = tokenWei × scaledRate / 1_000_000_000_000n
 *
 *   USDC (6-decimal stablecoin, ~$1 each):
 *     ethUsdScaled = round(ethUsdPrice × 100)          ← 2 decimal-place precision
 *     ethWei       = usdcWei × 100_000_000_000_000n / ethUsdScaled
 *
 * Token contracts on imtbl-zkevm-mainnet (verified from live API):
 *   ETH  = 0x52a6c53869ce09a731cd772f245b97a4401d3348  (18 dec, type ERC20)
 *   GODS = 0xe0e0981d19ef2e0a57cc48ca60d9454ed2d53feb  (18 dec, type ERC20)
 *   USDC = 0x6de8acc0d406837030ce4dd28e7c08c5a96a30d2  ( 6 dec, type ERC20)
 *   IMX  = no contract address                         (18 dec, type NATIVE)
 */

const https = require('https');
const fs    = require('fs');
const path  = require('path');

// ── Constants ────────────────────────────────────────────────────────────────
// Bot owner's wallet — sourced from the .env WALLET_ADDRESS the recipient sets
// via the Wallet tab in the UI (or manually in .env for CLI users).
const WALLET        = (process.env.WALLET_ADDRESS || '').toLowerCase();

// Wallets that will never be undercut — populated at startup via
// setWhitelistedWallets() from config.json. Listings from these wallets are
// invisible to the floor calculator so partner bots don't race each other down.
// (Direct-CLI users without the GUI can also push values here at boot.)
let WHITELISTED_WALLETS = new Set();
function setWhitelistedWallets(addrs) {
  WHITELISTED_WALLETS = new Set((addrs || []).map(a => String(a).toLowerCase().trim()).filter(Boolean));
}
const GU_CONTRACT   = '0x06d92b637dfcdf95a2faba04ef22b2a096029b69';
const ETH_CONTRACT  = '0x52a6c53869ce09a731cd772f245b97a4401d3348';
const GODS_CONTRACT = '0xe0e0981d19ef2e0a57cc48ca60d9454ed2d53feb';
const USDC_CONTRACT = '0x6de8acc0d406837030ce4dd28e7c08c5a96a30d2';
// IMX is the native chain token — no contract address, identified by type:"NATIVE"
const CHAIN         = 'imtbl-zkevm-mainnet';

const PAGE_SIZE        = 200;
const SLEEP_BETWEEN_MS = 120;
const MY_LISTING_TTL   = 10 * 60 * 1000;
const CACHE_MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; // 7 days
const RATES_TTL        = 30 * 60 * 1000;           // 30 min token rate refresh

const CACHE_FILE = path.join(__dirname, 'token_proto_cache.json');

// ── State ────────────────────────────────────────────────────────────────────
let myTokenIds         = new Set();
let tokenToProto       = {};
let protoToTokens      = {};
let globalTokenToProto = {};
let protoFloorCache    = {};  // ETH listings   → ETH wei prices
let godsFloorCache     = {};  // GODS listings  → converted ETH wei prices
let usdcFloorCache     = {};  // USDC listings  → converted ETH wei prices
let imxFloorCache      = {};  // IMX native     → converted ETH wei prices
let cachedRates        = null; // { godsEth, imxEth, ethUsd } — fetched together
let cachedRatesTs      = 0;
let initialized        = false;
const myListingCache   = {};

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ── HTTP ─────────────────────────────────────────────────────────────────────
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { headers: { 'Accept': 'application/json' } }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch(e) { resolve({ status: res.statusCode, body: null }); }
      });
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

async function fetchWithRetry(url, retries = 8) {
  for (let i = 0; i < retries; i++) {
    try {
      const r = await fetchJSON(url);
      if (r.status === 429) {
        const wait = 3000 * (i + 1);
        process.stdout.write(` [429 wait ${wait}ms]`);
        await sleep(wait);
        continue;
      }
      if (!r?.body?.result && r?.status !== 404) {
        process.stdout.write(` [empty retry ${i+1}/${retries}]`);
        await sleep(2000 * (i + 1));
        continue;
      }
      return r;
    } catch(e) {
      const isLast = i === retries - 1;
      process.stdout.write(` [${e.message} retry ${i+1}/${retries}]`);
      if (isLast) {
        console.log(`\n[floor] WARNING: request failed after ${retries} retries: ${url.slice(0, 80)}...`);
        return null;
      }
      await sleep(1500 * (i + 1));
    }
  }
  return null;
}

// ── Token rates ───────────────────────────────────────────────────────────────
// Source strategy (most reliable first):
//   ETH/USD  → Binance ETHUSDT (no rate limit, always works)
//   GODS/ETH → CoinGecko direct ratio (avoids two-step USD division)
//   IMX/ETH  → CoinGecko direct ratio
//
// Stale cache: rates are kept for up to 24 h rather than disabling floors
// entirely when CoinGecko is rate-limited. Prices don't change fast enough
// for a few-hour-old rate to cause meaningful errors.
async function fetchAllRates() {
  if (cachedRates && Date.now() - cachedRatesTs < RATES_TTL) return cachedRates;

  const fresh = {};

  // ── ETH/USD via Binance (reliable, no rate limit on the free ticker) ──────
  try {
    const r = await fetchJSON('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT');
    const p = parseFloat(r?.body?.price);
    if (p > 100) fresh.ethUsd = p;
  } catch(e) {
    console.log(`[floor] Binance ETH/USD error: ${e.message}`);
  }

  // ── GODS/ETH + IMX/ETH via CoinGecko (separate call — ETH already covered) ─
  try {
    const r = await fetchJSON(
      'https://api.coingecko.com/api/v3/simple/price' +
      '?ids=gods-unchained,immutable-x&vs_currencies=eth'
    );
    // Detect CoinGecko rate-limit response (returns JSON with error_code 429)
    if (r?.status === 429 || r?.body?.status?.error_code) {
      console.log(`[floor] CoinGecko rate-limited (status ${r?.status ?? r?.body?.status?.error_code})`);
    } else {
      const ge = r?.body?.['gods-unchained']?.eth;
      const ie = r?.body?.['immutable-x']?.eth;
      if (typeof ge === 'number' && ge > 0 && ge < 1) fresh.godsEth = ge;
      if (typeof ie === 'number' && ie > 0 && ie < 1) fresh.imxEth  = ie;
    }
  } catch(e) {
    console.log(`[floor] CoinGecko error: ${e.message}`);
  }

  if (Object.keys(fresh).length > 0) {
    // Merge: keep old values for any rates we couldn't refresh this cycle
    cachedRates   = { ...cachedRates, ...fresh };
    cachedRatesTs = Date.now();
    const parts = [];
    if (fresh.ethUsd)  parts.push(`ETH=$${fresh.ethUsd}`);
    if (fresh.godsEth) parts.push(`GODS=${fresh.godsEth}ETH`);
    if (fresh.imxEth)  parts.push(`IMX=${fresh.imxEth}ETH`);
    console.log(`[floor] Rates: ${parts.join(' | ')}`);
    return cachedRates;
  }

  // Stale cache fallback — use up to 24 h old rather than disabling floors
  if (cachedRates) {
    const ageH = Math.round((Date.now() - cachedRatesTs) / 3600000);
    console.log(`[floor] Rate sources unavailable — using ${ageH}h-old cached rates`);
    return cachedRates;
  }

  console.log('[floor] No rates available — non-ETH floors disabled this cycle');
  return {};
}

// ── Disk cache ────────────────────────────────────────────────────────────────
function loadCacheFromDisk() {
  try {
    if (!fs.existsSync(CACHE_FILE)) return false;
    const raw  = fs.readFileSync(CACHE_FILE, 'utf8');
    const data = JSON.parse(raw);
    const age  = Date.now() - (data.savedAt || 0);
    if (age > CACHE_MAX_AGE_MS) {
      console.log(`[floor] Cache is ${Math.round(age / 86400000)}d old — will rebuild`);
      return false;
    }
    const tokens = data.tokens || {};
    const count  = Object.keys(tokens).length;
    if (count < 1000) {
      console.log(`[floor] Cache has only ${count} entries — too small, discarding`);
      return false;
    }
    globalTokenToProto = tokens;
    console.log(`[floor] Loaded ${count.toLocaleString()} token->proto mappings (${Math.round(age / 3600000)}h old)`);
    return true;
  } catch(e) {
    console.log(`[floor] Could not read cache: ${e.message}`);
    return false;
  }
}

function saveCacheToDisk() {
  const tmp = CACHE_FILE + '.tmp';
  try {
    const count = Object.keys(globalTokenToProto).length;
    fs.writeFileSync(tmp, JSON.stringify({ savedAt: Date.now(), tokens: globalTokenToProto }), 'utf8');
    fs.renameSync(tmp, CACHE_FILE);
    console.log(`[floor] Saved ${count.toLocaleString()} mappings to disk`);
  } catch(e) {
    console.log(`[floor] Could not save cache: ${e.message}`);
    try { fs.unlinkSync(tmp); } catch(_) {}
  }
}

// ── Step 1: Load owned NFTs ───────────────────────────────────────────────────
async function loadOwnedNfts() {
  console.log('[floor] Step 1: Loading owned NFTs...');
  let cursor = null;
  let total  = 0;

  do {
    const url = `https://api.immutable.com/v1/chains/${CHAIN}/accounts/${WALLET}/nfts` +
      `?contract_address=${GU_CONTRACT}&page_size=200` +
      (cursor ? `&page_cursor=${encodeURIComponent(cursor)}` : '');

    const r = await fetchWithRetry(url);
    if (!r?.body?.result) break;

    for (const nft of r.body.result) {
      const pa = (nft.attributes || []).find(a => a.trait_type === 'Proto');
      if (!pa) continue;
      const proto = parseInt(pa.value);
      const tid   = nft.token_id;
      myTokenIds.add(tid);
      tokenToProto[tid] = proto;
      const qa = (nft.attributes || []).find(a => a.trait_type === 'Quality');
      globalTokenToProto[tid] = { proto, quality: qa ? String(qa.value) : null };
      if (!protoToTokens[proto]) protoToTokens[proto] = new Set();
      protoToTokens[proto].add(tid);
    }

    cursor = r.body.page?.next_cursor || null;
    total += r.body.result.length;
    process.stdout.write(`\r[floor] Step 1: Loaded ${total} NFTs, ${Object.keys(protoToTokens).length} protos...`);
    if (cursor) await sleep(150);
  } while (cursor);

  console.log(`\n[floor] Owned: ${total} tokens across ${Object.keys(protoToTokens).length} protos`);
}

// ── Step 2: Scan ALL GU listings (all currencies in one pass) ────────────────
// No buy_item_contract_address filter — we handle categorisation in code.
// Returns { sellerTokens, ethListings, godsListings, usdcListings, imxListings }
async function scanAllListings() {
  console.log('[floor] Step 2: Scanning all GU listings (ETH + GODS + USDC + IMX)...');

  const sellerTokens = {};
  const ethListings  = [];
  const godsListings = [];
  const usdcListings = [];
  const imxListings  = [];

  let cursor = null;
  let pages  = 0;
  let total  = 0;

  do {
    const url =
      `https://api.immutable.com/v1/chains/${CHAIN}/orders/listings` +
      `?sell_item_contract_address=${GU_CONTRACT}` +
      `&status=ACTIVE` +
      `&page_size=${PAGE_SIZE}` +
      (cursor ? `&page_cursor=${encodeURIComponent(cursor)}` : '');

    const r = await fetchWithRetry(url, 3);
    if (!r?.body?.result) break;
    pages++;

    for (const listing of r.body.result) {
      const tokenId     = listing.sell?.[0]?.token_id;
      const buy         = listing.buy?.[0];
      const amount      = buy?.amount;
      const seller      = listing.account_address;
      if (!tokenId || !amount || !seller) continue;

      // Identify currency bucket
      const buyType     = buy?.type;
      const buyContract = (buy?.contract_address || '').toLowerCase();

      let bucket;
      if      (buyType === 'NATIVE')                       bucket = imxListings;
      else if (buyContract === ETH_CONTRACT.toLowerCase()) bucket = ethListings;
      else if (buyContract === GODS_CONTRACT.toLowerCase()) bucket = godsListings;
      else if (buyContract === USDC_CONTRACT.toLowerCase()) bucket = usdcListings;
      else continue; // unknown currency — skip

      total++;
      if (myTokenIds.has(tokenId)) continue; // skip own tokens
      if (WHITELISTED_WALLETS.has(seller.toLowerCase())) continue; // skip partner wallets

      bucket.push({ tokenId, seller, price: BigInt(amount) });

      // Track sellers whose tokens we haven't resolved yet
      if (globalTokenToProto[tokenId] === undefined) {
        if (!sellerTokens[seller]) sellerTokens[seller] = new Set();
        sellerTokens[seller].add(tokenId);
      }
    }

    cursor = r.body.page?.next_cursor || null;
    process.stdout.write(
      `\r[floor] Step 2: page ${pages}, ${total} listings ` +
      `(ETH:${ethListings.length} GODS:${godsListings.length} USDC:${usdcListings.length} IMX:${imxListings.length})...`
    );
    if (cursor) await sleep(SLEEP_BETWEEN_MS);
  } while (cursor);

  console.log(
    `\n[floor] Scan done: ${total} total | ` +
    `ETH:${ethListings.length} GODS:${godsListings.length} USDC:${usdcListings.length} IMX:${imxListings.length} | ` +
    `new sellers: ${Object.keys(sellerTokens).length}`
  );
  return { sellerTokens, ethListings, godsListings, usdcListings, imxListings };
}

// ── Step 3: Resolve unknown tokens via seller NFT lists ───────────────────────
async function resolveSellerTokens(sellerTokens) {
  const sellers = Object.keys(sellerTokens);
  if (sellers.length === 0) {
    console.log('[floor] Step 3: No new sellers — cache is fully up to date.');
    return;
  }

  console.log(`[floor] Step 3: Resolving ${sellers.length} new sellers...`);

  let concurrency   = 3;
  const MIN_CONC    = 1;
  const MAX_CONC    = 8;
  let successStreak = 0;
  let done          = 0;
  let resolved      = 0;

  async function resolveSeller(seller) {
    const wantedTokens = sellerTokens[seller];
    let cursor = null;
    let found  = 0;
    let hit429 = false;

    do {
      const url = `https://api.immutable.com/v1/chains/${CHAIN}/accounts/${seller}/nfts` +
        `?contract_address=${GU_CONTRACT}&page_size=200` +
        (cursor ? `&page_cursor=${encodeURIComponent(cursor)}` : '');

      let r;
      try { r = await fetchJSON(url); } catch(e) { break; }

      if (r.status === 429) { hit429 = true; break; }
      if (!r?.body?.result) break;

      for (const nft of r.body.result) {
        if (!wantedTokens.has(nft.token_id)) continue;
        const pa = (nft.attributes || []).find(a => a.trait_type === 'Proto');
        const qa = (nft.attributes || []).find(a => a.trait_type === 'Quality');
        if (!pa) continue;
        globalTokenToProto[nft.token_id] = { proto: parseInt(pa.value), quality: qa ? String(qa.value) : null };
        found++;
        resolved++;
      }

      cursor = r.body.page?.next_cursor || null;
      if (cursor) await sleep(80);
    } while (cursor);

    return hit429;
  }

  const queue = [...sellers];

  while (queue.length > 0) {
    const batch   = queue.splice(0, concurrency);
    const results = await Promise.all(batch.map(s => resolveSeller(s)));
    const had429  = results.some(Boolean);

    done += batch.length;
    process.stdout.write(`\r[floor] Step 3: ${done}/${sellers.length} sellers, ${resolved} tokens mapped (concurrency=${concurrency})...`);

    if (had429) {
      concurrency   = Math.max(MIN_CONC, Math.floor(concurrency / 2));
      successStreak = 0;
      await sleep(3000);
      queue.unshift(...batch);
      done -= batch.length;
    } else {
      successStreak++;
      if (successStreak >= 5 && concurrency < MAX_CONC) {
        concurrency = Math.min(MAX_CONC, concurrency + 1);
        successStreak = 0;
      }
      await sleep(150);
    }
  }

  console.log(`\n[floor] Resolved ${resolved} new tokens`);
}

// ── Price conversions (BigInt-safe, no floats touch actual prices) ────────────

// 18-decimal tokens (GODS, IMX): ethWei = tokenWei × scaledRate / 1e12
// where scaledRate = round(rateInEth × 1e12)
function convert18decToEthWei(tokenWei, rateInEth) {
  if (!rateInEth || rateInEth <= 0) return null;
  const SCALE      = 1_000_000_000_000n;
  const scaledRate = BigInt(Math.round(rateInEth * 1_000_000_000_000));
  if (scaledRate === 0n) return null;
  return tokenWei * scaledRate / SCALE;
}

// USDC (6 decimals, ~$1 each): ethWei = usdcWei × 1e14 / round(ethUsd × 100)
// Derivation: ethWei = usdcWei × 1e12 / ethUsd
//   → multiply numerator and denominator by 100 to preserve 2 decimal places
function convertUsdcToEthWei(usdcWei, ethUsd) {
  if (!ethUsd || ethUsd <= 0) return null;
  const ethUsdScaled = BigInt(Math.round(ethUsd * 100)); // e.g. 237318 for $2373.18
  if (ethUsdScaled === 0n) return null;
  return usdcWei * 100_000_000_000_000n / ethUsdScaled;
}

// ── Build floor cache (generic — same outlier logic for all currencies) ───────
// rawListings: [{ tokenId, price: BigInt }] — prices in the token's own units
// convertFn:   (price: BigInt) => BigInt|null — converts to ETH wei
// label:       string for the log line
function buildAltFloorCache(rawListings, convertFn, label) {
  if (rawListings.length === 0) {
    console.log(`[floor] ${label}: no listings`);
    return {};
  }

  // Collect token-unit prices per proto+quality
  const allPrices = {};
  let unresolved  = 0;
  let nullQuality = 0;

  for (const { tokenId, price } of rawListings) {
    const entry = globalTokenToProto[tokenId];
    if (!entry)         { unresolved++;  continue; }
    if (!entry.quality) { nullQuality++; continue; }
    const key = `${entry.proto}:${entry.quality}`;
    if (!allPrices[key]) allPrices[key] = [];
    allPrices[key].push(price);
  }

  // Same outlier filter as ETH: need 2+ listings, next must be within 3×
  const newCache = {};
  let filtered = 0;

  for (const [key, prices] of Object.entries(allPrices)) {
    prices.sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    if (prices.length === 1) continue; // single listing — outlier risk

    let floorToken = null;
    for (let i = 0; i < prices.length; i++) {
      const next = prices[i + 1];
      if (!next) { if (floorToken === null) floorToken = prices[i]; break; }
      if (next <= prices[i] * 3n) { floorToken = prices[i]; break; }
      filtered++;
    }

    if (floorToken !== null) {
      const ethWei = convertFn(floorToken);
      if (ethWei !== null && ethWei > 0n) {
        newCache[key] = { price: ethWei, ts: Date.now() };
      }
    }
  }

  console.log(`[floor] ${label} floor cache: ${Object.keys(newCache).length} combos | unresolved: ${unresolved} | outliers: ${filtered}`);
  return newCache;
}

// ── Build ETH floor cache ────────────────────────────────────────────────────
function buildFloorCache(rawListings) {
  const allPrices = {};
  let unresolved  = 0;
  let nullQuality = 0;

  for (const { tokenId, price } of rawListings) {
    const entry = globalTokenToProto[tokenId];
    if (!entry)         { unresolved++;  continue; }
    if (!entry.quality) { nullQuality++; continue; }
    const key = `${entry.proto}:${entry.quality}`;
    if (!allPrices[key]) allPrices[key] = [];
    allPrices[key].push(price);
  }

  const newCache = {};
  let filtered = 0;

  for (const [key, prices] of Object.entries(allPrices)) {
    prices.sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    if (prices.length === 1) continue;

    let floor = null;
    for (let i = 0; i < prices.length; i++) {
      const next = prices[i + 1];
      if (!next) { if (floor === null) floor = prices[i]; break; }
      if (next <= prices[i] * 3n) { floor = prices[i]; break; }
      filtered++;
    }

    if (floor !== null) {
      newCache[key] = { price: floor, ts: Date.now() };
    }
  }

  protoFloorCache = newCache;
  console.log(`[floor] ETH floor cache: ${Object.keys(newCache).length} combos | unresolved: ${unresolved} | null quality: ${nullQuality} | outliers: ${filtered}`);
}

// ── Build all non-ETH floor caches ────────────────────────────────────────────
function buildAltFloorCaches(godsListings, usdcListings, imxListings, rates) {
  const { godsEth, imxEth, ethUsd } = rates;

  godsFloorCache = godsEth
    ? buildAltFloorCache(godsListings, p => convert18decToEthWei(p, godsEth), 'GODS')
    : (godsListings.length > 0 ? (console.log('[floor] GODS: rate unavailable — skipped'), {}) : {});

  imxFloorCache = imxEth
    ? buildAltFloorCache(imxListings, p => convert18decToEthWei(p, imxEth), 'IMX')
    : (imxListings.length > 0 ? (console.log('[floor] IMX: rate unavailable — skipped'), {}) : {});

  usdcFloorCache = ethUsd
    ? buildAltFloorCache(usdcListings, p => convertUsdcToEthWei(p, ethUsd), 'USDC')
    : (usdcListings.length > 0 ? (console.log('[floor] USDC: ETH rate unavailable — skipped'), {}) : {});
}

// ── Public: init ──────────────────────────────────────────────────────────────
async function init() {
  if (initialized) return;

  await loadOwnedNfts();

  const cacheLoaded = loadCacheFromDisk();
  if (!cacheLoaded) {
    console.log('[floor] No disk cache — full seller resolution on first run (one-time)...');
  }

  const rates = await fetchAllRates();
  const { sellerTokens, ethListings, godsListings, usdcListings, imxListings } = await scanAllListings();
  await resolveSellerTokens(sellerTokens);
  saveCacheToDisk();

  buildFloorCache(ethListings);
  buildAltFloorCaches(godsListings, usdcListings, imxListings, rates);

  initialized = true;
  console.log('[floor] Init complete — floor lookups are now instant.');
}

// ── Public: refreshFloorCache ─────────────────────────────────────────────────
async function refreshFloorCache() {
  console.log('[floor] Refreshing floor cache...');

  const rates = await fetchAllRates();
  const { sellerTokens, ethListings, godsListings, usdcListings, imxListings } = await scanAllListings();
  await resolveSellerTokens(sellerTokens);

  if (Object.keys(sellerTokens).length > 0) {
    saveCacheToDisk();
  }

  buildFloorCache(ethListings);
  buildAltFloorCaches(godsListings, usdcListings, imxListings, rates);
}

// ── Public: getFloor ──────────────────────────────────────────────────────────
// Returns the cheapest competitor floor as ETH wei.
// Priority: ETH listing > GODS-derived > IMX-derived > USDC-derived.
// All non-ETH values have already been converted to ETH wei.
function getFloor(proto, quality) {
  const key = `${proto}:${quality}`;
  return (protoFloorCache[key] || godsFloorCache[key] || imxFloorCache[key] || usdcFloorCache[key])?.price ?? null;
}

// ── Public: getMyListings ─────────────────────────────────────────────────────
async function getMyListings(proto) {
  const cached = myListingCache[proto];
  if (cached && Date.now() - cached.ts < MY_LISTING_TTL) return cached.listings;

  const tokenIds = Array.from(protoToTokens[proto] || []);
  if (tokenIds.length === 0) return [];

  const listings = [];
  const BATCH    = 20;

  for (let i = 0; i < tokenIds.length; i += BATCH) {
    const batch  = tokenIds.slice(i, i + BATCH);
    const params = batch.map(t => `sell_item_token_id[]=${t}`).join('&');
    const url    =
      `https://api.immutable.com/v1/chains/${CHAIN}/orders/listings` +
      `?sell_item_contract_address=${GU_CONTRACT}` +
      `&${params}` +
      `&status=ACTIVE` +
      `&buy_item_contract_address=${ETH_CONTRACT}` +
      `&order_by=buy_item_amount&direction=asc` +
      `&page_size=50`;

    const r = await fetchWithRetry(url);
    if (!r?.body?.result) continue;

    for (const listing of r.body.result) {
      const tokenId   = listing.sell?.[0]?.token_id;
      const amount    = listing.buy?.[0]?.amount;
      const listingId = listing.id;
      if (tokenId && amount && myTokenIds.has(tokenId)) {
        listings.push({ token_id: tokenId, listing_id: listingId, price: BigInt(amount) });
      }
    }
    if (i + BATCH < tokenIds.length) await sleep(100);
  }

  listings.sort((a, b) => (a.price < b.price ? -1 : a.price > b.price ? 1 : 0));
  myListingCache[proto] = { listings, ts: Date.now() };
  return listings;
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function weiToEth(wei) {
  if (!wei) return null;
  return Number(wei * 1000000n / BigInt('1000000000000000000')) / 1000000;
}

function invalidateMyListings(proto)          { delete myListingCache[proto]; }
function globalTokenToProtoEntry(tokenId)     { return globalTokenToProto[tokenId] || null; }
function invalidateAllMyListings()            { Object.keys(myListingCache).forEach(k => delete myListingCache[k]); }
function getOwnedProtos()                     { return Object.keys(protoToTokens).map(Number); }
function getMyTokenIds(proto)                 { return Array.from(protoToTokens[proto] || []); }

module.exports = {
  init,
  refreshFloorCache,
  getFloor,
  getMyListings,
  weiToEth,
  invalidateMyListings,
  globalTokenToProtoEntry,
  invalidateAllMyListings,
  getOwnedProtos,
  getMyTokenIds,
  setWhitelistedWallets,
};

// ── Standalone test ────────────────────────────────────────────────────────────
if (require.main === module) {
  (async () => {
    const start = Date.now();
    await init();
    console.log(`\n[test] Init took ${((Date.now() - start) / 1000).toFixed(1)}s\n`);

    const protos = getOwnedProtos().slice(0, 20);
    console.log(`[test] Checking floor for ${protos.length} protos...\n`);

    let found = 0;
    for (const proto of protos) {
      const myListings = await getMyListings(proto);
      const myCheapest = myListings[0]?.price ?? null;
      const floor      = getFloor(proto, 'Meteorite');
      if (!floor && !myCheapest) continue;
      found++;
      console.log(`Proto ${proto}:`);
      console.log(`  My cheapest : ${myCheapest ? weiToEth(myCheapest) + ' ETH' : 'not listed'}`);
      console.log(`  Floor       : ${floor ? weiToEth(floor) + ' ETH' : 'no competitor'}`);
      if (floor && myCheapest) {
        const pct = Number(floor * 10000n / myCheapest) / 100;
        console.log(`  Floor/mine  : ${pct.toFixed(1)}%`);
      }
      console.log();
    }
    if (found === 0) console.log('[test] None of the first 20 protos have listings');
  })();
}
