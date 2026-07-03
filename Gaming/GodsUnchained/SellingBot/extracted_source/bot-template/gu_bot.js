/**
 * Gods Unchained Floor Bot v3
 * Lists and re-lists GU cards at 0.5% below floor price
 *
 * Setup:
 *   1. npm install @imtbl/sdk ethers dotenv
 *   2. Fill in .env file (PRIVATE_KEY, WALLET_ADDRESS)
 *   3. node gu_bot.js
 *
 * Floor price strategy:
 *   - Owned NFT map (token_id -> proto) is built once at startup
 *   - For each proto, fetch your cheapest listing price via token_id[] filter
 *   - Scan global listings cheapest-first; skip your tokens; stop when price
 *     exceeds yours * 1.15; first unknown-owner listing of matching proto = floor
 *   - If no competitor found below your price ceiling -> you are the floor
 *   - Results cached 10 min per proto
 */

require('dotenv').config();
const { orderbook, config } = require('@imtbl/sdk');
const { ethers } = require('ethers');
const https = require('https');
const fs    = require('fs');
const path  = require('path');
const floorPrices = require('./floor_prices');

// ─── FIXED CHAIN CONSTANTS ─────────────────────────────────────────────────
const GU_CONTRACT      = '0x06d92b637dfcdf95a2faba04ef22b2a096029b69';
const CHAIN            = 'imtbl-zkevm-mainnet';
const ETH_ADDRESS      = '0x52a6c53869ce09a731cd772f245b97a4401d3348';
const PRICE_UNDERCUT   = 0.005;     // kept for reference, not used — we undercut by 1 wei

// ─── USER CONFIG (loaded from config.json next to this file) ───────────────
const DEFAULT_CONFIG = {
  relistThreshold: 0.01,       // only relist if new price moves >1% from current
  maxUndercutRelists: 3,       // cap downward (got-undercut) relists per cycle
  minFloorRatio: 0.90,         // skip listing if floor < 90% of avg sale price
  scanIntervalMs: 24 * 60 * 60 * 1000,   // full cycle (all sets)
  fastIntervalMs: 30 * 60 * 1000,        // fast cycle (only fastSets)
  fastSets: ['plague'],
  allowedQualities: ['Meteorite', 'Shadow', 'Gold', 'Diamond'],
  allowedSets: ['core', 'genesis', 'tides', 'dread', 'mortal', 'order', 'trial', 'wolf', 'roots', 'fallen', 'tower', 'guardians', 'wander', 'verdict', 'welcome', 'revival', 'promo', 'ascent', 'etherbots', 'spoils', 'plague'],
  requestDelay: 500,
  avgCacheTtlMs: 60 * 60 * 1000,
  useShineMultiplier: true,    // when no market floor, derive from Meteorite × 5/25/125
  whitelistedWallets: [],      // partner-bot wallets whose listings the floor calc ignores
  usePastSalesGuard: false,    // skip listing if last-N-sales avg is below the current lowest ask
  pastSalesGuardN: 5,          // sample size for the above guard
  aggressiveUndercut: false,   // always undercut market ask, ignore dump-protection
  undercutFloorPct: 90,        // safety floor: won't undercut below this % of last-N-sales avg
  undercutSalesN: 5,           // sample size for the safety floor
};

function loadConfig() {
  const cfgPath = path.join(__dirname, 'config.json');
  try {
    if (fs.existsSync(cfgPath)) {
      const user = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
      return { ...DEFAULT_CONFIG, ...user };
    }
  } catch (e) {
    console.error(`[config] failed to load config.json: ${e.message} — using defaults`);
  }
  return { ...DEFAULT_CONFIG };
}
const USER_CFG = loadConfig();
const RELIST_THRESHOLD     = USER_CFG.relistThreshold;
const MAX_UNDERCUT_RELISTS = USER_CFG.maxUndercutRelists;
const MIN_FLOOR_RATIO      = USER_CFG.minFloorRatio;
const SCAN_INTERVAL        = USER_CFG.scanIntervalMs;
const FAST_INTERVAL        = USER_CFG.fastIntervalMs;
const FAST_SETS            = new Set(USER_CFG.fastSets);
const ALLOWED_QUALITIES    = new Set(USER_CFG.allowedQualities);
const ALLOWED_SETS         = new Set(USER_CFG.allowedSets);
const REQUEST_DELAY        = USER_CFG.requestDelay;
const AVG_CACHE_TTL        = USER_CFG.avgCacheTtlMs;
const USE_SHINE_MULTIPLIER = USER_CFG.useShineMultiplier !== false; // default true
const USE_PAST_SALES_GUARD = USER_CFG.usePastSalesGuard === true;
const PAST_SALES_GUARD_N   = Math.max(1, parseInt(USER_CFG.pastSalesGuardN, 10) || 5);
const AGGRESSIVE_UNDERCUT  = USER_CFG.aggressiveUndercut === true;
const UNDERCUT_FLOOR_PCT   = Math.max(0, Math.min(100, parseInt(USER_CFG.undercutFloorPct, 10) || 90));
const UNDERCUT_SALES_N     = Math.max(1, parseInt(USER_CFG.undercutSalesN, 10) || 5);
const BATCH_SIZE           = 10;

// Push the whitelist into floor_prices BEFORE init() runs.
floorPrices.setWhitelistedWallets(USER_CFG.whitelistedWallets || []);

// Forge-cost multipliers — used as a fallback floor for shines that have no
// market data yet. 5 Meteorites → 1 Shadow, 5 Shadows → 1 Gold, 5 Golds → 1 Diamond.
const SHINE_MULT = { Meteorite: 1n, Shadow: 5n, Gold: 25n, Diamond: 125n };

const WALLET_ADDRESS  = (process.env.WALLET_ADDRESS || '').toLowerCase();
const PRIVATE_KEY     = process.env.PRIVATE_KEY;
const PUBLISHABLE_KEY = process.env.PUBLISHABLE_KEY || 'publishable_imapct_4cFGq7Lsyb9Xu1nLZ6NSMH5oY22P9Gt5';

