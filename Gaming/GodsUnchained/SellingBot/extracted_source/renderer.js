// ── Tab navigation ──────────────────────────────────────────────────────────
const tabs   = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.panel');
tabs.forEach(t => t.addEventListener('click', () => {
  const id = t.dataset.tab;
  tabs.forEach(x => x.classList.toggle('active', x === t));
  panels.forEach(p => p.classList.toggle('active', p.id === `tab-${id}`));
}));

// ── Status pill ─────────────────────────────────────────────────────────────
const statusDot  = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const btnStart   = document.getElementById('btnStart');
const btnStop    = document.getElementById('btnStop');
const btnPause   = document.getElementById('btnPause');
function setStatus(s) {
  // s = { running, paused, pid }
  const running = !!s?.running;
  const paused  = !!s?.paused;
  statusDot.classList.toggle('running', running && !paused);
  statusDot.classList.toggle('paused',  running && paused);
  if (!running)     statusText.textContent = 'Stopped';
  else if (paused)  statusText.textContent = `Paused (pid ${s.pid}) — click Resume to continue`;
  else              statusText.textContent = `Running (pid ${s.pid})`;
  btnStart.disabled = running;
  btnStop.disabled  = !running;
  btnPause.disabled = !running;
  btnPause.textContent = paused ? '▶ Resume' : '⏸ Pause';
  btnPause.classList.toggle('primary', paused);
  btnPause.classList.toggle('warn',   !paused);
}

// ── Log view ────────────────────────────────────────────────────────────────
// Bot writes two non-trivial things we have to handle to match a terminal:
//   1. \r-based progress updates that overwrite the same line in place.
//   2. ANSI color escapes (\x1b[34m) for colored output.
const logView = document.getElementById('logView');
const MAX_LOG_CHARS = 200_000;
let committedText = '';   // text confirmed by a \n
let currentLine   = '';   // in-progress line since last \n (reset by \r)

