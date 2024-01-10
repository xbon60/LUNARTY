import iwlist
content = iwlist.scan(interface='wlx0014d1a6e966')
cells = iwlist.parse(content)

# Affichage des informations pour chaque réseau
for cell in cells:
    mac_address = cell['mac']
    channel = cell['channel']
    essid = cell['essid']
    encryption = cell['encryption']

    print(f"ESSID: {essid}\nMAC Address: {mac_address}\nChannel: {channel}\nSecurity: {encryption}\n")

#channel, MAC ADDRESS NETWORK, BSSID, SSID, ENCYRPTION