// ─── LOGGING ───────────────────────────────────────────────────────────────
// 'w' = truncate on every startup so the log can't grow unbounded across restarts
const logFile = fs.createWriteStream(path.join(__dirname, 'bot.log'), { flags: 'w' });
function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
  logFile.write(line + '\n');
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// ─── ANSI COLORS ───────────────────────────────────────────────────────────
const BLUE  = '[34m';
const RESET = '[0m';

const QUALITY_COLOR = {
  Meteorite: '[31m',   // red
  Shadow:    '[35m',   // purple
  Gold:      '[33m',   // yellow
  Diamond:   '[96m',   // light blue
};
function qc(quality) { return QUALITY_COLOR[quality] || ''; }

// ─── ETH/USD PRICE ────────────────────────────────────────────────────────
let ethUsd = null;
let ethUsdTs = 0;
const ETH_USD_TTL = 5 * 60 * 1000; // refresh every 5 min

async function getEthUsd() {
  if (ethUsd && Date.now() - ethUsdTs < ETH_USD_TTL) return ethUsd;
  try {
    // Binance public API — reliable, no auth needed
    const r = await new Promise((resolve) => {
      const req = https.get(
        'https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT',
        { headers: { 'Accept': 'application/json' } },
        res => {
          let d = '';
          res.on('data', c => d += c);
          res.on('end', () => { try { resolve(JSON.parse(d)); } catch(e) { resolve(null); } });
        }
      );
      req.on('error', () => resolve(null));
      req.setTimeout(5000, () => { req.destroy(); resolve(null); });
    });
    if (r?.price) { ethUsd = parseFloat(r.price); ethUsdTs = Date.now(); }
  } catch(e) {}
  return ethUsd;
}

function ethToUsd(wei, usdPrice) {
  if (!usdPrice) return '?.?????';
  const eth = Number(wei) / 1e18;
  return (eth * usdPrice).toFixed(5);
}

// ─── CARD METADATA CACHE ─────────────────────────────────────────────────
// Stores { name, rarity, type } per proto from GU game API
const cardMetaCache = {};

// Rarity-based minimum prices in ETH wei — prevents listing way below rarity value
// These are conservative floors; real floors will usually be higher
const RARITY_MIN_PRICE = {
  common:    1000n,           // 0.000000001 ETH — basically no floor for commons
  rare:      1000n,           // same
  epic:      1000n,           // same
  legendary: 500000000000n,   // 0.0005 ETH min for legendaries (~$1)
  mythic:    2000000000000n,  // 0.002 ETH min for mythics (~$4)
};



async function getCardMeta(proto) {
  if (cardMetaCache[proto]) return cardMetaCache[proto];
  try {
    const r = await new Promise((resolve) => {
      const req = https.get(
        `https://api.godsunchained.com/v0/proto/${proto}`,
        { headers: { 'Accept': 'application/json' } },
        res => {
          let d = '';
          res.on('data', c => d += c);
          res.on('end', () => { try { resolve(JSON.parse(d)); } catch(e) { resolve(null); } });
        }
      );
      req.on('error', () => resolve(null));
      req.setTimeout(5000, () => { req.destroy(); resolve(null); });
    });

    // If API returns nothing or proto doesn't exist, mark as invalid
    if (!r || (!r.name && !r.id)) {
      cardMetaCache[proto] = null;
      return null;
    }

    const meta = {
      name:   r.name   || `proto:${proto}`,
      rarity: (r.rarity || 'common').toLowerCase(),
      type:   r.type   || 'unknown',
    };
    cardMetaCache[proto] = meta;
    return meta;
  } catch(e) {
    return null;
  }
}

async function getCardName(proto) {
  const meta = await getCardMeta(proto);
  return meta?.name || `proto:${proto}`;
}

// Validate a target price against GU game API metadata
// Returns { valid: bool, reason: string }
async function validatePrice(proto, targetPrice) {
  const meta = await getCardMeta(proto);

  // Proto doesn't exist in GU game API — likely a bad mapping
  if (!meta) {
    return { valid: false, reason: `proto ${proto} not found in GU API` };
  }

  const rarity = meta.rarity;

  // Check against rarity min price
  const minPrice = RARITY_MIN_PRICE[rarity] || RARITY_MIN_PRICE.common;
  if (targetPrice < minPrice) {
    return { valid: false, reason: `${ethers.formatEther(targetPrice)} ETH below min for ${rarity} (${ethers.formatEther(minPrice)} ETH)` };
  }

  return { valid: true, reason: '' };
}

// ─── IMX SETUP ─────────────────────────────────────────────────────────────
let orderbookClient;
let wallet;

async function setup() {
  const provider = new ethers.JsonRpcProvider('https://rpc.immutable.com');
  wallet = new ethers.Wallet(PRIVATE_KEY, provider);

  orderbookClient = new orderbook.Orderbook({
    baseConfig: {
      environment: config.Environment.PRODUCTION,
      publishableKey: PUBLISHABLE_KEY,
    },
  });

  log(`Bot started. Wallet: ${WALLET_ADDRESS}`);
}

// ─── HTTP (native https — no fetch dependency issues) ─────────────────────
function httpsGet(url) {
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
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('HTTP Timeout')); });
  });
}

async function apiFetch(url, retries = 4) {
  for (let i = 0; i < retries; i++) {
    try {
      const r = await httpsGet(url);
      if (r.status === 429) {
        log(`  Rate limited, waiting ${(i + 1) * 3}s...`);
        await sleep((i + 1) * 3000);
        continue;
      }
      return r;
    } catch(e) {
      if (i === retries - 1) throw e;
      await sleep(1000 * (i + 1));
    }
  }
}

// ─── OWNED NFT MAP (built once at startup, reused every cycle) ────────────
let myTokenIds    = new Set();    // all token_ids you own
let tokenToProto  = {};           // token_id -> proto (string)
let protoToTokens = {};           // proto -> Set<token_id>
let ownedMapReady = false;

