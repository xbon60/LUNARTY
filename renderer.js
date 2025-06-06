let networkslist = []; // Déclaration d'une variable globale pour stocker les réseaux Wi-Fi
let deauthCounter = 0; // Compteur de requêtes de déauth

const config = window.materialapi.config

// renderer.js (gère le clic sur le bouton)
window.addEventListener('DOMContentLoaded', () => {
    const buttonwifi = document.getElementById('validatebuttonwifi');
    const container = document.getElementById('buttonContainer');
    const view1Button = document.getElementById('showmainmenu');
    const view2Button = document.getElementById('showsettingsmenu');
    const toggleMonitor = document.getElementById('togglemonitor');
    
    // Créer l'élément pour afficher le compteur
    const deauthCounterDisplay = document.createElement('div');
    deauthCounterDisplay.id = 'deauthCounter';
    deauthCounterDisplay.style.position = 'fixed';
    deauthCounterDisplay.style.top = '10px';
    deauthCounterDisplay.style.right = '10px';
    deauthCounterDisplay.style.padding = '10px';
    deauthCounterDisplay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    deauthCounterDisplay.style.color = 'white';
    deauthCounterDisplay.style.borderRadius = '5px';
    deauthCounterDisplay.textContent = 'Requêtes DeAuth: 0';
    document.body.appendChild(deauthCounterDisplay);

    // Écouter les mises à jour du compteur
    window.refreshapi.deauthCounterUpdate((event, count) => {
        deauthCounter = count;
        deauthCounterDisplay.textContent = `Requêtes DeAuth: ${count}`;
    });


    view1Button.addEventListener('click', () => {
        window.appapi.showview('mainwiew');    

    });

    view2Button.addEventListener('click', () => {
        window.appapi.showview('settingswiew');   
    
    });

    toggleMonitor.addEventListener('click', () => {
        window.appapi.logreport('Clic sur le bouton monitor');
        window.materialapi.statusMonitor();
        if (toggleMonitor.textContent == "Activer le moniteur") {
            window.materialapi.enableMonitor();
        } else if (toggleMonitor.textContent == "Désactiver le moniteur") {
            window.materialapi.disableMonitor();
        }
        
    });

    
    window.refreshapi.statusMonitor((event, status) => {
        window.appapi.logreport("Status monitor: " + status);
        // Mettre à jour l'interface utilisateur en fonction du statut
        toggleMonitor.textContent = status ? "Désactiver le moniteur" : "Activer le moniteur";
        toggleMonitor.style.backgroundColor = status ? 'red' : 'green';
        toggleMonitor.style.color = status ? 'white' : 'black';
    });

    // Ajoute un événement de clic pour déclencher une action backend
    buttonwifi.addEventListener('click', () => {
        window.appapi.logreport('Clic sur le bouton wifi');
      // Appelle la méthode exposée par preload.js
      window.materialapi.wifianalyser();
    });

    window.refreshapi.wifianalyser((event, networks) => {
        networkslist = networks; // Mettre à jour la variable globale
        window.appapi.logreport(`Réseaux wifi mis à jour: ${JSON.stringify(networkslist, null, 2)}`);
        displayNetworks(); // Afficher les réseaux
    });

    buttonContainer.addEventListener('click', (event) => {
            // Vérifier si l'élément cliqué est un bouton
            if (event.target.tagName === 'BUTTON') {
            // Extraire le BSSID de l'ID du bouton (par exemple "36:eb:b6:bf:ad:8a")
            const bssid = event.target.id;
      
              // Rechercher le réseau correspondant dans la liste
            const network = networkslist.find(net => net.bssid === bssid);
      
            if (network) {
                // Loguer les informations du réseau trouvé
                window.appapi.logreport(`Réseau selectioné pour éxécuter la commande aircrack\n : ${JSON.stringify(network, null, 2)}`);
            } else {
                window.appapi.logreport(`Réseau non trouvé pour le BSSID: ${bssid}`);
            }
        }
    });

    function displayNetworks() {
        // Crée un bouton pour chaque réseau wifi
        container.innerHTML = ''; // Efface les boutons précédents
        networkslist.forEach(networkslist => {
            const networkContainer = document.createElement('div');
            networkContainer.style.marginBottom = '10px';
            
            const infoButton = document.createElement('button');
            const simplifiedsecurity = networkslist.security.slice(0, 4);
            infoButton.textContent = `SSID: ${networkslist.ssid || 'Non Détecté'} \n Security: ${simplifiedsecurity} \n BSSID: ${networkslist.bssid}`;
            infoButton.id = networkslist.bssid;
            networkContainer.appendChild(infoButton);

            const deauthButton = document.createElement('button');
            deauthButton.textContent = 'Lancer DeAuth';
            deauthButton.style.backgroundColor = '#ff4444';
            deauthButton.addEventListener('click', () => {
                window.appapi.logreport(`Lancement DeAuth pour le réseau: ${networkslist.bssid}`);
                window.materialapi.deauthattack(networkslist.channel, networkslist.bssid, 500);
            });
            networkContainer.appendChild(deauthButton);

            const handshakeButton = document.createElement('button');
            handshakeButton.textContent = 'Capturer Handshake';
            handshakeButton.style.backgroundColor = '#44ff44';
            handshakeButton.addEventListener('click', () => {
                window.appapi.logreport(`Lancement capture handshake pour le réseau: ${networkslist.bssid}`);
                window.materialapi.startHandshakeCapture(networkslist.bssid, networkslist.channel);
            });
            networkContainer.appendChild(handshakeButton);

            container.appendChild(networkContainer);
        });
    };
  });
  