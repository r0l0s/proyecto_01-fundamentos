
# El cliente se encarga de enviar comandos en forma de strings al rasberry
# Funciona principalmente para hacer pruebas y debugging

import socket

# El serverAddress se obtiene del raspberry una vez que se corra el codigo de conexión wifi
# El código wifi corre cada vez que se enciende el raspberry
# La dirección ip que da el raspberry es la que se pone acá

serverAddress = ('192.168.100.38', 2222)
bufferSize = 1024

UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Este while corre constantemente
# Acá es donde se mandan los comandos

while True: 
    # creating a command
    cmd = input('What is your command? ')
 
    # encoding
    cmdEncoded = cmd.encode('utf-8')
 
    # sending
    UDPClient.sendto(cmdEncoded, serverAddress)
     
    # waiting for response
    data,address = UDPClient.recvfrom(bufferSize)
    dataDecoded = data.decode('utf-8')
    print(f'Message from server: {dataDecoded}')