async function buildOwnedMap() {
  log('Building owned token map...');
  myTokenIds    = new Set();
  tokenToProto  = {};
  protoToTokens = {};

  let cursor = null;
  let total  = 0;

  do {
    const url = `https://api.immutable.com/v1/chains/${CHAIN}/accounts/${WALLET_ADDRESS}/nfts`
      + `?contract_address=${GU_CONTRACT}&page_size=200`
      + (cursor ? `&page_cursor=${cursor}` : '');

    const r = await apiFetch(url);
    if (!r?.body?.result) break;

    for (const nft of r.body.result) {
      const attrs = nft.attributes || [];
      const pa    = attrs.find(a => a.trait_type === 'Proto');
      if (!pa) continue;
      const proto = String(pa.value);
      const tid   = nft.token_id;
      myTokenIds.add(tid);
      tokenToProto[tid] = proto;
      if (!protoToTokens[proto]) protoToTokens[proto] = new Set();
      protoToTokens[proto].add(tid);
    }

    cursor = r.body.page?.next_cursor || null;
    total += r.body.result.length;
    if (total % 2000 === 0) log(`  Loaded ${total} NFTs...`);
    if (cursor) await sleep(150);
  } while (cursor);

  ownedMapReady = true;
  log(`Owned map ready: ${total} tokens, ${Object.keys(protoToTokens).length} unique protos`);
}

// ─── FETCH OWNED NFTS (full list with attributes, for the main cycle) ──────
async function fetchOwnedNFTs() {
  // Re-use the owned map data we already have — rebuild it fresh each cycle
  await buildOwnedMap();

  // Return nft-like objects with token_id and attributes for getProtoQuality()
  // We already have everything we need from the map; reconstruct minimal objects
  const nfts = [];
  for (const [tid, proto] of Object.entries(tokenToProto)) {
    nfts.push({
      token_id: tid,
      attributes: [
        { trait_type: 'Proto', value: proto },
        { trait_type: 'Quality', value: 'Meteorite' }, // default; updated below
      ],
      _proto: proto,
    });
  }
  return nfts;
}

// ─── FETCH OWNED NFTS WITH FULL ATTRIBUTES ────────────────────────────────
// Needed for quality info. We fetch fresh from API.
async function fetchOwnedNFTsFull() {
  log('Fetching owned NFTs...');
  const nfts = [];
  let cursor = null;

  do {
    const url = `https://api.immutable.com/v1/chains/${CHAIN}/accounts/${WALLET_ADDRESS}/nfts`
      + `?contract_address=${GU_CONTRACT}&page_size=200`
      + (cursor ? `&page_cursor=${cursor}` : '');

    const r = await apiFetch(url);
    if (!r?.body?.result) break;
    nfts.push(...r.body.result);
    cursor = r.body.page?.next_cursor || null;
    await sleep(150);
  } while (cursor);

  log(`Found ${nfts.length} owned NFTs`);
  return nfts;
}

// ─── FETCH MY ACTIVE LISTINGS ──────────────────────────────────────────────
async function fetchMyListings() {
  log('Fetching my active listings...');
  const listings = {};
  let cursor = null;

  do {
    const url = `https://api.immutable.com/v1/chains/${CHAIN}/orders/listings`
      + `?sell_item_contract_address=${GU_CONTRACT}`
      + `&account_address=${WALLET_ADDRESS}`
      + `&status=ACTIVE&page_size=200`
      + (cursor ? `&page_cursor=${cursor}` : '');

    const r = await apiFetch(url);
    if (!r?.body?.result) break;

    for (const listing of r.body.result) {
      const sell    = Array.isArray(listing.sell) ? listing.sell[0] : listing.sell;
      const tokenId = sell?.token_id;
      if (!tokenId) continue;
      const buy = Array.isArray(listing.buy) ? listing.buy[0] : listing.buy;
      // Only track ETH listings — ignore GODS/USDC/IMX listings
      if (buy?.contract_address?.toLowerCase() !== ETH_ADDRESS.toLowerCase()) continue;
      listings[tokenId] = {
        ...listing,
        _tokenId:    tokenId,
        _buyAmount:  buy?.amount,
        _buyContract: buy?.contract_address,
      };
    }

    cursor = r.body.page?.next_cursor || null;
    await sleep(REQUEST_DELAY);
  } while (cursor);

  log(`Found ${Object.keys(listings).length} active listings`);
  return listings;
}

// ─── FLOOR PRICE CACHE ────────────────────────────────────────────────────
const avgCache       = {};  // proto -> { price: BigInt|null, ts }

// ─── SALES TRACKING ────────────────────────────────────────────────────────
// Tracks active listing token_ids from previous cycle to detect sold cards
let prevListedTokenIds = null; // null = first cycle, no comparison yet

// ─── FLOOR PRICE — delegated to floor_prices.js ───────────────────────────
// floor_prices.init() is called at startup and builds a session-wide cache.
// getFloor() is then instant for the rest of the session.
// refreshFloorCache() re-scans listings each cycle to update prices.

async function fetchFloorPrice(proto, quality) {
  return floorPrices.getFloor(proto, quality);
}

// ─── FETCH AVG OF 3 CHEAPEST LISTINGS (fallback when no sales history) ────
const top3Cache = {}; // proto:quality -> { price, ts }
const TOP3_TTL  = 10 * 60 * 1000; // 10 min cache

