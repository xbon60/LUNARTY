import iwlist
from config import withoutmonitor
networklist = []

def scan_wifi_networks(interface):
    # Exécute la commande iwlist pour scanner les réseaux WiFi
    content = iwlist.scan(interface=interface)
    cells = iwlist.parse(content)
    return cells






# Affichage des informations pour chaque réseau
def dumpnetwork():
    value = ""
    print("Fonction Initiée(Scan Reseau)")
    content = iwlist.scan(interface=withoutmonitor)
    cells = iwlist.parse(content)
    for cell in cells:
        mac_address = cell['mac']
        channel = cell['channel']
        essid = cell['essid']
        encryption = cell['encryption']
        value = value + (f"ESSID: {essid}\nMAC Address: {mac_address}\nChannel: {channel}\nSecurity: {encryption}\n\n")
        print(f"ESSID: {essid}\nMAC Address: {mac_address}\nChannel: {channel}\nSecurity: {encryption}\n")
    
    return(value)



if __name__ == "__main__":
    dumpnetwork()