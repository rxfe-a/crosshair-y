const { app, BrowserWindow, globalShortcut } = require('electron');
const path = require('path');

let win;

function createWindow() {
  win = new BrowserWindow({
    fullscreen: true,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    focusable: false,
    hasShadow: false,
    enableLargerThanScreen: true,

    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      backgroundThrottling: false
    }
  });

  // Click-through support
  win.setIgnoreMouseEvents(true, { forward: true });

  // Load overlay UI
  win.loadFile(path.join(__dirname, "overlay/index.html"));

  // Hotkeys
  globalShortcut.register('F2', () => {
    win.webContents.send('toggle-image');
  });

  globalShortcut.register('F3', () => {
    app.quit();
  });
}

app.whenReady().then(() => {
  createWindow();
});

app.on("will-quit", () => globalShortcut.unregisterAll());

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});