async function fetchTop3Avg(proto, quality) {
  const cacheKey = `${proto}:${quality}`;
  const cached   = top3Cache[cacheKey];
  if (cached && Date.now() - cached.ts < TOP3_TTL) return cached.price;

  try {
    // Get all listings for tokens of this proto+quality from the floor cache
    // We already have rawListings sorted cheapest-first in protoFloorCache
    // Use getMyListings equivalent but for competitors — scan global listings
    // filtered to this proto+quality using our token cache
    const url = `https://api.immutable.com/v1/chains/${CHAIN}/orders/listings`
      + `?sell_item_contract_address=${GU_CONTRACT}`
      + `&status=ACTIVE`
      + `&buy_item_contract_address=${ETH_ADDRESS}`
      + `&order_by=buy_item_amount&direction=asc`
      + `&page_size=200`;

    const r = await apiFetch(url);
    if (!r?.body?.result) { top3Cache[cacheKey] = { price: null, ts: Date.now() }; return null; }

    // Filter to matching proto+quality, exclude our own listings
    const listings = r.body.result.filter(l => {
      if (l.account_address?.toLowerCase() === WALLET_ADDRESS) return false;
      const tokenId = l.sell?.[0]?.token_id;
      if (!tokenId) return false;
      const entry = floorPrices.globalTokenToProtoEntry(tokenId);
      if (!entry) return false;
      return entry.proto === parseInt(proto) && entry.quality === quality;
    }).slice(0, 3);

    if (!listings.length) { top3Cache[cacheKey] = { price: null, ts: Date.now() }; return null; }

    const prices = listings
      .map(l => BigInt(l.buy?.[0]?.amount ?? '0'))
      .filter(p => p > 0n);

    if (!prices.length) { top3Cache[cacheKey] = { price: null, ts: Date.now() }; return null; }

    const avg = prices.reduce((a, b) => a + b, 0n) / BigInt(prices.length);
    top3Cache[cacheKey] = { price: avg, ts: Date.now() };
    return avg;
  } catch(e) {
    top3Cache[cacheKey] = { price: null, ts: Date.now() };
    return null;
  }
}

// ─── FETCH AVG OF LAST 10 SALES (per proto+quality, ETH only) ────────────
async function fetch30DayAvg(proto, quality) {
  const cacheKey = `${proto}:${quality}`;
  const cached   = avgCache[cacheKey];
  if (cached && Date.now() - cached.ts < AVG_CACHE_TTL) return cached.price;

  try {
    // Fetch last 50 filled ETH listings for this contract globally
    // then filter to matching proto+quality, excluding our own sales
    const url = `https://api.immutable.com/v1/chains/${CHAIN}/orders/listings`
      + `?sell_item_contract_address=${GU_CONTRACT}`
      + `&status=FILLED`
      + `&buy_item_contract_address=${ETH_ADDRESS}`
      + `&page_size=50`;

    const r = await apiFetch(url);
    if (!r?.body?.result) { avgCache[cacheKey] = { price: null, ts: Date.now() }; return null; }

    const sales = r.body.result.filter(l => {
      // Exclude our own sales — we don't want our bot's cheap listings skewing the avg
      if (l.account_address?.toLowerCase() === WALLET_ADDRESS) return false;
      const tokenId = l.sell?.[0]?.token_id;
      if (!tokenId) return false;
      // Match by proto+quality using globalTokenToProto cache
      const entry = floorPrices.globalTokenToProtoEntry(tokenId);
      if (!entry) return false;
      return entry.proto === parseInt(proto) && entry.quality === quality;
    }).slice(0, 50);

    if (!sales.length) { avgCache[cacheKey] = { price: null, ts: Date.now() }; return null; }

    const prices = sales
      .map(l => BigInt(l.buy?.[0]?.amount ?? '0'))
      .filter(p => p > 0n);

    if (!prices.length) { avgCache[cacheKey] = { price: null, ts: Date.now() }; return null; }

    // Use median instead of mean to reduce impact of outliers
    prices.sort((a, b) => (a < b ? -1 : a > b ? 1 : 0));
    const median = prices[Math.floor(prices.length / 2)];
    avgCache[cacheKey] = { price: median, ts: Date.now() };
    return median;
  } catch(e) {
    avgCache[`${proto}:${quality}`] = { price: null, ts: Date.now() };
    return null;
  }
}

// ─── FETCH MEAN OF LAST N SALES (per proto+quality, newest-first, ETH only) ───
// Unlike fetch30DayAvg (median across last 50), this preserves chronological
// order, takes the N most recent matching sales, and returns their mean.
// Used by the "recent-sales guard" — see USE_PAST_SALES_GUARD.
const lastNCache = {};
async function fetchLastNSalesAvg(proto, quality, n) {
  const cacheKey = `${proto}:${quality}:n${n}`;
  const cached = lastNCache[cacheKey];
  if (cached && Date.now() - cached.ts < AVG_CACHE_TTL) return cached.price;

  try {
    const url = `https://api.immutable.com/v1/chains/${CHAIN}/orders/listings`
      + `?sell_item_contract_address=${GU_CONTRACT}`
      + `&status=FILLED`
      + `&buy_item_contract_address=${ETH_ADDRESS}`
      + `&sort_by=updated_at&sort_direction=desc`
      + `&page_size=50`;

    const r = await apiFetch(url);
    if (!r?.body?.result) { lastNCache[cacheKey] = { price: null, ts: Date.now() }; return null; }

    // Filter chronologically (API returns newest-first), take newest N matches
    const prices = r.body.result.filter(l => {
      if (l.account_address?.toLowerCase() === WALLET_ADDRESS) return false;
      const tokenId = l.sell?.[0]?.token_id;
      if (!tokenId) return false;
      const entry = floorPrices.globalTokenToProtoEntry(tokenId);
      if (!entry) return false;
      return entry.proto === parseInt(proto) && entry.quality === quality;
    })
    .slice(0, n)
    .map(l => BigInt(l.buy?.[0]?.amount ?? '0'))
    .filter(p => p > 0n);

    if (!prices.length) { lastNCache[cacheKey] = { price: null, ts: Date.now() }; return null; }
    const mean = prices.reduce((a, b) => a + b, 0n) / BigInt(prices.length);
    lastNCache[cacheKey] = { price: mean, ts: Date.now() };
    return mean;
  } catch(e) {
    lastNCache[cacheKey] = { price: null, ts: Date.now() };
    return null;
  }
}

// ─── GET PROTO AND QUALITY FROM NFT ───────────────────────────────────────
function getProtoQuality(nft) {
  try {
    const attrs = nft.attributes || nft.metadata?.attributes || [];
    let proto = null, quality = null, set = null;
    for (const a of attrs) {
      const trait = (a.trait_type || a.name || '').toLowerCase();
      if (trait === 'proto')   proto   = String(a.value);
      if (trait === 'quality') quality = String(a.value);
      if (trait === 'set')     set     = String(a.value).toLowerCase();
    }
    return { proto, quality, set };
  } catch(e) {
    return { proto: null, quality: null, set: null };
  }
}

