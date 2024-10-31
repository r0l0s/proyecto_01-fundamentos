
from tkinter import *
import time
import global_systems
import playerClass
import socket
import random
import threading
import pygame

pygame.mixer.init()

serverAddress = ('192.168.100.78', 2222)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def SetGamePlayers(number_of_players, window):
    window.destroy()
    for i in range (number_of_players):   
        InputWindow(i+1)
    SummaryWindow()
    

def MakeImage(path):
    return PhotoImage(file = path)


def StartCoin(window):
    window.destroy()
    CoinWindow()
    
def StartGame(window):
    window.destroy()
    game()

def StartEnd(window):
    window.destroy()
    endScreen()
    

###########################################################################################
###########################################################################################
def ChoosePlayer(playerindex):


    player_variables = {
        "is_running" : True,
        "character_index" : 0,
        "team": global_systems.equipoA,
        "character_name": None,
        "character_image": None,
        "character_team" : None,
    }
    
    def UpdateInfo():
        player_variables["character_name"] = player_variables["team"][player_variables["character_index"]][0]
        player_variables["character_image"] = player_variables["team"][player_variables["character_index"]][1]
        player_variables["character_team"] = player_variables["team"][player_variables["character_index"]][2]


    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Configuración de Juego")
    window.configure(bg="#262626")

    def stop():
        player_variables["is_running"] = False
        global_systems.Players[playerindex].setCharacter(player_variables["character_name"], player_variables["character_image"], player_variables["character_team"])
        print("player configured")
        print(global_systems.Players[playerindex].getCharacter("all"))
        window.destroy()


    def changeTeam(index):
        if index == 0:
            player_variables["team"] = global_systems.equipoA
        elif index == 1:
            player_variables["team"] = global_systems.equipoB       
        elif index == 2:
            player_variables["team"] = global_systems.equipoC
            

    TeamAImage = MakeImage("images/equipo01/escudo.png")
    TeamBImage = MakeImage("images/equipo02/escudo.png")
    TeamCImage = MakeImage("images/equipo03/escudo.png")


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

    playerLabel = Label(window, text=f"{global_systems.Players[playerindex].getPlayerName()} Escoja su personaje")
    playerLabel.place(relx=0.5, rely=0.1, anchor="center")
    
    
    
    def player_selection():

        

        while player_variables["is_running"]:

            command = "sendPot"
            commandEncoded = command.encode('utf-8')
            UDPClient.sendto(commandEncoded, serverAddress)

            data,address = UDPClient.recvfrom(bufferSize)
            dataDecoded = data.decode('utf-8')
            player_variables["character_index"] = int(dataDecoded)
            print(dataDecoded)

            UpdateInfo()

            characterImage = MakeImage(player_variables["character_image"])
            canvas.itemconfig(character, image = characterImage)
            nameLabel['text'] = f"{player_variables["character_name"]}"
            
            window.update()
            time.sleep(0.06)

    canvas = Canvas(window, width=150, height=150)
    canvas.place(relx=0.5, rely=0.3, anchor="center")
    character = canvas.create_image(0,0, anchor="nw")

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
    CantidadJugadores.place(relx=0.5, rely=0.2, anchor="center")
    
    ButtonSingle = Button(window, text="Un Jugador", width=30, height=2, command= lambda: SetGamePlayers(1, window))
    ButtonSingle.place(relx=0.5, rely=0.3, anchor="center")

    ButtonTwo = Button(window, text="Dos Jugadores", width=30, height=2, command= lambda: SetGamePlayers(2, window))
    ButtonTwo.place(relx=0.5, rely=0.4, anchor="center")

    ################################################################################################################

    FormaCambio = Label(window, text="Forma de intercambio:")
    FormaCambio.place(relx=0.5, rely=0.5, anchor="center")

    ButtonAuto = Button(window, text="Automática", width=30, height=2, command= lambda: global_systems.changeSwitchForm("auto"))
    ButtonAuto.place(relx=0.5, rely=0.6, anchor="center")

    ButtonManual = Button(window, text="Manual", width=30, height=2, command= lambda: global_systems.changeSwitchForm("manual"))
    ButtonManual.place(relx=0.5, rely=0.7, anchor="center")

    
    ButtonReturn = Button(window, text="Regresar", width=30, height=2, command= lambda: OpenMain(window))
    ButtonReturn.place(relx=0.2, rely=0.9, anchor="center")

    window.mainloop()
