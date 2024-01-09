import tkinter as tk
from tkinter import messagebox
import subprocess

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu Principal")
        self.master.attributes('-fullscreen', True)  # Met en plein écran

        # Crée un cadre pour le menu principal
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Boutons dans le menu principal
        self.btn_exit = tk.Button(self.main_frame, text="Exit", command=self.exit_app)
        self.btn_exit.pack(pady=10)
        
        self.btn_scan_wifi = tk.Button(self.main_frame, text="Scan réseau Wifi", command=self.show_wifi_scan)
        self.btn_scan_wifi.pack(pady=10)

    def exit_app(self):
        self.master.destroy()

    def show_wifi_scan(self):
        # Lance l'interface de scan WiFi depuis wifiscan.py
        self.master.destroy()  # Ferme l'écran principal
        subprocess.run(["python3", "wifiscan.py"])

# Crée l'application Tkinter pour main.py
root = tk.Tk()
app = MainApp(root)
root.mainloop()