// ─── PREPARE + SIGN ONE LISTING (no submit yet) ────────────────────────────
// Returns { tokenId, orderComponents, orderHash, orderSignature } or null.
async function prepareOneListing(tokenId, priceWei) {
  try {
    const prepareResponse = await orderbookClient.prepareListing({
      makerAddress: WALLET_ADDRESS,
      buy: {
        amount: priceWei.toString(),
        type: 'ERC20',
        contractAddress: ETH_ADDRESS,
      },
      sell: {
        contractAddress: GU_CONTRACT,
        tokenId: String(tokenId),
        type: 'ERC721',
      },
      orderExpiry: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
    });

    let orderComponents, orderHash, orderSignature;

    for (const action of prepareResponse.actions) {
      if (action.type === 'TRANSACTION' || action.type === orderbook.ActionType.TRANSACTION) {
        const tx      = await action.buildTransaction();
        const receipt = await wallet.sendTransaction(tx);
        await receipt.wait();
        log(`  Approval tx confirmed for token ${tokenId}`);
      } else if (action.type === 'SIGNABLE' || action.type === orderbook.ActionType.SIGNABLE) {
        orderComponents = action.message.value;
        orderHash       = prepareResponse.orderHash
          ?? prepareResponse.order?.orderHash
          ?? prepareResponse.order?.hash;
        orderSignature  = await wallet.signTypedData(
          action.message.domain,
          action.message.types,
          action.message.value
        );
      }
    }

    if (!orderSignature || !orderHash || !orderComponents) {
      log(`  Error: No signable action for token ${tokenId}`);
      return null;
    }

    return { tokenId, orderComponents, orderHash, orderSignature };
  } catch(e) {
    const msg = e.message || '';
    if (msg.includes('504') || msg.includes('Gateway') || msg.includes('Timeout') || msg.includes('timeout')) {
      log(`  RPC timeout preparing token ${tokenId} — skipping`);
    } else {
      log(`  Error preparing listing for token ${tokenId}: ${msg}`);
      if (e.body) log(`  Error body: ${JSON.stringify(e.body)?.slice(0, 200)}`);
    }
    return null;
  }
}

// ─── SUBMIT A BATCH OF SIGNED LISTINGS (up to 20) ─────────────────────────
// Returns Set of tokenIds that were successfully submitted.
// alreadyListed: Set passed in from cycle — 400 errors get added to it
async function submitListingsBatch(signedOrders, alreadyListed) {
  const succeeded = new Set();
  if (signedOrders.length === 0) return succeeded;

  for (const o of signedOrders) {
    try {
      await orderbookClient.createListing({
        orderComponents: o.orderComponents,
        orderHash:       o.orderHash,
        orderSignature:  o.orderSignature,
        makerFees:       [],
      });
      succeeded.add(o.tokenId);
    } catch(e) {
      const msg = e.message || '';
      if (msg.includes('400') || msg.includes('Bad Request')) {
        // Token is already listed — add to known set so we don't retry
        if (alreadyListed) alreadyListed.add(o.tokenId);
        log(`  Token ${o.tokenId} already listed — skipping`);
      } else {
        log(`  Error submitting token ${o.tokenId}: ${msg}`);
      }
    }
  }

  return succeeded;
}

// ─── CANCEL A LISTING ──────────────────────────────────────────────────────
async function cancelListing(listingId) {
  try {
    const { cancellationAction } = await orderbookClient.cancelOrdersOnChain(
      [listingId],
      WALLET_ADDRESS
    );
    const tx      = await cancellationAction.buildTransaction();
    const receipt = await wallet.sendTransaction(tx);
    await receipt.wait();
    return true;
  } catch(e) {
    const msg = e?.message || '';
    if (msg.includes('504') || msg.includes('Gateway') || msg.includes('Timeout') || msg.includes('timeout')) {
      log(`  RPC timeout cancelling ${listingId} — will retry next cycle`);
    } else {
      // Dump every own property on the error (except stack) so we can finally
      // see what's behind "Generic Error". This is verbose but it's the only
      // way to find the right field on the SDK's wrapped errors.
      let dump = '';
      try {
        const keys = Object.getOwnPropertyNames(e).filter(k => k !== 'stack');
        dump = JSON.stringify(e, keys, 2).slice(0, 800);
        // Also walk the cause chain
        let cur = e?.cause, depth = 0;
        while (cur && depth < 3) {
          const ckeys = Object.getOwnPropertyNames(cur).filter(k => k !== 'stack');
          dump += `\n    caused by: ${JSON.stringify(cur, ckeys).slice(0, 400)}`;
          cur = cur?.cause; depth++;
        }
      } catch (jsonErr) {
        dump = `(could not stringify: ${jsonErr.message})`;
      }
      log(`  Error cancelling listing ${listingId}: ${msg}\n    kind=${e?.constructor?.name || typeof e}\n    full=${dump}`);
    }
    return false;
  }
}

// ─── INVALIDATE CACHES FOR A PROTO ────────────────────────────────────────
function invalidateProto(proto) {
  floorPrices.invalidateMyListings(proto);
  delete avgCache[proto];
}

