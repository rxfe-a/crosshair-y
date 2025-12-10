const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld("overlayAPI", {
  onToggle: (handler) => ipcRenderer.on("toggle-image", handler)
});
