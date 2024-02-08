import pandas as pd

def extract_station_mac(csv_file, selected_bssid):
    # Charge le fichier CSV en tant que dataframe pandas
    df = pd.read_csv(csv_file, skiprows=4)  # Ignorer les 4 premières lignes du fichier

    # Assurez-vous que les noms de colonnes utilisés correspondent exactement aux noms réels
    relevant_columns = ['Station MAC', ' BSSID']  # Ajoutez l'espace au début de ' BSSID'

    # Sélectionne uniquement les colonnes pertinentes
    df = df[relevant_columns]

    # Retirer les espaces au début des adresses MAC
    df[' BSSID'] = df[' BSSID'].str.strip()

    # Filtre les lignes pour le BSSID spécifié
    filtered_rows = df[df[' BSSID'] == selected_bssid]

    if not filtered_rows.empty:
        # Récupère l'adresse MAC de la station associée au BSSID spécifié
        station_mac = filtered_rows.iloc[0]['Station MAC']
        return station_mac
    else:
        print(f"Aucune station MAC trouvée pour le BSSID {selected_bssid}")
        return None

# Exemple d'utilisation
csv_file_path = 'airdumpfile/airdump-01.csv'
selected_bssid = '66:4E:17:0E:A8:8C'

result = extract_station_mac(csv_file_path, selected_bssid)

if result:
    print(f"L'adresse de la station MAC associée au BSSID {selected_bssid} est : {result}")