// ─── CHECK FOR SALES ──────────────────────────────────────────────────────
async function checkForSales(currentListings) {
  if (prevListedTokenIds === null) {
    // First cycle — just record current listings, nothing to compare
    prevListedTokenIds = new Set(Object.keys(currentListings));
    return;
  }

  const usd = await getEthUsd();
  let sales = 0;

  for (const tokenId of prevListedTokenIds) {
    // If token was listed last cycle but isn't listed now, it was sold (or cancelled)
    if (currentListings[tokenId]) continue;

    // Verify it was actually sold by checking filled orders for this token
    try {
      const url = `https://api.immutable.com/v1/chains/${CHAIN}/orders/listings` +
        `?sell_item_contract_address=${GU_CONTRACT}` +
        `&sell_item_token_id[]=${tokenId}` +
        `&status=FILLED` +
        `&buy_item_contract_address=${ETH_ADDRESS}` +
        `&order_by=updated_at&direction=desc` +
        `&page_size=1`;
      const r = await apiFetch(url);
      const filled = r?.body?.result?.[0];
      if (!filled) continue; // not a sale — probably cancelled

      const amount   = filled.buy?.[0]?.amount ?? filled.buy?.amount;
      if (!amount) continue;
      const priceWei = BigInt(amount);
      const proto    = tokenToProto[tokenId];
      const cardName = proto ? await getCardName(proto) : `token:${tokenId}`;
      const usdVal   = ethToUsd(priceWei, usd);
      log(`${BLUE}  [SOLD] "${cardName}" @ ${ethers.formatEther(priceWei)} ETH ($${usdVal}) 🎉${RESET}`);
      sales++;
    } catch(e) {}

    await sleep(150);
  }

  if (sales > 0) log(`  ${sales} card(s) sold this cycle!`);
  prevListedTokenIds = new Set(Object.keys(currentListings));
}

