import pywifi
import time

# Initialisez l'interface Wi-Fi
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]  # Utilisez la première interface Wi-Fi

# Fonction pour scanner les réseaux Wi-Fi à proximité
def scan_wifi():
    iface.scan()
    time.sleep(2)  # Attendez un moment pour que le scan soit complété
    scan_results = iface.scan_results()
    return scan_results

# Fonction pour afficher les réseaux Wi-Fi détectés
def display_wifi_networks(networks):
    print("Réseaux Wi-Fi à proximité :")
    for network in networks:
        print(f"SSID: {network.ssid}, Signal Strength: {network.signal}")

# Exécutez le script
if __name__ == "__main__":
    wifi_networks = scan_wifi()
    display_wifi_networks(wifi_networks)
