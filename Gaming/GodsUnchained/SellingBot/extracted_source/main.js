const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path  = require('path');
const fs    = require('fs');
const { spawn } = require('child_process');

// ── Paths ────────────────────────────────────────────────────────────────────
// Bundled template lives next to the binary (or under resources/ in packaged builds).
// Working bot directory lives in userData so config/.env/log persist across runs.
const isPackaged = app.isPackaged;
const bundledBot = isPackaged
  ? path.join(process.resourcesPath, 'bot-template')
  : path.join(__dirname, 'bot-template');
let workingBotDir;   // set after app.whenReady (needs userData path)

let mainWindow = null;
let botProcess = null;

// ── First-run setup: copy bundled bot files into userData if not present ─────
function copyRecursive(src, dst) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    if (!fs.existsSync(dst)) fs.mkdirSync(dst, { recursive: true });
    for (const item of fs.readdirSync(src)) {
      copyRecursive(path.join(src, item), path.join(dst, item));
    }
  } else {
    fs.copyFileSync(src, dst);
  }
}

function ensureBotInstalled() {
  if (!fs.existsSync(workingBotDir)) {
    fs.mkdirSync(workingBotDir, { recursive: true });
  }
  const marker = path.join(workingBotDir, 'gu_bot.js');
  if (!fs.existsSync(marker)) {
    // First run: copy everything from the bundle
    console.log(`[setup] First run — copying bot files from ${bundledBot} to ${workingBotDir}`);
    copyRecursive(bundledBot, workingBotDir);
  }
  // Always ensure a config.json exists
  const cfgPath = path.join(workingBotDir, 'config.json');
  if (!fs.existsSync(cfgPath)) {
    const bundledCfg = path.join(bundledBot, 'config.json');
    if (fs.existsSync(bundledCfg)) fs.copyFileSync(bundledCfg, cfgPath);
  }
  // Always ensure a .env exists (blank values is fine — user fills via UI)
  const envPath = path.join(workingBotDir, '.env');
  if (!fs.existsSync(envPath)) {
    fs.writeFileSync(envPath, 'PRIVATE_KEY=\nWALLET_ADDRESS=\nPUBLISHABLE_KEY=publishable_imapct_4cFGq7Lsyb9Xu1nLZ6NSMH5oY22P9Gt5\n');
  }
}

// ── Window ───────────────────────────────────────────────────────────────────
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 980,
    height: 720,
    minWidth: 760,
    minHeight: 520,
    title: 'GU Bot',
    backgroundColor: '#1e1e2e',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });
  mainWindow.removeMenu();
  mainWindow.loadFile('index.html');
}

// ── .env parsing (simple KEY=VALUE, one per line) ────────────────────────────
function parseEnv(text) {
  const out = {};
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq < 0) continue;
    const k = line.slice(0, eq).trim();
    const v = line.slice(eq + 1).trim();
    out[k] = v;
  }
  return out;
}
function serializeEnv(obj) {
  return Object.entries(obj).map(([k, v]) => `${k}=${v ?? ''}`).join('\n') + '\n';
}

// ── IPC: config ──────────────────────────────────────────────────────────────
ipcMain.handle('config:get', () => {
  const p = path.join(workingBotDir, 'config.json');
  return JSON.parse(fs.readFileSync(p, 'utf8'));
});
ipcMain.handle('config:save', (_e, cfg) => {
  const p = path.join(workingBotDir, 'config.json');
  fs.writeFileSync(p, JSON.stringify(cfg, null, 2) + '\n');
  return true;
});

// ── IPC: env ────────────────────────────────────────────────────────────────
ipcMain.handle('env:get', () => {
  const p = path.join(workingBotDir, '.env');
  return parseEnv(fs.readFileSync(p, 'utf8'));
});
ipcMain.handle('env:save', (_e, envObj) => {
  const p = path.join(workingBotDir, '.env');
  fs.writeFileSync(p, serializeEnv(envObj));
  return true;
});

