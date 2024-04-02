from customtkinter import *
from monitor import *
from aircrack import *
from scanwifi import dumpwifi
from config import * 
custom_font = ("Arial", 10)
validationKeyBoardValue = []
keyboardpanel=["","1","2","3","4","5","6","7","8","9","0"]
keyboardpress=[]
#Zone Definition Bouton

def boutonactivermoniteur():
    global monitortext
    global withoutmonitor
    result = activate_monitor(withoutmonitor)
    monitortext.configure(text=result)

def boutondesactivermoniteur():
    global withoutmonitor
    global monitortext
    result = desactivate_monitor(withoutmonitor)
    monitortext.configure(text=result)

def boutonoption1():
    global MainLabel
    resetMainLabel()
    MainLabel.pack(side=LEFT, fill=Y, ipady=0, padx=0,pady=10)
    result = dumpwifi()
    MainLabel.configure(state='normal')
    MainLabel.delete("1.0", END)  # Supprime tout le contenu actuel
    MainLabel.insert(END, result)  # Insère le nouveau texte à la fin
    MainLabel.configure(state='disabled')


def boutonoption2():
    resetMainLabel()
    global MainLabel
    MainLabel.pack_forget()
    global listnet
    value, listnet=display_wifi_list_and_wifi_choice(withoutmonitor)

    create_buttons_from_list(value)
    
    
listbuttonnet = None
def create_buttons_from_list(wifi_values):
    global main_group
    global listbuttonnet
    numberrecord = 0
    print(wifi_values)
    del wifi_values[0]
    for value in wifi_values:
        numberrecord = numberrecord+1
        # Crée un bouton avec la valeur actuelle de la liste comme texte
        print(numberrecord)
        listbuttonnet = CTkButton(main_group, text=value, command=lambda val=value, num=numberrecord: functionwifilist(num-1))
        listbuttonnet.pack()

def functionwifilist(datainput):
    attacknetwork(listnet, datainput)

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
    label = Label(popup, text="Le programme a rencontré une erreur.")
    label.pack(pady=10)
    button = CTkButton(popup, text="Fermer", command=lambda: close_windows(fenetre, popup))
    button.pack()

def close_windows(parent, popup):
    parent.destroy()
    popup.destroy()

def initialisationprogramme():
    if check_interface_existence(withoutmonitor, card):
        boutondesactivermoniteur()
    #else: 
     #   create_popup()


# Création de la fenêtre principale
fenetre = CTk()
fenetre.title("PTT200")
fenetre.geometry("800x480")  # Taille de la fenêtre
#fenetre.overrideredirect(True)

#Zone Mode Bouton et Etat Mode Moniteur

monitor_group = CTkFrame(fenetre)
LabelMonitor = CTkLabel(monitor_group, text="Etat Mode Moniteur: ")
monitortext = CTkLabel(monitor_group, text="")
bouton1 = CTkButton(monitor_group, text="Activer Moniteur", width=13, height=1,font=custom_font, command= lambda: boutonactivermoniteur())
bouton2 = CTkButton(monitor_group, text="Desactiver Moniteur", width=13, height=1,font=custom_font,  command= lambda: boutondesactivermoniteur())
monitor_group.pack(fill=X, padx=10,pady=10)
LabelMonitor.pack(side=LEFT, ipady=0, padx=0,pady=10)
monitortext.pack(side=LEFT, ipady=0, padx=0,pady=10)
bouton1.pack(side=RIGHT, ipady=0, padx=10,pady=10)
bouton2.pack(side=RIGHT, ipady=0, padx=10,pady=10)

#Zone Options 
option_group = CTkFrame(fenetre)
Labeloption = CTkLabel(monitor_group, text="Options Disponibles ")
option1 = CTkButton(option_group, text="Scan Reseau Wifi", width=13, height=1,font=custom_font, command= lambda: boutonoption1())
option2 = CTkButton(option_group, text="Attaque Reseau", width=13, height=1,font=custom_font, command= lambda: boutonoption2())
option_group.pack(side=LEFT, fill=Y, padx=10,pady=10)
option1.pack(side=TOP, ipady=0, padx=10,pady=10)
option2.pack(side=TOP, ipady=0, padx=10,pady=10)


#Zone Principale

main_group = CTkFrame(fenetre)
scrollbar = CTkScrollableFrame(main_group, width=200, height=200)
main_group.pack(side=RIGHT, fill=Y, ipady=0, padx=0,pady=10)
main_group.pack_propagate(400)
MainLabel = CTkTextbox(main_group)
MainLabel.configure(state='disabled')

# Lancement de la boucle principale de la fenêtre
fenetre.after(50, initialisationprogramme())

fenetre.mainloop()
