import wifi
import time
from config import *
def scan_wifi():
    networks = wifi.Cell.all(withoutmonitor)
    print(networks)
    #time.sleep(10)

    wifi_list = []
    for cell in networks:
        mac_address = cell.ssid
        channel = cell.channel
        essid = cell.ssid
        encryption = cell.encryption_type
        frequency = cell.frequency
        value = f"ESSID: {essid}\nMAC Address: {mac_address}\nChannel: {channel}\nFrequency: {frequency}\nSecurity: {encryption}\n\n"
        wifi_list.append(value)

    return wifi_list


def dumpwifi():
    value = ""
    wifi_networks = scan_wifi()
    for network in wifi_networks:
        value = value + (network)

    
    return value




# Exemple d'utilisation
#wifi_networks = scan_wifi()
#print(wifi_networks)
#for network in wifi_networks:
#    print(network)