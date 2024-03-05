from tkinter import *
from monitor import *
from aircrack import *
from aircrackdump import *
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
    monitortext.config(text=result)

def boutondesactivermoniteur():
    global withoutmonitor
    global monitortext
    result = desactivate_monitor(withoutmonitor)
    monitortext.config(text=result)

def boutonoption1():
    global MainLabel
    global scrollbar
    resetMainLabel()
    MainLabel.pack(side=LEFT, fill=Y, ipady=0, padx=0,pady=10)
    scrollbar.config(command=MainLabel.yview)
    result = dumpnetwork()
    MainLabel.config(state='normal')
    MainLabel.delete("1.0", END)  # Supprime tout le contenu actuel
    MainLabel.insert(END, result)  # Insère le nouveau texte à la fin
    MainLabel.config(state='disabled')


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
    del wifi_values[0]
    print(wifi_values)
    for value in wifi_values:
        numberrecord = numberrecord+1
        # Crée un bouton avec la valeur actuelle de la liste comme texte
        print(numberrecord)
        listbuttonnet = Button(main_group, text=value, command=lambda val=value, num=numberrecord: functionwifilist(num-1))
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
            listbuttonnet.destroy()



def create_popup():
    global fenetre
    fenetre.withdraw()
    popup = Toplevel()
    popup.title("Erreur")
    popup.geometry("800x480")
    label = Label(popup, text="Le programme a rencontré une erreur.")
    label.pack(pady=10)
    button = Button(popup, text="Fermer", command=lambda: close_windows(fenetre, popup))
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
fenetre = Tk()
fenetre.title("PTT200")
fenetre.geometry("800x480")  # Taille de la fenêtre
#fenetre.overrideredirect(True)

#Zone Mode Bouton et Etat Mode Moniteur

monitor_group = Frame(fenetre)
LabelMonitor = Label(monitor_group, text="Etat Mode Moniteur: ")
monitortext = Label(monitor_group, text="")
bouton1 = Button(monitor_group, text="Activer Moniteur", width=13, height=1,font=custom_font, command= lambda: boutonactivermoniteur())
bouton2 = Button(monitor_group, text="Desactiver Moniteur", width=13, height=1,font=custom_font,  command= lambda: boutondesactivermoniteur())
monitor_group.pack(fill=X, padx=10,pady=10)
LabelMonitor.pack(side=LEFT, ipady=0, padx=0,pady=10)
monitortext.pack(side=LEFT, ipady=0, padx=0,pady=10)
bouton1.pack(side=RIGHT, ipady=0, padx=10,pady=10)
bouton2.pack(side=RIGHT, ipady=0, padx=10,pady=10)

#Zone Options 
option_group = Frame(fenetre, bg="#777777")
Labeloption = Label(monitor_group, text="Options Disponibles ")
option1 = Button(option_group, text="Scan Reseau Wifi", width=13, height=1,font=custom_font, command= lambda: boutonoption1())
option2 = Button(option_group, text="Attaque Reseau", width=13, height=1,font=custom_font, command= lambda: boutonoption2())
option_group.pack(side=LEFT, fill=Y, padx=10,pady=10)
option1.pack(side=TOP, ipady=0, padx=10,pady=10)
option2.pack(side=TOP, ipady=0, padx=10,pady=10)


#Zone Principale

main_group = Frame(fenetre, bg="#777777")
scrollbar = Scrollbar(main_group, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)
main_group.pack(side=RIGHT, fill=Y, ipady=0, padx=0,pady=10)
main_group.pack_propagate(400)
MainLabel = Text(main_group)
MainLabel.config(state='disabled')

# Lancement de la boucle principale de la fenêtre
fenetre.after(50, initialisationprogramme())

fenetre.mainloop()