##################################################################################


def SummaryWindow():
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Resumen de configuración")
    window.configure(bg="#262626")


    if len(global_systems.Players) == 1:

        playerName = global_systems.Players[0].getPlayerName()

        characterTeam = MakeImage(global_systems.Players[0].getCharacter("team"))
        characterImage = MakeImage(global_systems.Players[0].getCharacter("image"))

        
        Label(window, image=characterImage, width=150, height=150).place(relx=0.5, rely=0.5, anchor="center")
        Label(window, image=characterTeam, width=150, height=150).place(relx=0.5, rely=0.2, anchor="center")
        Label(window, text=f"Jugador: {playerName}").place(relx=0.5, rely=0.7, anchor="center")

    elif len(global_systems.Players) == 2:

        playerA_Name = global_systems.Players[0].getPlayerName()

        characterA_Team = MakeImage(global_systems.Players[0].getCharacter("team"))
        characterA_Image = MakeImage(global_systems.Players[0].getCharacter("image"))

        
        Label(window, image=characterA_Image, width=150, height=150).place(relx=0.25, rely=0.5, anchor="center")
        Label(window, image=characterA_Team, width=150, height=150).place(relx=0.25, rely=0.2, anchor="center")
        Label(window, text=f"Jugador: {playerA_Name}").place(relx=0.25, rely=0.7, anchor="center")


        playerB_Name = global_systems.Players[1].getPlayerName()

        characterB_Team = MakeImage(global_systems.Players[1].getCharacter("team"))
        characterB_Image = MakeImage(global_systems.Players[1].getCharacter("image"))

        
        Label(window, image=characterB_Image, width=150, height=150).place(relx=0.75, rely=0.5, anchor="center")
        Label(window, image=characterB_Team, width=150, height=150).place(relx=0.75, rely=0.2, anchor="center")
        Label(window, text=f"Jugador: {playerB_Name}").place(relx=0.75, rely=0.7, anchor="center")

        vsIcon = MakeImage("images/vs.png")
        Label(window, image=vsIcon, width=150, height=150).place(relx=0.5, rely=0.5, anchor="center")

    def vsSFX():
        global_systems.backgroundMusic.setVolume(0.0)
        effect = pygame.mixer.Sound("music/vs.mp3")
        effect.set_volume(1)
        effect.play()
        time.sleep(5)
        global_systems.backgroundMusic.setVolume(0.2)

    
    vs_sfx = threading.Thread(target=vsSFX)
    vs_sfx.daemon = True
    vs_sfx.start()


    ButtonListo = Button(window, text="Listo", width=30, height=2, command= lambda: StartCoin(window))
    ButtonListo.place(relx=0.2, rely=0.9, anchor="center")

    window.mainloop()


##################################################################################
##################################################################################
def CoinWindow():
    
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Selección Aleatoria")
    window.configure(bg="#262626")

    info = {
        "character" : None,
        "name" : None
    }


    def animacion(index):
        
        while index < 147:
            moneda = MakeImage(f"images/coin/{index}.png")
            canvas.itemconfig(coin, image = moneda)
            index += 1
            time.sleep(0.05)
            window.update()
        
        selection = random.randint(0,1)
        global_systems.startingPlayer = selection
        selected = MakeImage(global_systems.Players[selection].getCharacter("image"))
        info["character"] = selected
        Label(window, image=selected, width=150, height=150).place(relx=0.5, rely=0.3, anchor="center")
        Label(window, text=f"Empieza: {global_systems.Players[selection].getPlayerName()}").place(relx=0.5, rely=0.5, anchor="center")
        Button(window, text="Jugar", width=30, height=2, command= lambda: StartGame(window)).place(relx=0.5, rely=0.9, anchor="center")

        global_systems.otherGuy = global_systems.OtherPlayer(global_systems.startingPlayer)

        chosen_sfx = threading.Thread(target=chosenSFX)
        chosen_sfx.daemon = True
        chosen_sfx.start()

        window.update()
            
    canvas = Canvas(window, width=400, height=307, bg="#262626")
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    coin = canvas.create_image(0,0, anchor="nw", image= info["character"])

    def chosenSFX():
        global_systems.backgroundMusic.setVolume(0.0)
        effect = pygame.mixer.Sound("music/choosen.mp3")
        effect.set_volume(1)
        effect.play()
        time.sleep(5)
        global_systems.backgroundMusic.setVolume(0.2)


    def monedaSFX():
        global_systems.backgroundMusic.setVolume(0.0)
        effect = pygame.mixer.Sound("music/moneda.mp3")
        effect.set_volume(1)
        effect.play()
        time.sleep(5)
        global_systems.backgroundMusic.setVolume(0.2)


    moneda_sfx = threading.Thread(target=monedaSFX)
    moneda_sfx.daemon = True
    moneda_sfx.start()

    
    animacion(1)
    window.mainloop()
