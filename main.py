import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description='PTT2000 PROJECT V0.')

    # Ajoutez vos options ici
    parser.add_argument('-a', action='store_true', help='voir les reseau wifi et leurs informations')
    parser.add_argument('-b', action='store_true', help='Utilitaire Aircrack-ng')
    # parser.add_argument('-b', type=str, help='Option B')

    args = parser.parse_args()

    if args.a:
        subprocess.run(["python3", "aircrackdump-ng.py"])

    if args.b:
    	subprocess.run(["python3", "aircrack-ng.py"])

if __name__ == "__main__":
    main()
