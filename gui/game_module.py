
from tkinter import *
import time
import global_systems
import playerClass

def SetGamePlayers(number_of_players, window):
    window.destroy()
    
    for i in range (number_of_players):   
        InputWindow(i+1)

###########################################################################################
###########################################################################################
def ChoosePlayer(playerindex):

    player_variables = {
        "is_running" : True,
        "character_index" : 0,
        "team": global_systems.equipoA
    }
    
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Configuración de Juego")
    window.configure(bg="#262626")
    #print("player configured")

    def stop():
        # Falta setPersonaje
        player_variables["is_running"] = False
        print("done")
        window.destroy()


    def changeTeam(index):
        if index == 0:
            player_variables["team"] = global_systems.equipoA

        elif index == 1:
            player_variables["team"] = global_systems.equipoB
        
        elif index == 2:
            player_variables["team"] = global_systems.equipoC

    
    TeamAImage = PhotoImage(file = "images/equipo01/escudo.png")
    TeamBImage = PhotoImage(file = "images/equipo02/escudo.png")
    TeamCImage = PhotoImage(file = "images/equipo03/escudo.png")


    ButtonTeamA = Button(window, image=TeamAImage, width=150, height=150, command= lambda: changeTeam(0))
    ButtonTeamA.place(relx=0.25, rely=0.8, anchor="center")

    ButtonTeamB = Button(window, image=TeamBImage, width=150, height=150, command= lambda: changeTeam(1))
    ButtonTeamB.place(relx=0.5, rely=0.8, anchor="center")

    ButtonTeamC = Button(window, image=TeamCImage, width=150, height=150, command= lambda: changeTeam(2))
    ButtonTeamC.place(relx=0.75, rely=0.8, anchor="center")

    ButtonConfirm = Button(window, text="Confirmar", width=30, height=2, command = stop)
    ButtonConfirm.place(relx=0.5, rely=0.6, anchor="center") 

    nameLabel = Label(window, text ="")
    nameLabel.place(relx=0.5, rely=0.5, anchor="center")

    playerLabel = Label(window, text=f"{global_systems.Players[playerindex].getName()} Escoja su personaje")
    playerLabel.place(relx=0.5, rely=0.1, anchor="center")
    
    
    
    def player_selection():

        while player_variables["is_running"]:
            
            equipo = player_variables["team"]
            #characterImage = PhotoImage(file = global_systems.equipoA[player_variables['character_index']][1])
            characterImage = PhotoImage(file = equipo[player_variables['character_index']][1])
            #print(global_systems.equipoA[player_variables['character_index']][1])
            canvas.itemconfig(character, image = characterImage)
            nameLabel['text'] = f"{equipo[player_variables['character_index']][0]}"
            
            
            
            window.update()
            time.sleep(0.016)

    canvas = Canvas(window, width=150, height=150)
    canvas.place(relx=0.5, rely=0.3, anchor="center")

    #characterImage = PhotoImage(file = f"{global_systems.equipoA[player_variables["character_index"]][1]}")
    character = canvas.create_image(0,0, anchor="nw")#, image = characterImage)

    def change(value):
        player_variables["character_index"] = int(value)

    def potenciometro():

        extra_window = Tk()
        extra_window.title('señal')
        extra_window.geometry('300x300')

        #Slider
        poten = Scale(extra_window, from_= 0, to= 2, command= lambda value: change(value))
        poten.pack(fill='both', expand= True)

    
    potenciometro()
    player_selection()
    
    
    
    window.mainloop()
###########################################################################################
###########################################################################################



def Confirm(window, entry, jugador):
    player = playerClass.Player(entry.get())
    global_systems.Players.append(player)
    window.destroy()
    ChoosePlayer(jugador-1)



def InputWindow(jugador):
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Nombre")

    window.configure(bg="#262626")

    NameLabel = Label(window, text = f"Jugador {jugador} ingrese su nombre")
    NameLabel.place(relx=0.5, rely=0.4, anchor="center")

    NameEntry = Entry(window)
    NameEntry.place(relx=0.5, rely=0.5, anchor="center")

    ButtonConfirm = Button(window, text="Confirmar", width=30, height=2, command= lambda: Confirm(window, NameEntry, jugador))
    ButtonConfirm.place(relx=0.5, rely=0.6, anchor="center")



    window.mainloop()



# Esta es la ventana de configuración
##################################################################################
def GameConfigWindow(OpenMain):
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Configuración de Juego")
    window.configure(bg="#262626")

    CantidadJugadores = Label(window, text="Cuantos Jugadores?")
    CantidadJugadores.place(relx=0.5, rely=0.2)
    
    ButtonSingle = Button(window, text="Un Jugador", width=30, height=2, command= lambda: SetGamePlayers(1, window))
    ButtonSingle.place(relx=0.5, rely=0.3, anchor="center")

    ButtonTwo = Button(window, text="Dos Jugadores", width=30, height=2, command= lambda: SetGamePlayers(2, window))
    ButtonTwo.place(relx=0.5, rely=0.35, anchor="center")

    ButtonThree = Button(window, text="Tres Jugadores", width=30, height=2, command= lambda: SetGamePlayers(3, window))
    ButtonThree.place(relx=0.5, rely=0.4, anchor="center")
    
    
    ButtonReturn = Button(window, text="Regresar", width=30, height=2, command= lambda: OpenMain(window))
    ButtonReturn.place(relx=0.2, rely=0.9, anchor="center")

    
    
    # Control de música
    #play_button = Button(window, text="Reproducir Música", width=30, height=2, command=play)
    #play_button.place(relx=0.5, rely=0.3, anchor="center")

    #stop_button = Button(window, text="Detener Música", width=30, height=2, command=stop)
    #stop_button.place(relx=0.5, rely=0.5, anchor="center")



    window.mainloop()
##################################################################################