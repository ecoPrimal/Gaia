// ═══ GAIA EASEL — preload bridge ═══
// Secure bridge between renderer and main process
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('gaia', {
  // File system
  readDir: (path) => ipcRenderer.invoke('read-dir', path),
  readFile: (path) => ipcRenderer.invoke('read-file', path),
  writeFile: (path, content) => ipcRenderer.invoke('write-file', path, content),

  // Terminal
  runCommand: (cmd, cwd) => ipcRenderer.invoke('run-command', cmd, cwd),

  // Ports
  checkPort: (port) => ipcRenderer.invoke('check-port', port),

  // AI
  think: (prompt, model) => ipcRenderer.invoke('think', prompt, model),

  // System
  gpuInfo: () => ipcRenderer.invoke('gpu-info'),
  sysInfo: () => ipcRenderer.invoke('sys-info'),
  openExternal: (url) => ipcRenderer.invoke('open-external', url),

  // Biome.exe — the front runner
  runBiome: () => ipcRenderer.invoke('run-biome'),
  runOrganismBinary: (name, args) => ipcRenderer.invoke('run-organism-binary', name, args),
  listOrganismBinaries: () => ipcRenderer.invoke('list-organism-binaries'),

  // Neural API
  capabilityCall: (cap, op, args) => ipcRenderer.invoke('capability-call', cap, op, args),

  // Ecosystem
  ecosystemMap: () => ipcRenderer.invoke('ecosystem-map'),

  // Google / Keyring
  getGoogleSession: () => ipcRenderer.invoke('get-google-session'),
  eatGoogleDocs: () => ipcRenderer.invoke('eat-google-docs'),
  launchPaint: () => ipcRenderer.invoke('launch-paint'),
  launchRustdesk: () => ipcRenderer.invoke('launch-rustdesk'),
  readHands: () => ipcRenderer.invoke('read-hands'),
  writeHands: (patch) => ipcRenderer.invoke('write-hands', patch),
  herReload: () => ipcRenderer.invoke('her-reload'),

  // Events from main
  on: (channel, callback) => {
    const validChannels = [
      'file-opened', 'folder-opened', 'save-file',
      'navigate-tab', 'toggle-chat', 'toggle-terminal',
      'toggle-sidebar', 'quick-open', 'think-selection',
      'eat-google-docs', 'open-paint', 'open-glass', 'her-act'
    ];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => callback(...args));
    }
  }
});
