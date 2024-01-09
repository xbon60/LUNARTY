import csv
import subprocess

def display_wifi_list():
    # Lire le fichier CSV généré par airodump-ng
    with open('wifilist-01.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for index, row in enumerate(reader, 1):
            print(f"{index}. BSSID: {row[0]}, ESSID: {row[13]}")

def execute_aircrack(network_index):
    # Exécuter aircrack-ng sur le réseau sélectionné
    subprocess.run(["aircrack-ng", "-b", f"{network_index}", "-w", "wordlist.txt", "captured_data.cap"])

if __name__ == "__main__":
    # Exécute d'abord airdump.py pour générer le fichier CSV
    subprocess.run(["python3", "airdump.py"])

    # Affiche la liste des réseaux et demande à l'utilisateur de choisir
    display_wifi_list()
    network_index = int(input("Choisissez le réseau en entrant son numéro : "))

    # Exécute aircrack-ng sur le réseau choisi
    execute_aircrack(network_index)

