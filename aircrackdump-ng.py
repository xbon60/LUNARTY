import iwlist
from config import withoutmonitor
content = iwlist.scan(interface=withoutmonitor)
cells = iwlist.parse(content)

# Affichage des informations pour chaque réseau
for cell in cells:
    mac_address = cell['mac']
    channel = cell['channel']
    essid = cell['essid']
    encryption = cell['encryption']

    print(f"ESSID: {essid}\nMAC Address: {mac_address}\nChannel: {channel}\nSecurity: {encryption}\n")

#channel, MAC ADDRESS NETWORK, BSSID, SSID, ENCYRPTION
