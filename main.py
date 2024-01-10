import argparse
import subprocess
import time 
from monitor import check_interface_existence
from config import withoutmonitor
from config import card


def main():
    parser = argparse.ArgumentParser(description='PTT2000 PROJECT V0.')

    # Ajoutez vos options ici
    parser.add_argument('-a', action='store_true', help='Scan Reseaux Wifi')
    parser.add_argument('-b', action='store_true', help='Utilitaire Aircrack-ng')
    # parser.add_argument('-b', type=str, help='Option B')

    args = parser.parse_args()

    if args.a:
        subprocess.run(["python3", "aircrackdump-ng.py"])

    if args.b:
    	subprocess.run(["python3", "aircrack-ng.py"])

if __name__ == "__main__":
    if check_interface_existence(withoutmonitor):
        monitor = False
    else:
        monitor = True
        result = subprocess.run(["sudo", "airmon-ng", "stop", card], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        time.sleep(5)
        print('Mode Moniteur Desactivé')
        
    
    subprocess.run(["sudo", "python3", "monitor.py", "-d"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    main()
