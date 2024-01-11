import argparse
import subprocess
import time 
from monitor import monitor_mode
from monitor import desactivate_monitor
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
    if monitor_mode(withoutmonitor):
        pass
    else:
        desactivate_monitor(withoutmonitor)
    main()
