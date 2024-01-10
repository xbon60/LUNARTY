import subprocess
import iwlist
from config import withoutmonitor
from config import card
import psutil
import argparse
def check_interface_existence(withoutmonitor):
    # Obtient la liste des interfaces réseau
    network_interfaces = psutil.net_if_addrs()

    # Vérifie si l'interface spécifiée existe dans la liste
    if withoutmonitor in network_interfaces:
        return True
    else:
        return False
        

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
    	desactivate_monitor(card)
    if args.v:
        verification_monitor_mode()
    	
def activate_monitor(withoutmonitor):
    if check_interface_existence(withoutmonitor):
        monitor = False
        result = subprocess.run(["sudo", "airmon-ng", "start", withoutmonitor], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        #print(result.stdout) 
        print('Mode Moniteur Actif')
    else:
        monitor = True
        print('Mode Moniteur Actif')


def desactivate_monitor(card):
    if check_interface_existence(withoutmonitor):
        monitor = False
        print('Mode Moniteur Desactivé')
    else:
        monitor = True
        result = subprocess.run(["sudo", "airmon-ng", "stop", card], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        #print(result.stdout) 
        print('Mode Moniteur Desactivé')
        
def verification_monitor_mode():
    if check_interface_existence(withoutmonitor):
        monitor = False
        print('True')
    else:
        monitor = True
        print('False')
        
if __name__ == "__main__":
    main(withoutmonitor,card)

