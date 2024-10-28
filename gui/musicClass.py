import pygame



class Song:
    def __init__(self):
         pygame.mixer.init()
         pygame.mixer.music.load("music/theme.mp3")

    def startSong(self):
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()


    def stopSong(self):
        pygame.mixer.music.stop()

    def setVolume(self,volume):
        pygame.mixer.music.set_volume(volume)
