import subprocess
import iwlist
import psutil
import argparse
from config import withoutmonitor
from config import card


def main(withoutmonitor, card):
    parser = argparse.ArgumentParser(description='PTT2000 PROJECT V0.')

    # Ajoutez vos options ici
    parser.add_argument('-a', action='store_true', help='Activé Mode Moniteur')
    parser.add_argument('-d', action='store_true', help='Desactivé Mode Moniteur')
    parser.add_argument('-v', action='store_true', help='Verifier ETAT Mode Moniteur')
    
    args = parser.parse_args()

    if args.a:
        activate_monitor(withoutmonitor)

    if args.d:
        desactivate_monitor(withoutmonitor)
        
    if args.v:
        verification_monitor_mode(withoutmonitor)


def check_interface_existence(withoutmonitor, card):
    # Obtient la liste des interfaces réseau
    network_interfaces = psutil.net_if_addrs()

    # Vérifie si l'interface withoutmonitor existe dans la liste
    if withoutmonitor not in network_interfaces:
    # Vérifie si l'interface card existe dans la liste
        if card not in network_interfaces:
            return False

    return True
    

def monitor_mode(withoutmonitor):
     # Obtient la liste des interfaces réseau
    network_interfaces = psutil.net_if_addrs()

    # Vérifie si l'interface spécifiée existe dans la liste
    if withoutmonitor in network_interfaces:
        return True
    else:
        return False


def activate_monitor(withoutmonitor):
    if monitor_mode(withoutmonitor):
        result = subprocess.run(["sudo", "airmon-ng", "start", withoutmonitor], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print('Mode Moniteur Actif')
    else:
        print('Mode Moniteur Deja Actif')
        

def desactivate_monitor(withoutmonitor):
    if monitor_mode(withoutmonitor):
        print('Mode Moniteur Deja Desactivé')
    else:
        result = subprocess.run(["sudo", "airmon-ng", "stop", card], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print('Mode Moniteur Désactivé')
        

def verification_monitor_mode(withoutmonitor):
    if monitor_mode(withoutmonitor):
        print('True')
    else:
        print('False')
        

if __name__ == "__main__":
    if check_interface_existence(withoutmonitor, card):
        main(withoutmonitor, card)
    else : 
        print("erreur carte Reseaux")