##################################################################################
##################################################################################

def game():

    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Juego")
    window.configure(bg="#262626")

    firstTurnPlayer = global_systems.Players[global_systems.startingPlayer]
    firstTurnPlayer.setBackground("green")
    
    command = str(global_systems.startingPlayer)
    commandEncoded = command.encode('utf-8')
    UDPClient.sendto(commandEncoded, serverAddress)

    
    secondTurnPlayer = global_systems.Players[global_systems.otherGuy]
    secondTurnPlayer.setBackground("#262626")
    
    gameVariables = {
        "isRunning" : True,
        "player" : firstTurnPlayer,
        "blockPlayer" : MakeImage("images/block.png"),
        "lock" : 0
    }

    def checkTurn():

        if global_systems.switchForm == "manual":
            if (gameVariables["lock"] == 1 and firstTurnPlayer.getShots() == 0):
                firstTurnPlayer.setBackground("#262626") 
                gameVariables["player"] = secondTurnPlayer
                secondTurnPlayer.setBackground("green")
                
                command = str(global_systems.otherGuy)
                commandEncoded = command.encode('utf-8')
                UDPClient.sendto(commandEncoded, serverAddress)
            
            elif (gameVariables["lock"] == 0 and firstTurnPlayer.getShots() == 0):
                  firstTurnPlayer.setBackground("#262626") 
                  gameVariables["player"] = None
        
        elif global_systems.switchForm == "auto":
            if firstTurnPlayer.getShots() == 0:
                firstTurnPlayer.setBackground("#262626") 
                gameVariables["player"] = secondTurnPlayer
                secondTurnPlayer.setBackground("green")

                command = str(global_systems.otherGuy)
                commandEncoded = command.encode('utf-8')
                UDPClient.sendto(commandEncoded, serverAddress)


    def endGame():
        if (firstTurnPlayer.getShots() == 0 and secondTurnPlayer.getShots() == 0): 
            gameVariables["isRunning"] = False



    def Timer():
            print("timer started")
            while gameVariables["player"].getShotStatus() == True:
                time.sleep(3)
                if gameVariables["player"] == None:
                    return
                elif gameVariables["player"].getShotStatus() == True:
                        gameVariables["player"].setScore(5)

    def zoneSFX(zone):
        effect = pygame.mixer.Sound(f"sfx/{zone}.mp3")
        effect.set_volume(1)
        effect.play()
    
    def action(action):

        if action == "End":
            if gameVariables["player"].getShotStatus() == False:
                
                gameVariables["player"].removeShots()
                gameVariables["player"].setMissedShots()

            elif gameVariables["player"].getShotStatus() == True:
                
                gameVariables["player"].removeShots()
                gameVariables["player"].setShotStatus(False)

        elif action == "Switch":
            gameVariables["lock"] = 1

        elif action == "null":
            pass

        else:
            score = action.split("-")

            if gameVariables["player"].getShotStatus() == False:
                gameVariables["player"].setShotStatus(True)
                gameVariables["player"].setScore(int(score[1]))
                
                shotTimer = threading.Thread(target=Timer)
                shotTimer.daemon = True
                shotTimer.start()

                zone = threading.Thread(target=lambda:zoneSFX(score[0]))
                zone.daemon = True
                zone.start()
            
            elif gameVariables["player"].getShotStatus() == True:
                gameVariables["player"].setScore(int(score[1]))
                
                zone = threading.Thread(target=lambda:zoneSFX(score[0]))
                zone.daemon = True
                zone.start()


    def Gameloop():
        while gameVariables["isRunning"]:
            try:

                Player1_shots['text'] = f"Tiros Restantes: {global_systems.Players[0].getShots()}"
                Player2_shots['text'] = f"Tiros Restantes: {global_systems.Players[1].getShots()}"

                Player1_missedShots['text'] = f"Tiros Fallidos: {global_systems.Players[0].getMissedShots()}"
                Player2_missedShots['text'] = f"Tiros Fallidos: {global_systems.Players[1].getMissedShots()}"

                Player1_score['text'] = f"Puntaje Total: {global_systems.Players[0].getScore()}"
                Player2_score['text'] = f"Puntaje Total: {global_systems.Players[1].getScore()}"
                
                checkTurn()
                canvas.itemconfig(Player1_background, fill=f"{global_systems.Players[0].getBackground()}")
                canvas.itemconfig(Player2_background, fill=f"{global_systems.Players[1].getBackground()}")
                window.update()
                endGame()
                time.sleep(0.06)
            
            except ValueError:
                return "Intercambie jugador para continuar"
            
        StartEnd()

    def checking():
        while gameVariables["isRunning"]:

            if global_systems.switchForm == "auto":
                
                command = "sendZone"
                commandEncoded = command.encode('utf-8')
                UDPClient.sendto(commandEncoded, serverAddress)
                
                data,address = UDPClient.recvfrom(bufferSize)
                dataDecoded = data.decode('utf-8')
                print(dataDecoded)
                action(dataDecoded)

            elif global_systems.switchForm == "manual":
            
                if gameVariables["player"].getShots()!=0:
                    command = "sendZone"
                    commandEncoded = command.encode('utf-8')
                    UDPClient.sendto(commandEncoded, serverAddress)
                    
                    data,address = UDPClient.recvfrom(bufferSize)
                    dataDecoded = data.decode('utf-8')
                    print(dataDecoded)
                    action(dataDecoded)

                else:
                    command = "needSwitch"
                    commandEncoded = command.encode('utf-8')
                    UDPClient.sendto(commandEncoded, serverAddress)
                    
                    data,address = UDPClient.recvfrom(bufferSize)
                    dataDecoded = data.decode('utf-8')
                    print(dataDecoded)
                    action(dataDecoded)

            time.sleep(0.1)


    canvas_width, canvas_height = 800, 700
    canvas = Canvas(window, width=canvas_width, height=canvas_height, bg="#262626")
    canvas.pack()



    # Player 1
    Player1_team = MakeImage(global_systems.Players[0].getCharacter("team"))
    Player1_character = MakeImage(global_systems.Players[0].getCharacter("image"))
    Label(window, image=Player1_team, width=150, height=150).place(relx=0.25, rely=0.2, anchor="center")
    Label(window, image=Player1_character, width=150, height=150).place(relx=0.25, rely=0.35, anchor="center")

    Player1_name = Button(window, text=f"{global_systems.Players[0].getPlayerName()}", width=20, height=2)
    Player1_name.place(relx=0.25, rely=0.5, anchor="center")

    Player1_shots = Button(window, text="", width=20, height=2)
    Player1_shots.place(relx=0.25, rely=0.6, anchor="center")

    Player1_missedShots = Button(window, text="", width=20, height=2)
    Player1_missedShots.place(relx=0.25, rely=0.7, anchor="center")

    Player1_score = Button(window, text="", width=20, height=2)
    Player1_score.place(relx=0.25, rely=0.8, anchor="center")

    Player1_background = canvas.create_rectangle(0,0,400,700, fill="#262626")



    
    # Player 2
    Player2_team = MakeImage(global_systems.Players[1].getCharacter("team"))
    Player2_character = MakeImage(global_systems.Players[1].getCharacter("image"))
    Label(window, image=Player2_team, width=150, height=150).place(relx=0.75, rely=0.2, anchor="center")
    Label(window, image=Player2_character, width=150, height=150).place(relx=0.75, rely=0.35, anchor="center")

    Player2_name = Button(window, text=f"{global_systems.Players[1].getPlayerName()}", width=20, height=2)
    Player2_name.place(relx=0.75, rely=0.5, anchor="center")

    Player2_shots = Button(window, text="", width=20, height=2)
    Player2_shots.place(relx=0.75, rely=0.6, anchor="center")

    Player2_missedShots = Button(window, text="", width=20, height=2)
    Player2_missedShots.place(relx=0.75, rely=0.7, anchor="center")

    Player2_score = Button(window, text="", width=20, height=2)
    Player2_score.place(relx=0.75, rely=0.8, anchor="center")

    Player2_background = canvas.create_rectangle(400,0,800,700, fill="#262626")


    listen = threading.Thread(target= checking)
    listen.daemon = True
    listen.start()

    Gameloop()
    window.mainloop()


    ##################################################################################
    ##################################################################################

