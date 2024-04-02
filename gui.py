from customtkinter import *
from monitor import *
from aircrack import *
from scanwifi import dumpwifi
from config import * 
custom_font = ("Arial", 10)
validationKeyBoardValue = []

#Zone Definition Bouton

def activermoniteur():
    global monitortext
    global withoutmonitor
    result = activate_monitor(withoutmonitor)
    monitortext.configure(text=result)

def desactivermoniteur():
    global withoutmonitor
    global monitortext
    result = desactivate_monitor(withoutmonitor)
    monitortext.configure(text=result)

listbuttonnet = None
from tkinter import Canvas, Scrollbar, Frame

def create_buttons_from_list():
    global listnet
    wifi_values, listnet=display_wifi_list_and_wifi_choice(withoutmonitor)

    global main_group
    global listbuttonnet
    numberrecord = 0
    del wifi_values[0]

    # Create a canvas and a scrollbar
    canvas = Canvas(main_group)
    scrollbar = Scrollbar(main_group, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Configure the canvas to scroll with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Pack the scrollbar and the canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="right", fill="both", expand=True)

    # Create the scrollable frame inside the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    for i, value in enumerate(wifi_values):
        row, col = divmod(i, 3)  # Calculate the current row and column
        numberrecord = numberrecord+1
        # Crée un bouton avec la valeur actuelle de la liste comme texte
        
        listbuttonnet = CTkButton(scrollable_frame, text=value, command=lambda val=value, num=numberrecord: functionwifilist(num-1))
        listbuttonnet.grid(row=row, column=col, padx=10, pady=5)  

def functionwifilist(datainput):
    selected_option = optionmenu.get()
    if selected_option == "Attaque Réseau Wifi":
        attacknetwork(listnet, datainput)
    else: 
        print("Option not implemented")


def activate_mainLabel():
    global MainLabel
    if MainLabel.winfo_ismapped():
       MainLabel.pack(fill=Y, ipady=0, padx=0,pady=10)

def resetMainLabel():
    global listbuttonnet
    if listbuttonnet is not None:
        if listbuttonnet.winfo_exists():
            print("check")
            listbuttonnet.destroy()

def create_popup():
    global fenetre
    fenetre.withdraw()
    popup = Toplevel()
    popup.title("Erreur")
    popup.geometry("800x480")
    label = CTkLabel(popup, text="Le programme a rencontré une erreur.")
    label.pack(pady=10)
    button = CTkButton(popup, text="Fermer", command=lambda: close_windows(fenetre, popup))
    button.pack()

def close_windows(parent, popup):
    parent.destroy()
    popup.destroy()

def initialisationprogramme():
    if check_interface_existence(withoutmonitor, card):
        desactivermoniteur()
        create_buttons_from_list()
    else: 
       create_popup()


# Création de la fenêtre principale
fenetre = CTk()
fenetre.title("PTT200")
fenetre.geometry("800x480")  # Taille de la fenêtre


#Zone Settings

monitor_group = CTkFrame(fenetre)
LabelMonitor = CTkLabel(monitor_group, text="Etat Mode Moniteur: ")
monitortext = CTkLabel(monitor_group, text="")

monitor_group.pack(fill=X, padx=10,pady=10)
LabelMonitor.pack(side=LEFT, ipady=0, padx=0,pady=10)
monitortext.pack(side=LEFT, ipady=0, padx=0,pady=10)


options_list = ["Attaque Reseau"]
#Menu Options Réglages 


# Set the default value of the variable 
optionmenu = CTkOptionMenu(monitor_group, values=["Attaque Réseau Wifi", "option 2"])
optionmenu.pack(side=RIGHT)

#Zone Principale

main_group = CTkFrame(fenetre)
main_group.pack(side=TOP, fill=BOTH, expand=True, ipady=0, padx=0,pady=10)
main_group.configure(fg_color='red')
main_group.pack_propagate(400)


# Lancement de la boucle principale de la fenêtre
fenetre.after(50, initialisationprogramme())

fenetre.mainloop()