// ─── MAIN CYCLE ────────────────────────────────────────────────────────────
async function runCycle(activeSets = ALLOWED_SETS) {
  const setLabel = activeSets === ALLOWED_SETS ? 'ALL sets' : [...activeSets].join(',');
  log(`─── Starting scan cycle (${setLabel}) ───`);

  // Refresh floor cache with latest listings before processing
  await floorPrices.refreshFloorCache();

  // Build owned map + fetch full NFT list (with quality) in parallel
  const [nfts, myListings] = await Promise.all([
    fetchOwnedNFTsFull(),
    fetchMyListings(),
  ]);

  // Check for sold cards (compare to previous cycle's listings)
  await checkForSales(myListings);

  // Rebuild token maps from fresh NFT data
  myTokenIds    = new Set();
  tokenToProto  = {};
  protoToTokens = {};
  for (const nft of nfts) {
    const attrs = nft.attributes || [];
    const pa    = attrs.find(a => a.trait_type === 'Proto');
    if (!pa) continue;
    const proto = String(pa.value);
    const tid   = nft.token_id;
    myTokenIds.add(tid);
    tokenToProto[tid] = proto;
    if (!protoToTokens[proto]) protoToTokens[proto] = new Set();
    protoToTokens[proto].add(tid);
  }
  ownedMapReady = true;

  const listedTokenIds = new Set(Object.keys(myListings));
  let listed = 0, relisted = 0, skipped = 0, errors = 0, noFloor = 0;
  let undercutRelists = 0; // count of downward (got-undercut) relists this cycle — capped by MAX_UNDERCUT_RELISTS

  const LIST_BATCH_SIZE = 20; // max listings per bulk submit

  // Re-order NFTs so we process one of each proto+quality first, then second copies, etc.
  // Within each copy round, cards where we are being undercut come first.
  // Pre-filter by allowed qualities and sets so progress counter is accurate.
  const nftsByProtoQuality = {};
  for (const nft of nfts) {
    const { proto, quality, set } = getProtoQuality(nft);
    if (!proto || !quality) continue;
    if (!ALLOWED_QUALITIES.has(quality)) continue;
    if (!activeSets.has(set)) continue;
    const key = `${proto}:${quality}`;
    if (!nftsByProtoQuality[key]) nftsByProtoQuality[key] = [];
    nftsByProtoQuality[key].push(nft);
  }

  // Determine which proto+quality keys are being undercut
  // (floor < our cheapest listing price for that proto+quality)
  const undercutKeys = new Set();
  for (const key of Object.keys(nftsByProtoQuality)) {
    const [proto, quality] = key.split(':');
    const floor = floorPrices.getFloor(proto, quality);
    if (!floor) continue;
    // Find cheapest of our listed tokens for this proto+quality
    const nftsForKey = nftsByProtoQuality[key];
    let ourCheapest = null;
    for (const nft of nftsForKey) {
      const tid = nft.token_id;
      if (!listedTokenIds.has(tid)) continue;
      const listing = myListings[tid];
      if (!listing) continue;
      const price = BigInt(listing._buyAmount || '0');
      if (price > 0n && (ourCheapest === null || price < ourCheapest)) ourCheapest = price;
    }
    // If floor is cheaper than our listing, we are being undercut
    if (ourCheapest !== null && floor < ourCheapest) undercutKeys.add(key);
  }

  // Sort keys: undercut ones first, then rest
  const sortedKeys  = Object.keys(nftsByProtoQuality).sort((a, b) => {
    const aUndercut = undercutKeys.has(a) ? 0 : 1;
    const bUndercut = undercutKeys.has(b) ? 0 : 1;
    return aUndercut - bUndercut;
  });

  log(`  Prioritising ${undercutKeys.size} undercut proto+quality groups`);

  const orderedNfts  = [];
  const maxCopies    = Math.max(...sortedKeys.map(k => nftsByProtoQuality[k].length));
  for (let copy = 0; copy < maxCopies; copy++) {
    for (const key of sortedKeys) {
      if (nftsByProtoQuality[key][copy]) orderedNfts.push(nftsByProtoQuality[key][copy]);
    }
  }

  // Queue of { tokenId, proto, targetPrice, cardName, usd } ready to be submitted
  let pendingListings = [];

  async function flushListingBatch() {
    if (pendingListings.length === 0) return;

    log(`  [BATCH] Preparing ${pendingListings.length} listings...`);

    // Prepare + sign each listing sequentially (SDK requirement)
    const signedOrders = [];
    for (const item of pendingListings) {
      const signed = await prepareOneListing(item.tokenId, item.targetPrice);
      if (signed) {
        signedOrders.push({ ...signed, ...item });
      } else {
        errors++;
      }
      await sleep(200);
    }

    // Submit all signed orders in one bulk call
    const succeeded = await submitListingsBatch(signedOrders, listedTokenIds);

    for (const item of signedOrders) {
      if (succeeded.has(item.tokenId)) {
        const lastSoldStr = item.avg30d ? ` | last sold ~$${ethToUsd(item.avg30d, item.usd)}` : '';
        log(`${qc(item.quality)}  [LIST] "${item.cardName}" [${item.quality}] @ ${ethers.formatEther(item.targetPrice)} ETH ($${ethToUsd(item.targetPrice, item.usd)})${lastSoldStr}${RESET}`);
        listed++;
        listedTokenIds.add(item.tokenId);
        invalidateProto(item.proto);
      } else {
        errors++;
      }
    }

    pendingListings = [];
  }

  for (let i = 0; i < orderedNfts.length; i++) {
    const nft     = orderedNfts[i];
    const tokenId = nft.token_id;
    const { proto, quality, set } = getProtoQuality(nft);

    if (!proto || !quality) { skipped++; continue; }
    if (!ALLOWED_QUALITIES.has(quality)) { skipped++; continue; }
    if (!activeSets.has(set))            { skipped++; continue; }

    let   floor  = await fetchFloorPrice(proto, quality);
    const avg30d = await fetch30DayAvg(proto, quality);

    // ── Shine-multiplier fallback ─────────────────────────────────────────
    // For Shadow/Gold/Diamond cards with no market data, derive a price from
    // the SAME proto's Meteorite version using forge-cost ratios:
    //   Shadow = 5x Met, Gold = 25x Met, Diamond = 125x Met.
    // Reference price for the multiplier prefers recent-sale median (more
    // trustworthy) over the cheapest listing (can be a troll low).
    if (!floor && USE_SHINE_MULTIPLIER) {
      const mult = SHINE_MULT[quality];
      if (mult && mult > 1n) {
        const metAvg   = await fetch30DayAvg(proto, 'Meteorite');
        const metFloor = metAvg ? null : await fetchFloorPrice(proto, 'Meteorite');
        const ref = metAvg || metFloor;
        if (ref && ref > 0n) {
          floor = ref * mult;
          log(`  ${qc(quality)}[MULT-FLOOR] proto ${proto} [${quality}] derived from Met ${metAvg ? 'sales' : 'floor'} ` +
              `(${ethers.formatEther(ref)} ETH × ${mult}n) = ${ethers.formatEther(floor)} ETH${RESET}`);
        }
      }
    }

    if (!floor) { noFloor++; continue; }

    // Dump protection: if we have sales history, floor must be >= 90% of median sale
    // If no sales history (rare/higher shine cards), use avg of 3 cheapest listings instead
    // Aggressive-undercut mode bypasses this entirely (relies on its own safety floor below).
    if (!AGGRESSIVE_UNDERCUT) {
      if (avg30d) {
        const minPrice = avg30d * BigInt(Math.round(MIN_FLOOR_RATIO * 100)) / BigInt(100);
        if (floor < minPrice) { skipped++; continue; }
      } else {
        const top3Avg = await fetchTop3Avg(proto, quality);
        if (top3Avg) {
          const minPrice = top3Avg * BigInt(Math.round(MIN_FLOOR_RATIO * 100)) / BigInt(100);
          if (floor < minPrice) { skipped++; continue; }
        }
      }
    }

    // ── Recent-sales guard ─────────────────────────────────────────────────
    // If the last N sales averaged BELOW the current lowest ask, nobody's
    // actually buying at these prices — LIST at the recent-sales price
    // instead of at the (too-high) market ask. Opt-in via config.
    if (USE_PAST_SALES_GUARD) {
      const nSalesAvg = await fetchLastNSalesAvg(proto, quality, PAST_SALES_GUARD_N);
      if (nSalesAvg && nSalesAvg < floor) {
        log(`  ${qc(quality)}[GUARD] proto ${proto} [${quality}] using last-${PAST_SALES_GUARD_N}-sales avg ${ethers.formatEther(nSalesAvg)} ETH instead of ask ${ethers.formatEther(floor)} ETH${RESET}`);
        floor = nSalesAvg;
      }
    }

    let targetPrice            = floor - 1n; // undercut by exactly 1 wei — cheapest without rounding loss

    // ── Aggressive undercut safety floor ───────────────────────────────────
    // In aggressive mode we undercut everyone, but never below undercutFloorPct%
    // of the last-N-sales average. Clamp the target up if we'd go below.
    if (AGGRESSIVE_UNDERCUT) {
      const undercutRefAvg = await fetchLastNSalesAvg(proto, quality, UNDERCUT_SALES_N);
      if (undercutRefAvg && undercutRefAvg > 0n) {
        const minAllowed = undercutRefAvg * BigInt(UNDERCUT_FLOOR_PCT) / 100n;
        if (targetPrice < minAllowed) {
          log(`  ${qc(quality)}[UNDERCUT-FLOOR] proto ${proto} [${quality}] clamped from ${ethers.formatEther(targetPrice)} to ${ethers.formatEther(minAllowed)} ETH (${UNDERCUT_FLOOR_PCT}% of last-${UNDERCUT_SALES_N}-sales avg)${RESET}`);
          targetPrice = minAllowed;
        }
      }
    }
    const [usd, cardName, priceCheck] = await Promise.all([getEthUsd(), getCardName(proto), validatePrice(proto, targetPrice)]);

    // Cross-check price against GU game API metadata
    if (!priceCheck.valid) {
      log(`  [SKIP] "${cardName}" [${quality}] — ${priceCheck.reason}`);
      skipped++;
      continue;
    }

    if (!listedTokenIds.has(tokenId)) {
      // Queue for batch listing
      pendingListings.push({ tokenId, proto, quality, targetPrice, cardName, usd, avg30d });

      // Flush when batch is full
      if (pendingListings.length >= LIST_BATCH_SIZE) {
        await flushListingBatch();
      }

    } else {
      // Already listed — check if relist needed (still one at a time, needs cancel first)
      const currentListing = myListings[tokenId];
      const currentPrice   = BigInt(currentListing._buyAmount || '0');
      const listingId      = currentListing.id ?? currentListing.listing_id ?? currentListing.order_id;

      if (currentPrice === 0n) { skipped++; continue; }

      // Relist in BOTH directions so we always hug the floor:
      //   ↓ we got undercut    → targetPrice dropped below currentPrice - threshold
      //   ↑ the floor moved up → targetPrice rose above currentPrice + threshold
      // RELIST_THRESHOLD (basis points) creates a dead-band to avoid thrashing on 1-wei wiggles.
      const bps        = BigInt(Math.round(RELIST_THRESHOLD * 10000)); // 0.01 -> 100 bps
      const lowerBound = currentPrice * (10000n - bps) / 10000n;
      const upperBound = currentPrice * (10000n + bps) / 10000n;
      const isUndercut = targetPrice < lowerBound;  // ↓ being undercut
      const floorRose  = targetPrice > upperBound;  // ↑ floor moved up
      // Cap downward (got-undercut) relists per cycle to save IMX fees on undercut wars.
      if (isUndercut && undercutRelists >= MAX_UNDERCUT_RELISTS) {
        skipped++;
        continue;
      }
      if (isUndercut || floorRose) {
        // Flush any pending new listings before relisting
        await flushListingBatch();

        // Count the ATTEMPT (not just the success) so the cap triggers even
        // when cancels keep failing with errors like "Generic Error" — otherwise
        // a broken cancel endpoint causes the bot to hammer every candidate.
        if (isUndercut) undercutRelists++;

        const dir         = targetPrice > currentPrice ? '↑' : '↓';
        const lastSoldStr = avg30d ? ` | last sold ~$${ethToUsd(avg30d, usd)}` : '';
        log(`${qc(quality)}  [RELIST${dir}] "${cardName}" [${quality}] ${ethers.formatEther(currentPrice)} -> ${ethers.formatEther(targetPrice)} ETH ($${ethToUsd(targetPrice, usd)})${lastSoldStr}${RESET}`);
        const cancelled = await cancelListing(listingId);
        if (cancelled) {
          await sleep(3000);
          const signed = await prepareOneListing(tokenId, targetPrice);
          if (signed) {
            const succeeded = await submitListingsBatch([signed], listedTokenIds);
            if (succeeded.has(tokenId)) { relisted++; invalidateProto(proto); } else errors++;
          } else errors++;
        } else errors++;
      } else {
        skipped++;
      }
    }

    if ((i + 1) % 100 === 0) {
      log(`  Progress: ${i + 1}/${orderedNfts.length} | Listed:${listed} Relisted:${relisted} Skipped:${skipped} NoFloor:${noFloor} Errors:${errors}`);
    }
  }

  // Flush any remaining queued listings
  await flushListingBatch();

  log(`─── Cycle done: Listed:${listed} Relisted:${relisted} (undercut ${undercutRelists}/${MAX_UNDERCUT_RELISTS}) Skipped:${skipped} NoFloor:${noFloor} Errors:${errors} ───`);
}

