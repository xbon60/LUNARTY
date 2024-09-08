// Import Des Dépendances
const { app, BrowserWindow, ipcMain, BaseWindow, WebContentsView, globalShortcut, webContents } = require('electron')
const path = require('node:path')
const { exec } = require('child_process');
const wifi = require('node-wifi');
const fs = require('fs');
const uploadFile = require('./upload'); // Importez la fonction uploadFile



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
    uploadFile('styles.css', config.apiKey)
     .then(response => {
      const message = response.message;
      console.log(` \x1b[32m${message}\x1b[0m `);
     })
     .catch(error => console.error('Erreur :', error));

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
    console.log('\x1b[32m%s\x1b[0m', 'Rapport Provenant du renderer:\n\n', report);
});

  