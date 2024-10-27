import time

class Player:
    def __init__(self, playerName):
        
        self.playerName = playerName
        self.characterName = None
        self.characterImage = None
        self.characterTeam = None
        self.score = 0
        self.shots = 3
        self.missed_shots = 0
        self.active_shot = False

    def getPlayerName(self):
        return self.playerName

    def setCharacter(self, name, image, team):
        self.characterName = name
        self.characterImage = image
        self.characterTeam = team

    def getCharacter(self, atributo):
        
        if atributo == "name":
            return self.characterName
        elif atributo == "image":
            return self.characterImage
        elif atributo == "team":
            return self.characterTeam
        elif atributo == "all":
            return (self.playerName,self.characterName, self.characterImage, self.characterTeam, self.score, self.shots)
        
    
    def getScore(self):
        return self.score
    
    def setScore(self, newScore):
        self.score += newScore

    def getShots(self):
        return self.shots
    
    def removeShots(self):
        self.shots -= 1

    def getShotStatus(self):
        return self.active_shot
    
    def setShotStatus(self, status):
        self.active_shot = status

    def getMissedShots(self):
        return self.missed_shots
    
    def setMissedShots(self):
        self.missed_shots += 1
