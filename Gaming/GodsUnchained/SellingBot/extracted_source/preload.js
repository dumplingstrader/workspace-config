const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  getConfig: () => ipcRenderer.invoke('config:get'),
  saveConfig: (cfg) => ipcRenderer.invoke('config:save', cfg),
  getEnv: () => ipcRenderer.invoke('env:get'),
  saveEnv: (env) => ipcRenderer.invoke('env:save', env),
  getStatus: () => ipcRenderer.invoke('bot:status'),
  startBot: () => ipcRenderer.invoke('bot:start'),
  stopBot: () => ipcRenderer.invoke('bot:stop'),
  pauseBot: () => ipcRenderer.invoke('bot:pause'),
  resumeBot: () => ipcRenderer.invoke('bot:resume'),
  openBotFolder: () => ipcRenderer.invoke('app:openBotFolder'),
  openLog: () => ipcRenderer.invoke('app:openLog'),
  onLog: (cb) => ipcRenderer.on('bot:log', (_e, p) => cb(p)),
  onStatus: (cb) => ipcRenderer.on('bot:status', (_e, s) => cb(s)),
});