const ANSI_COLORS = {
  '30': '#414868', '31': '#f7768e', '32': '#9ece6a', '33': '#e0af68',
  '34': '#7aa2f7', '35': '#bb9af7', '36': '#7dcfff', '37': '#c0caf5',
  '90': '#565f89', '91': '#ff7a93', '92': '#b9f27c', '93': '#ffd866',
  '94': '#7aa2f7', '95': '#c574dd', '96': '#7dcfff', '97': '#ffffff',
};
const ANSI_RE = /\x1b\[([0-9;]*)m/g;
const ESC_HTML = { '&': '&amp;', '<': '&lt;', '>': '&gt;' };
const esc = s => s.replace(/[&<>]/g, c => ESC_HTML[c]);

function ansiToHtml(s) {
  let out = '', openSpan = false, lastIdx = 0, m;
  ANSI_RE.lastIndex = 0;
  while ((m = ANSI_RE.exec(s)) !== null) {
    out += esc(s.substring(lastIdx, m.index));
    if (openSpan) { out += '</span>'; openSpan = false; }
    for (const code of m[1].split(';')) {
      if (code === '0' || code === '') continue; // reset
      const color = ANSI_COLORS[code];
      if (color) { out += `<span style="color:${color}">`; openSpan = true; }
    }
    lastIdx = ANSI_RE.lastIndex;
  }
  out += esc(s.substring(lastIdx));
  if (openSpan) out += '</span>';
  return out;
}

function appendLog(text) {
  text = text.replace(/\r\n/g, '\n');           // normalize Windows line endings
  const segs = text.split('\n');
  for (let i = 0; i < segs.length; i++) {
    const seg = segs[i];
    const lastR = seg.lastIndexOf('\r');
    if (lastR >= 0) currentLine = seg.substring(lastR + 1); // \r → overwrite current line
    else            currentLine += seg;
    if (i < segs.length - 1) {                   // \n → commit current line
      committedText += currentLine + '\n';
      currentLine = '';
    }
  }
  if (committedText.length > MAX_LOG_CHARS) {
    committedText = committedText.substring(committedText.length - MAX_LOG_CHARS);
  }
  logView.innerHTML = ansiToHtml(committedText + currentLine);
  logView.scrollTop = logView.scrollHeight;
}
window.api.onLog(({ text }) => appendLog(text));
window.api.onStatus(s => setStatus(s));

// ── Run tab buttons ─────────────────────────────────────────────────────────
btnStart.addEventListener('click', async () => {
  appendLog('[ui] starting bot...\n');
  const r = await window.api.startBot();
  if (!r.ok) {
    appendLog(`[ui] ERROR: ${r.error}\n`);
    alert(r.error);
  }
});
btnStop.addEventListener('click', async () => {
  appendLog('[ui] stopping bot...\n');
  await window.api.stopBot();
});
btnPause.addEventListener('click', async () => {
  // Button toggles between Pause and Resume based on current state
  const paused = btnPause.textContent.includes('Resume');
  if (paused) {
    appendLog('[ui] resuming bot...\n');
    const r = await window.api.resumeBot();
    if (!r.ok) appendLog(`[ui] ERROR: ${r.error}\n`);
  } else {
    appendLog('[ui] pausing bot — will idle after the current cycle finishes...\n');
    const r = await window.api.pauseBot();
    if (!r.ok) appendLog(`[ui] ERROR: ${r.error}\n`);
  }
});
document.getElementById('btnClearLog').addEventListener('click', () => {
  committedText = '';
  currentLine = '';
  logView.textContent = '';
});
document.getElementById('btnOpenLog').addEventListener('click', () => window.api.openLog());
document.getElementById('btnOpenFolder').addEventListener('click', () => window.api.openBotFolder());

// ── Settings tab ────────────────────────────────────────────────────────────
const form = document.getElementById('settingsForm');
const qboxes = () => document.querySelectorAll('.qbox');

function populateSettings(cfg) {
  document.getElementById('cfg_relistThresholdPct').value  = (cfg.relistThreshold * 100).toFixed(2);
  document.getElementById('cfg_maxUndercutRelists').value  = cfg.maxUndercutRelists;
  document.getElementById('cfg_minFloorRatioPct').value    = Math.round(cfg.minFloorRatio * 100);
  document.getElementById('cfg_scanIntervalMin').value     = Math.round(cfg.scanIntervalMs / 60000);
  document.getElementById('cfg_fastIntervalMin').value     = Math.round(cfg.fastIntervalMs / 60000);
  document.getElementById('cfg_fastSets').value            = (cfg.fastSets || []).join(', ');
  document.getElementById('cfg_allowedSets').value         = (cfg.allowedSets || []).join(', ');
  document.getElementById('cfg_requestDelay').value        = cfg.requestDelay;
  document.getElementById('cfg_avgCacheTtlMin').value      = Math.round(cfg.avgCacheTtlMs / 60000);
  document.getElementById('cfg_useShineMultiplier').checked = cfg.useShineMultiplier !== false;
  document.getElementById('cfg_whitelistedWallets').value = (cfg.whitelistedWallets || []).join('\n');
  document.getElementById('cfg_usePastSalesGuard').checked = cfg.usePastSalesGuard === true;
  document.getElementById('cfg_pastSalesGuardN').value = cfg.pastSalesGuardN ?? 5;
  document.getElementById('cfg_aggressiveUndercut').checked = cfg.aggressiveUndercut === true;
  document.getElementById('cfg_undercutFloorPct').value = cfg.undercutFloorPct ?? 90;
  document.getElementById('cfg_undercutSalesN').value = cfg.undercutSalesN ?? 5;
  const want = new Set(cfg.allowedQualities || []);
  qboxes().forEach(b => { b.checked = want.has(b.value); });
}

function readSettings() {
  const val = (id) => document.getElementById(id).value;
  const num = (id) => parseFloat(val(id));
  const int = (id) => parseInt(val(id), 10);
  const csv = (id) => val(id).split(',').map(s => s.trim()).filter(Boolean);
  return {
    relistThreshold:    num('cfg_relistThresholdPct') / 100,
    maxUndercutRelists: int('cfg_maxUndercutRelists'),
    minFloorRatio:      num('cfg_minFloorRatioPct') / 100,
    scanIntervalMs:     int('cfg_scanIntervalMin') * 60000,
    fastIntervalMs:     int('cfg_fastIntervalMin') * 60000,
    fastSets:           csv('cfg_fastSets'),
    allowedSets:        csv('cfg_allowedSets'),
    allowedQualities:   [...qboxes()].filter(b => b.checked).map(b => b.value),
    requestDelay:       int('cfg_requestDelay'),
    avgCacheTtlMs:      int('cfg_avgCacheTtlMin') * 60000,
    useShineMultiplier: document.getElementById('cfg_useShineMultiplier').checked,
    whitelistedWallets: document.getElementById('cfg_whitelistedWallets').value
                          .split(/[\s,]+/).map(s => s.trim().toLowerCase())
                          .filter(s => /^0x[a-f0-9]{40}$/.test(s)),
    usePastSalesGuard:  document.getElementById('cfg_usePastSalesGuard').checked,
    pastSalesGuardN:    int('cfg_pastSalesGuardN'),
    aggressiveUndercut: document.getElementById('cfg_aggressiveUndercut').checked,
    undercutFloorPct:   int('cfg_undercutFloorPct'),
    undercutSalesN:     int('cfg_undercutSalesN'),
  };
}

function validateCfg(cfg) {
  const errs = [];
  if (!(cfg.relistThreshold >= 0 && cfg.relistThreshold <= 0.5)) errs.push('Relist threshold must be 0–50%.');
  if (!(cfg.minFloorRatio >= 0 && cfg.minFloorRatio <= 1))      errs.push('Dump-protection ratio must be 0–100%.');
  if (cfg.maxUndercutRelists < 0)                                errs.push('Max undercut relists must be 0 or more.');
  if (cfg.scanIntervalMs < 60000)                                errs.push('Full cycle interval must be at least 1 minute.');
  if (cfg.fastIntervalMs < 60000)                                errs.push('Fast cycle interval must be at least 1 minute.');
  if (cfg.allowedQualities.length === 0)                         errs.push('Pick at least one quality.');
  if (cfg.allowedSets.length === 0)                              errs.push('Pick at least one set.');
  return errs;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const cfg = readSettings();
  const errs = validateCfg(cfg);
  const msg = document.getElementById('cfgSavedMsg');
  if (errs.length) {
    msg.textContent = '✘ ' + errs.join(' ');
    msg.className = 'saved-msg err';
    return;
  }
  await window.api.saveConfig(cfg);
  msg.textContent = '✓ Saved — restart the bot for changes to apply.';
  msg.className = 'saved-msg ok';
  setTimeout(() => { msg.textContent = ''; }, 6000);
});

