import iwlist
content = iwlist.scan(interface='wlx0014d1a6e966')
cells = iwlist.parse(content)

def display_wifi_list_and_wifi_choice(cells):
    # Affichage des informations pour chaque réseau avec un numéro associé
    for i, cell in enumerate(cells, 1):
        mac_address = cell['mac']
        channel = cell['channel']
        essid = cell['essid']
        encryption = cell['encryption']

        print(f"{i}. ESSID: {essid}, MAC Address: {mac_address}, Channel: {channel}, Security: {encryption}")

    # Demande à l'utilisateur de choisir un réseau
    selected_index = int(input("Choisissez le numéro du réseau que vous souhaitez sélectionner: ")) - 1

    # Vérifie que l'index sélectionné est valide
    if 0 <= selected_index < len(cells):
        selected_cell = cells[selected_index]

        # Stocke les valeurs du réseau sélectionné dans des variables
        machinal = selected_cell['mac']
        essaifinal = selected_cell['essid']
        encryptionfinal = selected_cell['encryption']
        channel_final = selected_cell['channel']

        # Utilise les valeurs sélectionnées comme nécessaire dans le reste du code
        print(f"Vous avez sélectionné le réseau :\nESSID: {essaifinal}\nMAC Address: {machinal}\nChannel: {channel_final}\nSecurity: {encryptionfinal}")
        
        # Ajoute ici le reste du code que vous souhaitez exécuter avec les valeurs sélectionnées
    else:
        print("Index non valide. Veuillez sélectionner un numéro de réseau valide.")

