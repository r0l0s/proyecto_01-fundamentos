
# Personajes
###############################################################
A = {
    "jugador01" : ["Mordecai", 'images/equipo01/jugador01.png','images/equipo01/escudo.png'],
    "jugador02" : ["Benson", 'images/equipo01/jugador02.png','images/equipo01/escudo.png'],
    "jugador03" : ["Rigby", 'images/equipo01/jugador03.png','images/equipo01/escudo.png']
}
equipoA = [A["jugador01"],A["jugador02"],A["jugador03"]]

B = {
    "jugador01" : ["Bob", 'images/equipo02/jugador01.png','images/equipo02/escudo.png'],
    "jugador02" : ["Patricio", 'images/equipo02/jugador02.png','images/equipo02/escudo.png'],
    "jugador03" : ["Calamardo", 'images/equipo02/jugador03.png','images/equipo02/escudo.png']
}
equipoB = [B["jugador01"],B["jugador02"],B["jugador03"]]


C = {
    "jugador01" : ["Gumball", 'images/equipo03/jugador01.png','images/equipo03/escudo.png'],
    "jugador02" : ["Darwin", 'images/equipo03/jugador02.png','images/equipo03/escudo.png'],
    "jugador03" : ["Richard", 'images/equipo03/jugador03.png','images/equipo03/escudo.png']
}
equipoC = [C["jugador01"],C["jugador02"],C["jugador03"]]
###############################################################

switchForm = "auto"

backgroundMusic = None

def changeSwitchForm(form):
    global switchForm

    switchForm = form
    print(str(switchForm))

Players = []
startingPlayer = None
otherGuy = None


def OtherPlayer(startingPlayer):
    if startingPlayer == 0:
        return 1
    else:
        return 0

textInfo = """
    Tecnológico de Costa Rica 
    Ingeniería en Computadores 
    Fundamentos de Sistemas Computacionales
    Profesor: Luis Chavarría
    Estudiantes:
    Yazar Arias Saborio
    Antonio Rojas Loaiza
    Costa Rica, 2024 
    Versión 1.0 
    """