document.getElementById('btnResetCfg').addEventListener('click', async () => {
  const cfg = await window.api.getConfig();
  populateSettings(cfg);
});

// ── Wallet tab ──────────────────────────────────────────────────────────────
const walletForm = document.getElementById('walletForm');
async function loadWallet() {
  const env = await window.api.getEnv();
  document.getElementById('env_WALLET_ADDRESS').value  = env.WALLET_ADDRESS || '';
  document.getElementById('env_PRIVATE_KEY').value     = env.PRIVATE_KEY || '';
  document.getElementById('env_PUBLISHABLE_KEY').value = env.PUBLISHABLE_KEY || '';
}
walletForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const env = {
    PRIVATE_KEY:     document.getElementById('env_PRIVATE_KEY').value.trim(),
    WALLET_ADDRESS:  document.getElementById('env_WALLET_ADDRESS').value.trim().toLowerCase(),
    PUBLISHABLE_KEY: document.getElementById('env_PUBLISHABLE_KEY').value.trim(),
  };
  const msg = document.getElementById('walletSavedMsg');
  if (!env.WALLET_ADDRESS.match(/^0x[a-f0-9]{40}$/)) {
    msg.textContent = '✘ Wallet address must be 0x + 40 hex chars.';
    msg.className = 'saved-msg err';
    return;
  }
  if (!env.PRIVATE_KEY.match(/^(0x)?[a-fA-F0-9]{64}$/)) {
    msg.textContent = '✘ Private key must be 64 hex chars (with or without 0x).';
    msg.className = 'saved-msg err';
    return;
  }
  if (!env.PRIVATE_KEY.startsWith('0x')) env.PRIVATE_KEY = '0x' + env.PRIVATE_KEY;
  await window.api.saveEnv(env);
  msg.textContent = '✓ Saved.';
  msg.className = 'saved-msg ok';
  setTimeout(() => { msg.textContent = ''; }, 4000);
});

document.getElementById('btnTogglePK').addEventListener('click', () => {
  const inp = document.getElementById('env_PRIVATE_KEY');
  const btn = document.getElementById('btnTogglePK');
  const showing = inp.type === 'text';
  inp.type = showing ? 'password' : 'text';
  btn.textContent = showing ? 'Show' : 'Hide';
});

// ── Initial load ────────────────────────────────────────────────────────────
(async () => {
  try {
    const cfg = await window.api.getConfig();
    populateSettings(cfg);
    await loadWallet();
    setStatus(await window.api.getStatus());
  } catch (e) {
    appendLog(`[ui] init error: ${e.message}\n`);
  }
})();
