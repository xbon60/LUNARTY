import subprocess

def run_airdump():
    # Exécuter airodump-ng et générer le fichier CSV
    subprocess.run(["airodump-ng", "--output-format", "csv", "-w", "wifilist", "wlan0"])

if __name__ == "__main__":
    run_airdump()

