import argparse
import subprocess
from config import withoutmonitor

def check_interface_existence(interface):
    try:
        # Vérifie si l'interface existe en exécutant airmon-ng
        subprocess.run(["airmon-ng", "check", "kill"])
        subprocess.run(["airmon-ng", "start", interface], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def activate_monitor():
    if check_interface_existence(withoutmonitor):
        main()
    else:
        print(f"Interface {withoutmonitor} n'existe pas. Vérifiez votre configuration.")
        main()
    
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
    activate_monitor()

