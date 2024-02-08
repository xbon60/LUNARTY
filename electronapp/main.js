const { app, BrowserWindow, ipcMain } = require('electron')

let mainWindow;

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600
  })

  mainWindow.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow()
  
  ipcMain.on('activer-moniteur', () => {
    activer_moniteur();
  });

  ipcMain.on('desactiver-moniteur', () => {
    desactiver_moniteur();
  });
})

function activer_moniteur() {
  const displaymoniteur = mainWindow.webContents;
  let buttonaffichage = "a";
  displaymoniteur.executeJavaScript(`document.getElementById('displaymoniteur').textContent += '${buttonaffichage}'`);
}

function desactiver_moniteur() {
  const displaymoniteur = mainWindow.webContents;
  let buttonaffichage = "b";
  displaymoniteur.executeJavaScript(`document.getElementById('displaymoniteur').textContent += '${buttonaffichage}'`);
}
