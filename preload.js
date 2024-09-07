const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('materialapi', {
  wifianalyser: () => ipcRenderer.send('wifianalyser'),
  aircrackattack: (command) => ipcRenderer.send('aircrackattack', command),
  configrequest: () => ipcRenderer.send('configrequest'),
  setconfig: (command) => ipcRenderer.send('setconfig', command)
  // nous pouvons aussi exposer des variables en plus des fonctions
})

contextBridge.exposeInMainWorld('refreshapi', {
    ResultTextBox: (callback) => ipcRenderer.on('update-results', callback),
    wifianalyser: (callback) => ipcRenderer.on('wifianalyser', callback),
    configrequest: (callback) => ipcRenderer.on('configrequest', callback)
  })

contextBridge.exposeInMainWorld('appapi', {
  showview: (wiew) => ipcRenderer.send('show-view', wiew),
  logreport: (report) => ipcRenderer.send('log-report', report)
  })