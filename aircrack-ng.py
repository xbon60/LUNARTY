import subprocess
import iwlist

def scan_wifi_networks(interface):
    # Exécute la commande iwlist pour scanner les réseaux WiFi
    content = iwlist.scan(interface=interface)
    cells = iwlist.parse(content)
    return cells

def display_wifi_list_and_wifi_choice():
    # Scanne les réseaux WiFi
    interface = 'wlx0014d1a6e966'
    wifi_networks = scan_wifi_networks(interface)

    # Affichage des informations pour chaque réseau avec un numéro associé
    for i, cell in enumerate(wifi_networks, 1):
        mac_address = cell['mac']
        channel = cell['channel']
        essid = cell['essid']
        encryption = cell['encryption']

        print(f"{i}. ESSID: {essid}, MAC Address: {mac_address}, Channel: {channel}, Security: {encryption}")

    # Demande à l'utilisateur de choisir un réseau
    selected_index = int(input("Choisissez le numéro du réseau que vous souhaitez sélectionner: ")) - 1

    # Vérifie que l'index sélectionné est valide
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
        execute_aircrack(selected_cell)
    else:
        print("Index non valide. Veuillez sélectionner un numéro de réseau valide.")

def execute_aircrack(selected_cell, worldlist_path='worldlist.txt', capture_file='cap.cap'):
    # Récupère les informations nécessaires du réseau sélectionné
    bssid = selected_cell['mac']

    # Construit la commande Aircrack-ng
    aircrack_command = ['aircrack-ng', '-w', worldlist_path, '-b', bssid, capture_file]

    try:
        # Exécute la commande Aircrack-ng en tant que processus externe
        result = subprocess.run(aircrack_command, capture_output=True, text=True, check=True)

        # Affiche la sortie de la commande
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Gère les erreurs lors de l'exécution de la commande
        print(f"Erreur lors de l'exécution de la commande Aircrack-ng : {e.stderr}")

if __name__ == "__main__":
    # Appelle la fonction pour afficher la liste des réseaux et demander à l'utilisateur de choisir
    display_wifi_list_and_wifi_choice()