// ─── ENTRY POINT ───────────────────────────────────────────────────────────

// Catch any unhandled promise rejections — prevents crash on unexpected errors
process.on('unhandledRejection', (reason) => {
  const msg = (reason?.message || String(reason) || '').slice(0, 200);
  log(`[unhandledRejection] ${msg} — bot continues`);
});

process.on('uncaughtException', (e) => {
  const msg = (e?.message || String(e) || '').slice(0, 200);
  log(`[uncaughtException] ${msg} — bot continues`);
});

// ── PAUSE / RESUME (IPC from parent Electron process) ──────────────────────
// Pause takes effect at the next cycle boundary (after the current cycle
// finishes). Resume picks up immediately. All in-memory state is preserved.
let paused = false;
if (process.send) {
  process.on('message', (msg) => {
    if (!msg || typeof msg !== 'object') return;
    if (msg.type === 'pause' && !paused) {
      paused = true;
      log('━━━ PAUSE requested — bot will idle after the current cycle finishes ━━━');
    } else if (msg.type === 'resume' && paused) {
      paused = false;
      log('━━━ RESUME — next cycle starts now ━━━');
    }
  });
}
async function waitWhilePaused() {
  if (!paused) return;
  log('━━━ PAUSED — waiting for resume... ━━━');
  while (paused) await sleep(2000);
}

function isRpcError(e) {
  const msg = (e?.message || e?.shortMessage || String(e) || '').toLowerCase();
  return msg.includes('504') || msg.includes('gateway') || msg.includes('timeout') ||
         msg.includes('server_error') || msg.includes('network') || msg.includes('econnreset') ||
         msg.includes('econnrefused') || msg.includes('enotfound');
}

(async () => {
  if (!PRIVATE_KEY || !WALLET_ADDRESS) {
    console.error('ERROR: Missing PRIVATE_KEY or WALLET_ADDRESS in .env');
    process.exit(1);
  }

  await setup();

  // Init floor price cache
  log('Initialising floor price cache (this takes a while on first run)...');
  while (true) {
    try {
      await floorPrices.init();
      break;
    } catch(e) {
      log(`Floor init error: ${e.message} — retrying in 30s`);
      await sleep(30000);
    }
  }
  log('Floor price cache ready.');

  // Loop ticks every FAST_INTERVAL (30 min). Fast sets (plague) relist every tick;
  // all other sets run once per SCAN_INTERVAL (24h). lastFullRun=0 forces a full
  // run on the first tick.
  let lastFullRun = 0;
  while (true) {
    await waitWhilePaused();   // block here if user clicked Pause in the UI
    const doFull = Date.now() - lastFullRun >= SCAN_INTERVAL;
    const activeSets = doFull ? ALLOWED_SETS : FAST_SETS;
    if (doFull) lastFullRun = Date.now();

    try {
      await runCycle(activeSets);
    } catch(e) {
      if (isRpcError(e)) {
        log(`RPC error — waiting 60s before retry: ${(e.message || '').slice(0, 100)}`);
        await sleep(60000);
        continue;
      }
      log(`Cycle error: ${e.message}`);
      log(e.stack);
    }
    const nextFullIn = Math.max(0, SCAN_INTERVAL - (Date.now() - lastFullRun));
    log(`Sleeping ${(FAST_INTERVAL / 60000).toFixed(0)}m (fast: ${[...FAST_SETS].join(',')}; full run in ${(nextFullIn / 3600000).toFixed(1)}h)...`);
    await sleep(FAST_INTERVAL);
  }
})();
