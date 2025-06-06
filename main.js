// Import Des Dépendances
const { app, BrowserWindow, ipcMain, BaseWindow, WebContentsView, globalShortcut, webContents } = require('electron')
const path = require('node:path')
const { exec } = require('child_process');
const wifi = require('node-wifi');
const fs = require('fs');
const uploadFile = require('./upload'); // Importez la fonction uploadFile
const { Interface } = require('node:readline');
const { log } = require('node:console');



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
let mainWindow
let mainwiew

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

  //bannerwiew = new WebContentsView({
    //webPreferences: {
      //  preload: path.join(__dirname, 'preload.js'),
      //  nodeIntegration: true,
      //  contextIsolation: true
    //}
  //});

    //mainWindow.contentView.addChildView(bannerwiew);
    //bannerwiew.webContents.loadFile('banner.html');
    

  mainwiew = new WebContentsView({
    webPreferences: {
        preload: path.join(__dirname, 'preload.js'),
        nodeIntegration: true,
        contextIsolation: true
    }
  });

    mainWindow.contentView.addChildView(mainwiew);
    mainwiew.webContents.loadFile('index.html');

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
     //bannerwiew.setBounds({ x: 0, y: 0, width: width, height: 50});
     mainwiew.setBounds({ x: 0, y: 0, width: width, height: height });
    }
  
    // Gestion des événements IPC pour changer de vue
ipcMain.on('show-view', (event, view) => {
    console.log('show-view', view);
    const bounds = boundsvalue;
    const width = bounds.width;
    const height = bounds.height;

    if (view === 'mainwiew') {
      if (actualyview === 'mainwiew') {
        console.log('La vue principale est déjà affichée.');
        } else {
        mainwiew.webContents.loadFile('index.html');
        actualyview = 'mainwiew';
        }

    } else if (view === 'settingswiew') {
      if (actualyview === 'settingswiew') {
        console.log('La vue des paramètres est déjà affichée.');
      }else {
      mainwiew.webContents.loadFile('settings.html');
      actualyview = 'settingswiew';
      }
    }
});    
    
    // Activer DevTools si le raccourci Ctrl+Shift+I est utilisé
  globalShortcut.register('Control+Shift+I', () => {
    if (mainwiew && mainwiew.webContents) {
      mainwiew.webContents.toggleDevTools();
    } else {
      console.log("La vue principale n'est pas définie.");
    }
  });

   
 }



app.whenReady().then(() => {
  createWindow()
  // Vérifier si aircrack-ng est installé
  try {
    const { execSync } = require('child_process');
    execSync('which aircrack-ng');
  } catch (error) {
    throw new Error('aircrack-ng n\'est pas installé. Installez-le avec: sudo apt-get install aircrack-ng');
  }
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

ipcMain.on('statusMonitor', (event) => {
    try {
        const { execSync } = require('child_process');
        const result = execSync(`iwconfig ${config.networkcard}`).toString();
        const isMonitorMode = result.includes('Mode:Monitor');
        statusMonitor = isMonitorMode;
        event.reply('statusMonitor', statusMonitor);
        log(`État du moniteur: ${statusMonitor ? 'Activé' : 'Désactivé'}`);
    } catch (error) {
        log(`Erreur lors de la vérification du mode moniteur: ${error.message}`);
        event.reply('statusMonitor', false);
    }
});

ipcMain.on('enableMonitor', (event) => {
  try {
      const { execSync } = require('child_process');
      // Vérifier si l'interface existe
      try {
          execSync(`iwconfig ${config.networkcard}`);
      } catch (error) {
          event.reply('statusMonitor', false);
          throw new Error(`L'interface ${config.networkcard} n'existe pas`);
      }
      // Exécuter airmon-ng avec pkexec
      execSync(`pkexec airmon-ng start ${config.networkcard}`);
      
      // Vérifier si le mode moniteur a été activé
      const result = execSync(`iwconfig ${config.networkcard}`).toString();
      const isMonitorMode = result.includes('Mode:Monitor');
      
      if (!isMonitorMode) {
          throw new Error('Le mode moniteur n\'a pas pu être activé');
      }

      event.reply('statusMonitor', true);
      log('Mode moniteur activé avec succès');
  } catch (error) {
      log(`Erreur lors de l'activation du mode moniteur: ${error.message}`);
      event.reply('statusMonitor', false);
  }
});

ipcMain.on('aircrackattack', (event, command) => {
    //console.log('Airack command:', command);
    uploadFile('styles.css', config.apiKey)
     .then(response => {
      const message = response.message;
      console.log(` \x1b[32m${message}\x1b[0m `);
     })
     .catch(error => console.error('Erreur :', error));

});









// Gestion des rapports de log provenant du renderer
ipcMain.on('log-report', (event, report) => {
    console.log('\x1b[32m%s\x1b[0m', 'Rapport Provenant du renderer:\n\n', report);
});

  