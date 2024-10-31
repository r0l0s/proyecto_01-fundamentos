from machine import Pin
from utime import sleep
import network
import socket
from machine import Pin, ADC
import math

class Systems:
    def __init__(self):
        self.client = None
        self.pot = False
        self.zone = False
        self.switch = False
        self.changePlayer = False 
        self.player = None

    def getClient(self):
        return self.client
    def setClient(self, address):
        self.client = address

    def getPot(self):
        return self.pot
    
    def setPot(self,state):
        self.pot = state

    def getZone(self):
        return self.zone

    def setZone(self, state):
        self.zone = state

    def getSwitch(self):
        return self.switch
    
    def setSwitch(self, state):
        self.switch = state

    def getChangePlayer(self):
        return self.changePlayer
    
    def setChangePlayer(self, state):
        self.changePlayer = state

    def getPlayer(self):
        return self.player
    
    def setPlayer(self,player):
        self.player = player


# Global Variables ###################################################################
#######################################################################################

test = Systems()
mainLED = Pin("LED", Pin.OUT)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
potentiometer = ADC(Pin(28))

ButtonSwitch = Pin(0, Pin.IN, Pin.PULL_DOWN)


zoneA = Pin(7, Pin.IN, Pin.PULL_DOWN)
zoneB = Pin(8, Pin.IN, Pin.PULL_DOWN)
zoneC = Pin(9, Pin.IN, Pin.PULL_DOWN)
zoneD = Pin(10, Pin.IN, Pin.PULL_DOWN)
zoneE = Pin(11, Pin.IN, Pin.PULL_DOWN)
End = Pin(12, Pin.IN, Pin.PULL_DOWN)

zones = [(zoneA,"ZA-2","hlllll"), 
         (zoneB,"ZB-3","lhllll"), 
         (zoneC,"ZC-4","llhlll"), 
         (zoneD,"ZD-5","lllhll"), 
         (zoneE,"ZE-10","llllhh"), 
         (End,"End")]

player_1 = Pin(26, Pin.OUT)
player_2 = Pin(27, Pin.OUT)


# Register Stuff

pulse = Pin(18, Pin.OUT)
clock = Pin(19, Pin.OUT)
clear = Pin(20, Pin.OUT)

regList = []

#######################################################################################
#######################################################################################



# Establishing connection #############################################################
#######################################################################################

def connection():
    global mainLED, UDPServer
    wifi = network.WLAN(network.STA_IF)
    wifi.active(False)
    wifi.active(True)

    try:
        wifi.connect('Hubble -2.4G','hubble2024')
        print('Establishing WiFi connection')
        
        for i in range(20):
            sleep(1)
            if wifi.isconnected():
                break
        if wifi.isconnected():
            
            print ('connected')
            wifiInfo = wifi.ifconfig()
            ServerIP = wifiInfo[0]
            # Hace un print de la dirección ip que se pone en el cliente
            print (ServerIP)

            # connecting the UDP server with a specific IP address
            server.bind((ServerIP, 2222))

            print('Server Waiting...')
            mainLED.toggle()
            sleep(5)
            mainLED.off()
                
        else:
            connection()
            
    except Exception as e: print(e)

#######################################################################################
#######################################################################################

def switch():
    global ButtonSwitch
    while test.getSwitch() == False:
        if ButtonSwitch.value() == 1:
            test.setSwitch(True)
            return

# Micro controller Actions #############################################################
#######################################################################################

# This function handles the zone logic and communication
##########################################################
def zoneReading():
    global zones

    for pin in zones:
        print("count")
        if pin[0].value() == 1:
            if pin[1] == "End":
                return pin[1]
            else:
                registerA(pin[2])
                return pin[1]
    return "null"
##########################################################

# Register section ################################################
###################################################################

def translator(index):
    global regList
    
    if index == 6:
        return 0
    
    elif regList[index] == 'h':
        regList[index] = 1
        
    elif regList[index] == 'l':
        regList[index] = 0
        
    return translator(index+1)


# Micro controller - Register
############################################################
def registerA(messageDecoded):
    global regList, clear, clock, pulse
    
    clear.value(0)
    sleep(0.01)
    clear.value(1)
    
    # Guarda los caracteres en mylist
    regList = list(messageDecoded[:6])  # Solo toma los primeros 6 caracteres
    print(regList)
    
    # Traduce el patrón
    translator(0)
    
    # Envía el patrón al registro
    def reg(pattern, index):
        if index == 6:
            return
        else:
            pulse.value(pattern[index])
            clock.value(1)
            clock.value(0)
            print(pulse.value())
            return reg(pattern, index + 1)
    
    reg(regList, 0)
    regList.clear()
############################################################


def action():
    global test
        
    if test.getPot():

        potVal = potentiometer.read_u16()
        factor = 3.3 / (65535)

        vol = math.floor(potVal*factor)

        if vol >= 3:
            vol = 2
        
        sleep(0.1)

        dataString = str(1)
        dataStringEncoded = dataString.encode('utf-8')    
        server.sendto(dataStringEncoded,test.getClient())
        test.setPot(False)


    elif test.getZone():

        cmd = str(zoneReading())
        sleep(0.1)
        cmdEncoded = cmd.encode('utf-8')    
        server.sendto(cmdEncoded,test.getClient())
        test.setZone(False)


    elif test.getSwitch():

        switch()

        dataString = "Switch"
        dataStringEncoded = dataString.encode('utf-8')    
        server.sendto(dataStringEncoded,test.getClient())
        test.setSwitch(False)

    elif test.getChangePlayer():

        if test.getPlayer() == 1:
            player_1.value(1)
            player_2.value(0)
        
        elif test.getPlayer() == 0:
            player_2.value(1)
            player_1.value(0)

        dataString = "null"
        dataStringEncoded = dataString.encode('utf-8')    
        server.sendto(dataStringEncoded,test.getClient())
        test.setChangePlayer(False)


#######################################################################################
#######################################################################################

# Waiting for commands ################################################################
#######################################################################################

def commandLoop():
    global test
    
    while True:

        data, address = server.recvfrom(1024)
        decoded = data.decode()
        test.setClient(address)
        print(decoded)
        
        if decoded == "sendPot":
            test.setPot(True)
            action()


        elif decoded == "sendZone":
            test.setZone(True)
            action()

            cmd = input("command:")
 
            # encoding
            cmdEncoded = cmd.encode('utf-8')

            # sending
            server.sendto(cmdEncoded, test.getClient())
    
            
        elif decoded == "needSwitch":
            test.setSwitch(True)
            action()

        elif decoded =="0":
            test.setPlayer(0)
            test.setChangePlayer(True)
            action()

        elif decoded == "1":
            test.setPlayer(1)
            test.setChangePlayer(True)
            action()

        elif decoded == "kill":
            return()

#######################################################################################
#######################################################################################


connection()
commandLoop()


        

            







