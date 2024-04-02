import wifi
import time
from config import *

def scan_wifi(show_networks_without_essid=False):
    networks = wifi.Cell.all(withoutmonitor)
    valueinlist = [""]
    wifi_list = []
    for cell in networks:
        mac_address = cell.address
        channel = cell.channel
        essid = cell.ssid
        encryption = cell.encryption_type
        frequency = cell.frequency

        # Skip networks without ESSID if show_networks_without_essid is False
        if not essid and not show_networks_without_essid:
            continue

        value = f"ESSID: {essid}\nMAC Address: {mac_address}\nChannel: {channel}\nFrequency: {frequency}\nSecurity: {encryption}\n\n"
        
        wifi_list.append(value)

    return wifi_list

def dumpwifi():
    value = ""
    print()
    wifi_networks = scan_wifi()
    for network in wifi_networks:
        value = value + (network)

    print(wifi_networks)
    return value, wifi_networks



# Exemple d'utilisation
#wifi_networks = scan_wifi()
#print(wifi_networks)
#for network in wifi_networks:
#    print(network)