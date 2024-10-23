
class Player:
    def __init__(self, nombreJugador):
        
        self.nombreJugador = nombreJugador
        self.nombrePersonaje = None
        self.personajeImage = None
        self.equipo = None
        self.puntaje = 0
        self.lanzamientos = 3


    def getName(self):
        return self.nombreJugador
    
    def setPersonaje(self, nombre, imagen, equipo):
        self.nombrePersonaje = nombre
        self.personajeImage = imagen
        self.equipo = equipo

    def getPersonaje(self, atributo):
        if atributo == "nombre":
            return self.nombrePersonaje
        elif atributo == "imagen":
            return self.personajeImage
        elif atributo == "equipo":
            return self.equipo
        
    
    def getPuntaje(self):
        return self.puntaje
    
    def setPuntaje(self, nuevoPuntaje):
        self.puntaje += nuevoPuntaje

    def getLanzamientos(self):
        return self.lanzamientos
    
    def setLanzamientos(self):
        self.lanzamientos -= 1