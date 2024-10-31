
# El cliente se encarga de enviar comandos en forma de strings al rasberry
# Funciona principalmente para hacer pruebas y debugging

import socket
import threading
import time 

# El serverAddress se obtiene del raspberry una vez que se corra el codigo de conexión wifi
# El código wifi corre cada vez que se enciende el raspberry
# La dirección ip que da el raspberry es la que se pone acá

serverAddress = ('192.168.100.78', 2222)
bufferSize = 1024

UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Este while corre constantemente
# Acá es donde se mandan los comandos


while True: 
    
    cmd = input("command:")
 
    # encoding
    cmdEncoded = cmd.encode('utf-8')

    # sending
    UDPClient.sendto(cmdEncoded, serverAddress)
    print(serverAddress)

    data,address = UDPClient.recvfrom(bufferSize)
    serverAddress = address
    dataDecoded = data.decode('utf-8')
    print(f'Message from server: {dataDecoded}')

     
