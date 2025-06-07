const { contextBridge, ipcRenderer } = require('electron')
const fs = require('fs');
const path = require('node:path');

// Charger la configuration
const configPath = path.join(__dirname, 'config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

contextBridge.exposeInMainWorld('materialapi', {
  wifianalyser: () => ipcRenderer.send('wifianalyser'),
  
  configrequest: () => ipcRenderer.send('configrequest'),
  setconfig: (command) => ipcRenderer.send('setconfig', command),
  enableMonitor: () => ipcRenderer.send('enableMonitor'),
  disableMonitor: () => ipcRenderer.send('disableMonitor'),
  statusMonitor: () => ipcRenderer.send('statusMonitor'),
  deauthattack: (channel,bssid,deauth) => ipcRenderer.send('deauthattack', channel,bssid,deauth),
  startHandshakeCapture: (bssid, channel) => ipcRenderer.send('start-handshake-capture', bssid, channel),
  config: config
  // nous pouvons aussi exposer des variables en plus des fonctions
})

contextBridge.exposeInMainWorld('refreshapi', {
    ResultTextBox: (callback) => ipcRenderer.on('update-results', callback),
    wifianalyser: (callback) => ipcRenderer.on('wifianalyser', callback),
    configrequest: (callback) => ipcRenderer.on('configrequest', callback),
    statusMonitor: (callback) => ipcRenderer.on('statusMonitor', callback),
    deauthCounterUpdate: (callback) => ipcRenderer.on('deauth-counter-update', callback),
  })

contextBridge.exposeInMainWorld('appapi', {
  showview: (wiew) => ipcRenderer.send('show-view', wiew),
  logreport: (report) => ipcRenderer.send('log-report', report)
  })