// ── IPC: bot process lifecycle ───────────────────────────────────────────────
let botPaused = false;
function statusPayload() {
  return { running: !!botProcess, paused: botPaused, pid: botProcess?.pid ?? null };
}
ipcMain.handle('bot:status', () => statusPayload());

ipcMain.handle('bot:start', () => {
  if (botProcess) return { ok: false, error: 'Bot already running' };
  const env = parseEnv(fs.readFileSync(path.join(workingBotDir, '.env'), 'utf8'));
  if (!env.PRIVATE_KEY || !env.WALLET_ADDRESS) {
    return { ok: false, error: 'Wallet not configured — fill in Wallet tab first' };
  }
  // Spawn the bot using Electron's bundled Node (ELECTRON_RUN_AS_NODE=1)
  // so the recipient doesn't need a separate Node install. The 4th 'ipc' slot
  // gives us a parent↔child message channel for pause/resume control.
  botProcess = spawn(process.execPath, ['gu_bot.js'], {
    cwd: workingBotDir,
    env: { ...process.env, ...env, ELECTRON_RUN_AS_NODE: '1' },
    stdio: ['ignore', 'pipe', 'pipe', 'ipc'],
  });
  botPaused = false;
  botProcess.stdout.setEncoding('utf8');
  botProcess.stderr.setEncoding('utf8');
  botProcess.stdout.on('data', d => mainWindow?.webContents.send('bot:log', { stream: 'out', text: d }));
  botProcess.stderr.on('data', d => mainWindow?.webContents.send('bot:log', { stream: 'err', text: d }));
  botProcess.on('error', (e) => {
    mainWindow?.webContents.send('bot:log', { stream: 'sys', text: `\n[bot] spawn error: ${e.message}\n` });
  });
  botProcess.on('exit', (code, sig) => {
    mainWindow?.webContents.send('bot:log', { stream: 'sys', text: `\n[bot] exited (code=${code} sig=${sig ?? '-'})\n` });
    botProcess = null;
    botPaused = false;
    mainWindow?.webContents.send('bot:status', statusPayload());
  });
  mainWindow?.webContents.send('bot:status', statusPayload());
  return { ok: true, pid: botProcess.pid };
});

ipcMain.handle('bot:stop', () => {
  if (!botProcess) return { ok: false, error: 'Bot not running' };
  try { botProcess.kill(); } catch {}
  return { ok: true };
});

ipcMain.handle('bot:pause', () => {
  if (!botProcess) return { ok: false, error: 'Bot not running' };
  if (botPaused) return { ok: false, error: 'Already paused' };
  try { botProcess.send({ type: 'pause' }); } catch (e) { return { ok: false, error: e.message }; }
  botPaused = true;
  mainWindow?.webContents.send('bot:status', statusPayload());
  return { ok: true };
});

ipcMain.handle('bot:resume', () => {
  if (!botProcess) return { ok: false, error: 'Bot not running' };
  if (!botPaused) return { ok: false, error: 'Not paused' };
  try { botProcess.send({ type: 'resume' }); } catch (e) { return { ok: false, error: e.message }; }
  botPaused = false;
  mainWindow?.webContents.send('bot:status', statusPayload());
  return { ok: true };
});

// ── IPC: utility ─────────────────────────────────────────────────────────────
ipcMain.handle('app:openBotFolder', () => shell.openPath(workingBotDir));
ipcMain.handle('app:openLog', () => {
  const lf = path.join(workingBotDir, 'bot.log');
  if (fs.existsSync(lf)) shell.openPath(lf);
});

// ── Lifecycle ────────────────────────────────────────────────────────────────
app.whenReady().then(() => {
  workingBotDir = path.join(app.getPath('userData'), 'bot');
  try { ensureBotInstalled(); }
  catch (e) {
    dialog.showErrorBox('Setup failed', `Could not prepare bot directory:\n${e.message}`);
    app.quit();
    return;
  }
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (botProcess) { try { botProcess.kill(); } catch {} }
  if (process.platform !== 'darwin') app.quit();
});

app.on('before-quit', () => {
  if (botProcess) { try { botProcess.kill(); } catch {} }
});
