import tkinter as tk
import subprocess

class WifiScanApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Scan WiFi")

        # Make the window fullscreen
        self.master.attributes('-fullscreen', True)

        self.create_widgets()

    def create_widgets(self):
        # Bouton pour le menu principal
        self.btn_menu_principal = tk.Button(self.master, text="Menu principal", command=self.open_main_menu)
        self.btn_menu_principal.grid(row=0, column=0, pady=10)

        # Bouton pour la liste des réseaux WiFi
        self.btn_scan_wifi = tk.Button(self.master, text="Liste des réseaux WiFi", command=self.scan_wifi_networks)
        self.btn_scan_wifi.grid(row=0, column=1, pady=10)

        # Text widget for displaying WiFi networks
        self.text_box = tk.Text(self.master, wrap=tk.WORD)
        self.text_box.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def open_main_menu(self):
        self.master.destroy()  # Ferme l'interface de scan WiFi
        subprocess.run(["python3", "main.py"])  # Ouvre l'interface principale

    def scan_wifi_networks(self):
        command = ["iwlist", "scan"]
        result = subprocess.run(command, capture_output=True, text=True)

        # Clear the existing text in the Text widget
        self.text_box.delete(1.0, tk.END)

        # Display the list of WiFi networks in the Text widget
        parsed_output = self.parse_wifi_output(result.stdout)
        self.display_colored_text(parsed_output)

    def parse_wifi_output(self, output):
        lines = output.split('\n')
        parsed_output = ""

        for line in lines:
            if "ESSID" in line:
                ssid = line.split(":")[1].strip()
                parsed_output += f"WiFi Network: {ssid}\n"
            elif "Signal level" in line:
                signal_strength = line.split("=")[1].split()[0]
                parsed_output += f"Signal Strength: {signal_strength}\n"
            elif "Encryption key" in line:
                encryption_status = "Encrypted" if "on" in line else "Open"
                parsed_output += f"Encryption: {encryption_status}\n"
            elif "Protocol:" in line:
                wifi_protocol = line.split(":")[1].strip()
                parsed_output += f"Protocol: {wifi_protocol}\n"
            elif "Frequency:" in line:
                frequency = line.split()[0].split(":")[1].strip()
                parsed_output += f"Frequency: {frequency}\n"
            elif "Address" in line:
                mac_address = line.split()[4]
                parsed_output += f"MAC Address: {mac_address}\n"

        return parsed_output

    def display_colored_text(self, text):
        self.text_box.tag_configure("ssid", foreground="blue")
        self.text_box.tag_configure("signal", foreground="green")
        self.text_box.tag_configure("encryption", foreground="purple")
        self.text_box.tag_configure("protocol", foreground="orange")  # Added color for Protocol
        self.text_box.tag_configure("frequency", foreground="red")  # Added color for Frequency
        self.text_box.tag_configure("mac", foreground="brown")

        lines = text.split('\n')

        row_index = 2  # Starting row for displaying networks

        for line in lines:
            if "WiFi Network:" in line:
                # Insert a newline before each network to separate them into blocks
                self.text_box.insert(tk.END, "\n")
                self.text_box.insert(tk.END, line + "\n", "ssid")

                # Add a button for each WiFi network in the same row
                ssid = line.split(":")[1].strip()
                btn_test = tk.Button(self.master, text="Test", command=lambda ssid=ssid: self.test_network(ssid))
                btn_test.grid(row=row_index, column=2, pady=5)

                row_index += 1

            elif "Signal Strength:" in line:
                self.text_box.insert(tk.END, line + "\n", "signal")
            elif "Encryption:" in line:
                self.text_box.insert(tk.END, line + "\n", "encryption")
            elif "Protocol:" in line:
                self.text_box.insert(tk.END, line + "\n", "protocol")  # Use the "protocol" tag
            elif "Frequency:" in line:
                self.text_box.insert(tk.END, line + "\n", "frequency")  # Use the "frequency" tag
            elif "MAC Address:" in line:
                self.text_box.insert(tk.END, line + "\n", "mac")
            else:
                self.text_box.insert(tk.END, line + "\n")

    def test_network(self, ssid):
        # Function to execute aircrack-ng help for the selected WiFi network
        subprocess.run(["aircrack-ng", "--help"])
        print(f"Testing network: {ssid}")

# Crée l'application Tkinter pour wifiscan.py
root = tk.Tk()
app = WifiScanApp(root)
root.mainloop()

