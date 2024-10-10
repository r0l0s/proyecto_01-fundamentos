import socket
import utime
import network
import machine
from machine import Pin
import _thread


# En esta sección se crean las variables globales que guardan el puerto
# También determinan si el puerto es de salida o entrada

LED = Pin('LED',Pin.OUT)

buzzer = Pin(15, Pin.OUT)

potentiometer = Pin(27, Pin.OUT)

pulse = Pin(18, Pin.OUT)

clock = Pin(19, Pin.OUT)

clear = Pin(20, Pin.OUT)

mylist = []

analog_reading = True

#######################################################################
#######################################################################
# Ejecución del código wifi
# El raspberry intenta establecer conección con el router
# Si la conexión es exitosa se enciende el led verde integrado en el raspberry
# Si no es exitosa, el buzzer suena por un segundo

wifi = network.WLAN(network.STA_IF)
wifi.active(False)
wifi.active(True)

try:
    wifi.connect('Hubble -2.4G','hubble2024')
    print('Establishing WiFi connection')
    
    for i in range(10):
        utime.sleep(1)
        if wifi.isconnected():
            break
    if wifi.isconnected():
        
        print ('connected')
        wifiInfo = wifi.ifconfig()
        ServerIP = wifiInfo[0]
        # Hace un print de la dirección ip que se pone en el cliente
        print (ServerIP)

        # port
        ServerPort = 2222

        # size of the packet
        bufferSize = 1024 # bytes

        # creating the socket
        # UDP is the communication protocol
        UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # connecting the UDP server with a specific IP address
        UDPServer.bind((ServerIP, ServerPort))

        #print('UDP Server Waiting...')
        LED.value(1)
        
              
    else:
        buzzer.value(1)
        utime.sleep(1)
        buzzer.value(0)
        
except Exception as e: print(e)
#######################################################################
#######################################################################


# Esta función se encarga de encender el buzzer
# No tiene que ver con la conexión wifi
def buzz(address):
    buzzer.value(1)
    utime.sleep(0.5)
    buzzer.value(0)
    
    dataString = f'Received Command: {messageDecoded}'
    dataStringEncoded = dataString.encode('utf-8')
    UDPServer.sendto(dataStringEncoded,address)
    

# Sección de lectura del potenciómetro
#######################################################################
#######################################################################

# Esta función detiene la lectura del potenciómetro
def quit_reading(address):
    global analog_reading
    
    analog_reading == False
    
    dataString = f'Received Command: {messageDecoded}'
    dataStringEncoded = dataString.encode('utf-8')
    UDPServer.sendto(dataStringEncoded,address)


# Esta función lee el valor del potenciómetro
# El while se mantiene corriendo por medio del hilo
def readingPot(address):
    global potentiometer, analog_reading
    analog_reading == True
    myPot = machine.ADC(potentiometer)
    
    while analog_reading:
        
         potVal = myPot.read_u16()
         voltage = (3.3/65106)*potVal-(430*3.3/65106)
         
         dataString = str(voltage)
         dataStringEncoded = dataString.encode('utf-8')
         UDPServer.sendto(dataStringEncoded,address)    
         utime.sleep(0.1)
         
             
    dataString = f'Received Command: {messageDecoded}'
    dataStringEncoded = dataString.encode('utf-8')
    UDPServer.sendto(dataStringEncoded,address)
         
#######################################################################
#######################################################################



# Sección de registro
#######################################################################
#######################################################################

def reset_register(address):
    
    clear.value(0)
    utime.sleep(0.01)
    clear.value(1)
    
    dataString = f'Received Command: {messageDecoded}'
    dataStringEncoded = dataString.encode('utf-8')
    UDPServer.sendto(dataStringEncoded,address)


def translator(index):
    global mylist
    
    if index == 6:
        return 0
    
    elif mylist[index] == 'h':
        mylist[index] = 1
        
    elif mylist[index] == 'l':
        mylist[index] = 0
        
    return translator(index+1)


def register(address):
    
    global mylist
    
    clear.value(0)
    utime.sleep(0.01)
    clear.value(1)
    
    dataString = 'Insert Pattern'
    dataStringEncoded = dataString.encode('utf-8')
    UDPServer.sendto(dataStringEncoded,address)
    

        
    # waiting for message
    message, address = UDPServer.recvfrom(bufferSize)

    # decoding
    messageDecoded = message.decode('utf-8')
        
    
    for i in range(6):
        mylist.append(messageDecoded[i])
        
        
        
    translator(0)
        
    print(mylist)
            
            
    def reg(pattern, index):
            
        if index == 6:
            return 
        
        else:
            pulse.value(pattern[index])
            print(index)
            #utime.sleep(0.01)
            clock.value(1)
            #utime.sleep(0.01)
            clock.value(0)
            
            return reg(pattern,index+1)
        
        
    reg(mylist,0)
    
    mylist.clear()
    
    print(mylist)
    
    # sending data back
    dataString = f'Received Command: {messageDecoded}'
    dataStringEncoded = dataString.encode('utf-8')
    UDPServer.sendto(dataStringEncoded,address)

#######################################################################
#######################################################################

# Este while corre en el núcleo principal del raspberry
# Está encargado de escuchar comandos del cliente y ejecutar funciones
while True:

    # waiting for message
    message, address = UDPServer.recvfrom(bufferSize)

    # decoding
    messageDecoded = message.decode('utf-8')
    #print(messageDecoded)
    
    if messageDecoded == 'CONFIG':
        _thread.start_new_thread(readingPot,(address))
        
    elif messageDecoded == 'CONFIG_CLOSE':
        quit_reading(address)
        
    elif messageDecoded == 'BUZZ':
        buzz(address)
        
    elif messageDecoded == 'REG':
        register(address)
    
    elif messageDecoded == 'REG_CLEAR':
        reset_register(address)
    
    print("running")