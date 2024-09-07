// Import Des Dépendances
const { app, BrowserWindow, ipcMain, BaseWindow, WebContentsView } = require('electron')
const path = require('node:path')
const { exec } = require('child_process');
const wifi = require('node-wifi');
const fs = require('fs');

//Gestion Configuration
const configPath = path.join(__dirname, 'config.json');
let config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
console.log('Configuration:', config);

ipcMain.on('configrequest', (event) => {
    console.log('Demande de configuration reçue...');
    event.reply('configrequest',config);
});

// Variables Globales
let boundsvalue = {}
let actualyview = 'mainwiew';

// Création de la fenêtre
const createWindow = () => {
  const mainWindow = new BaseWindow({
    width: 800,
    height: 480,
    menuBarVisible: false,
    autoHideMenuBar: true,
    webPreferences: {
        nodeIntegration: true,
    }
  });

  bannerwiew = new WebContentsView({
    webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
        nodeIntegration: true,
        contextIsolation: true
    }
  });

    mainWindow.contentView.addChildView(bannerwiew);
    bannerwiew.webContents.loadFile('banner.html');
    

  mainwiew = new WebContentsView({
    webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
        nodeIntegration: true,
        contextIsolation: true
    }
  });

    mainWindow.contentView.addChildView(mainwiew);
    mainwiew.webContents.loadFile('index.html');

  settingswiew = new WebContentsView({
    webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
        nodeIntegration: true,
        contextIsolation: true
    }
    });
  
    mainWindow.contentView.addChildView(settingswiew);
    settingswiew.webContents.loadFile('settings.html');

   // Initialisation des vues avec les dimensions actuelles de la fenêtre
   updateViewBounds();

   // Écouteur pour le redimensionnement de la fenêtre
   mainWindow.on('resize', () => {
     updateViewBounds();
   });
 
   // Fonction pour mettre à jour les dimensions des vues
   function updateViewBounds() {
     const bounds = mainWindow.getBounds();
     boundsvalue = bounds;
     const width = bounds.width;
     const height = bounds.height;
     bannerwiew.setBounds({ x: 0, y: 0, width: width, height: 50});
     if (actualyview === 'mainwiew') {
        mainwiew.setBounds({ x: 0, y: 50, width: width, height: height - 50 });
    }else {
        settingswiew.setBounds({ x: 0, y: 50, width: width, height: height - 50 });
    }}

   
 }

 // Gestion des événements IPC pour changer de vue
ipcMain.on('show-view', (event, view) => {
    console.log('show-view', view);
    const bounds = boundsvalue;
    const width = bounds.width;
    const height = bounds.height;

    if (view === 'mainwiew') {
      mainwiew.setBounds({ x: 0, y: 50, width: width, height: height - 50 });
      settingswiew.setBounds({ x: 0, y: 50, width: 0, height: 0 });;
      actualyview = 'mainwiew';
    } else if (view === 'settingswiew') {
      mainwiew.setBounds({ x: 0, y: 50, width: 0, height: 0 });
      settingswiew.setBounds({ x: 0, y: 50, width: width, height: height - 50 });
      actualyview = 'settingswiew';
    }
});
app.whenReady().then(() => {
  createWindow()

})
ipcMain.on('setconfig', (event, newConfig) => {
    console.log('Nouvelle configuration en application... :', newConfig);
    fs.writeFileSync(configPath, JSON.stringify(newConfig, null, 2));
    console.log('Configuration enregistrée:');
    console.log('application de la jnouvelle configuration...');
    config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    console.log('Configuration appliqué');

});


ipcMain.on('wifianalyser', (event) => {
    wifi.init({
        iface: null // network interface, choose a random wifi interface if set to null
    });
    
    wifi.scan((error, networks) => {
        if (error) {
            console.log(error);
        } else {
            //console.log(networks);
            event.reply('wifianalyser', networks);
        }
    });
});

ipcMain.on('aircrackattack', (event, command) => {
    console.log('Airack command:', command);
    exec(command, (error, stdout, stderr) => {
        if (error) {
            event.sender.send('run-aircrack-command-response', `Erreur: ${error.message}`);
            console.log(`Erreur: ${error.message}`);
        } else if (stderr) {
            event.sender.send('run-aircrack-command-response', `Erreur: ${stderr}`);
            console.log(`Erreur: ${stderr}`);
        } else {
            event.sender.send('run-aircrack-command-response', stdout);
            console.log(`stdout: ${stdout}`);
        }
    });
});

ipcMain.on('log-report', (event, report) => {
    console.log('Rapport Provenant du renderer:\n\n', report);
});

  