def endScreen():
        
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Juego")
    window.configure(bg="#262626")


    canvas_width, canvas_height = 800, 700
    canvas = Canvas(window, width=canvas_width, height=canvas_height, bg="#262626")
    canvas.pack()



    def ganador():

        if global_systems.Players[0].getScore() > global_systems.Players[1].getScore():
            canvas.itemconfig(Player1_background, fill="yellow")
            Player1_end['text'] = "GANADOR!!!!"
            Player2_end['text'] = ":("
        
        elif global_systems.Players[1].getScore() > global_systems.Players[0].getScore():
            canvas.itemconfig(Player2_background, fill="yellow")
            Player2_end['text'] = "GANADOR!!!!"
            Player1_end['text'] = ":("
        
        Player1_score['text'] = f"Puntaje Total: {global_systems.Players[0].getScore()}"
        Player2_score['text'] = f"Puntaje Total: {global_systems.Players[1].getScore()}"

        command = "kill"
        commandEncoded = command.encode('utf-8')
        UDPClient.sendto(commandEncoded, serverAddress)



    # Player 1
    Player1_team = MakeImage(global_systems.Players[0].getCharacter("team"))
    Player1_character = MakeImage(global_systems.Players[0].getCharacter("image"))
    Label(window, image=Player1_team, width=150, height=150).place(relx=0.25, rely=0.2, anchor="center")
    Label(window, image=Player1_character, width=150, height=150).place(relx=0.25, rely=0.35, anchor="center")

    Player1_name = Button(window, text=f"{global_systems.Players[0].getPlayerName()}", width=20, height=2)
    Player1_name.place(relx=0.25, rely=0.5, anchor="center")

    Player1_score = Button(window, text="", width=20, height=2)
    Player1_score.place(relx=0.25, rely=0.6, anchor="center")

    Player1_end = Button(window, text="", width=20, height=2)
    Player1_end.place(relx=0.25, rely=0.7, anchor="center")


    Player1_background = canvas.create_rectangle(0,0,400,700, fill="#262626")



    
    # Player 2
    Player2_team = MakeImage(global_systems.Players[1].getCharacter("team"))
    Player2_character = MakeImage(global_systems.Players[1].getCharacter("image"))
    Label(window, image=Player2_team, width=150, height=150).place(relx=0.75, rely=0.2, anchor="center")
    Label(window, image=Player2_character, width=150, height=150).place(relx=0.75, rely=0.35, anchor="center")

    Player2_name = Button(window, text=f"{global_systems.Players[1].getPlayerName()}", width=20, height=2)
    Player2_name.place(relx=0.75, rely=0.5, anchor="center")

    Player2_score = Button(window, text="", width=20, height=2)
    Player2_score.place(relx=0.75, rely=0.6, anchor="center")

    Player2_end = Button(window, text="", width=20, height=2)
    Player2_end.place(relx=0.75, rely=0.7, anchor="center")
    
    Player2_background = canvas.create_rectangle(400,0,800,700, fill="#262626")

    ganador()


    window.mainloop()