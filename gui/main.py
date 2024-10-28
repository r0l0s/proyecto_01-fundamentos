
from tkinter import *
import pygame
import global_systems
import game_module
import threading
import musicClass



def OpenGame(window):
    window.destroy()
    game_module.GameConfigWindow(OpenMain)

def OpenGameConfig(window):
    window.destroy()
    GameConfigWindow()

def OpenAbout(window):
    window.destroy()
    AboutWindow()

def OpenDebug(window):
    window.destroy()
    DebugWindow()

def OpenMain(window):
    window.destroy()
    MainWindow()




# Sección de música
##################################################################################

#pygame.mixer.init()

global_systems.backgroundMusic = musicClass.Song()


# Esta función inicializa la canción y luego la reproduce
def play():
    global_systems.backgroundMusic.startSong()
    
    
# Esta función detiene la música
def stop():
    global_systems.backgroundMusic.stopSong()


##################################################################################


# Esta es la ventana principal
##################################################################################
def MainWindow():
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("PinBall!!!")
    window.configure(bg="#262626")


    ButtonPlay = Button(window, text="Jugar", width=30, height=2, command= lambda: OpenGame(window))
    ButtonPlay.place(relx=0.5, rely=0.25, anchor="center")

    ButtonConfig = Button(window, text="Configuración de música",width=30, height=2, command= lambda: OpenGameConfig(window))
    ButtonConfig.place(relx=0.5, rely=0.45, anchor="center")

    ButtonAbout = Button(window, text="About",width=30, height=2, command= lambda: OpenAbout(window))
    ButtonAbout.place(relx=0.5, rely=0.65, anchor="center")

    ButtonPruebas = Button(window, text="Modo de Pruebas",width=30, height=2, command= lambda: OpenAbout(window))
    ButtonPruebas.place(relx=0.5, rely=0.85, anchor="center")


    window.mainloop()
##################################################################################


# Esta es la ventana de configuración
##################################################################################
def GameConfigWindow():
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Configuración de Juego")
    window.configure(bg="#262626")

    ButtonReturn = Button(window, text="Regresar", width=30, height=2, command= lambda: OpenMain(window))
    ButtonReturn.place(relx=0.2, rely=0.9, anchor="center")

    
    
    # Control de música
    play_button = Button(window, text="Reproducir Música", width=30, height=2, command=play)
    play_button.place(relx=0.5, rely=0.3, anchor="center")

    stop_button = Button(window, text="Detener Música", width=30, height=2, command=stop)
    stop_button.place(relx=0.5, rely=0.5, anchor="center")



    window.mainloop()
##################################################################################


# Esta es la ventana de about
##################################################################################
def AboutWindow():
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("About")
    window.configure(bg="#262626")

    ImageA = PhotoImage(file="images/antonio.png")
    ImageB = PhotoImage(file="images/yazar.png")

    ButtonReturn = Button(window, text="Regresar", width=30, height=2, command= lambda: OpenMain(window))
    ButtonReturn.place(relx=0.2, rely=0.9, anchor="center")

    IntegranteA = Label(window, image= ImageA)
    IntegranteA.place(relx=0.25, rely=0.25, anchor='center')

    IntegranteB = Label(window, image= ImageB)
    IntegranteB.place(relx=0.75, rely=0.25, anchor='center')

    text_info = Label(text= global_systems.textInfo)
    text_info.place(relx=0.5, rely=0.6, anchor='center')


    window.mainloop()
##################################################################################


# Esta es la ventana de about
##################################################################################
def DebugWindow():
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Modo de Pruebas")
    window.configure(bg="#262626")

    ButtonReturn = Button(window, text="Regresar", width=30, height=2, command= lambda: OpenMain(window))
    ButtonReturn.place(relx=0.2, rely=0.9, anchor="center")

    
    
    # Control de música
    play_button = Button(window, text="Reproducir Música", width=30, height=2, command=play)
    play_button.place(relx=0.5, rely=0.3, anchor="center")

    stop_button = Button(window, text="Detener Música", width=30, height=2, command=stop)
    stop_button.place(relx=0.5, rely=0.5, anchor="center")



    window.mainloop()
##################################################################################











# Main Thread Barrier ############################################################
##################################################################################

if __name__ == "__main__":

    MainWindow()