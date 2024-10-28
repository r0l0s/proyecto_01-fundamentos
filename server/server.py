
from tkinter import*
import socket
import time
import threading

serverIP = '192.168.100.7'
serverPort = 2222
bufferSize = 1024

UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServer.bind((serverIP,serverPort))

cuba = None
carrot = True
system = {
    "running": True
}

def TestWindow():
    
    window = Tk()
    window.minsize(width= 800, height=700)
    window.title("Testing")
    window.configure(bg="#262626")


    scaleVariable = IntVar()
    potentiometer = Scale(window, from_= 0, to=2, length=300, orient="vertical", variable=scaleVariable)
    potentiometer.place(relx=0.1, rely=0.5, anchor="center")


    
    def ZoneA():
        dataString = "ZA-2"
        dataStringEncoded = dataString.encode('utf-8')
        UDPServer.sendto(dataStringEncoded,cuba)
        print(cuba)
        print("sent")

    ZonaA = Button(window, text="Zone A", width=30, height=2, command= ZoneA) 
    ZonaA.place(relx=0.5, rely=0.2, anchor="center")


    def ZoneB():
        dataString = "ZB-3"
        dataStringEncoded = dataString.encode('utf-8')
        UDPServer.sendto(dataStringEncoded,cuba)
        print(cuba)
        print("sent")

    ZonaB = Button(window, text="Zone B", width=30, height=2, command= ZoneB) 
    ZonaB.place(relx=0.5, rely=0.3, anchor="center")

    
    def ZoneC():
        dataString = "ZC-4"
        dataStringEncoded = dataString.encode('utf-8')
        UDPServer.sendto(dataStringEncoded,cuba)
        print(cuba)
        print("sent")

    ZonaC = Button(window, text="Zone C", width=30, height=2, command= ZoneC) 
    ZonaC.place(relx=0.5, rely=0.4, anchor="center")


    def ZoneD():
        dataString = "ZD-5"
        dataStringEncoded = dataString.encode('utf-8')
        UDPServer.sendto(dataStringEncoded,cuba)
        print(cuba)
        print("sent")

    ZonaD = Button(window, text="Zone D", width=30, height=2, command= ZoneD) 
    ZonaD.place(relx=0.5, rely=0.5, anchor="center")


    def ZoneE():
        dataString = "ZE-10"
        dataStringEncoded = dataString.encode('utf-8')
        UDPServer.sendto(dataStringEncoded,cuba)
        print(cuba)
        print("sent")

    ZonaE = Button(window, text="Zone E", width=30, height=2, command= ZoneE) 
    ZonaE.place(relx=0.5, rely=0.6, anchor="center")


    def End():
        dataString = "End"
        dataStringEncoded = dataString.encode('utf-8')
        UDPServer.sendto(dataStringEncoded,cuba)
        print(cuba)
        print("sent")

    End = Button(window, text="EndShot", width=30, height=2, command= End) 
    End.place(relx=0.5, rely=0.7, anchor="center")


    def Switch():
        dataString = "Switch"
        dataStringEncoded = dataString.encode('utf-8')
        UDPServer.sendto(dataStringEncoded,cuba)
        print(cuba)
        print("sent")

    SwitchButton = Button(window, text="Switch", width=30, height=2, command= Switch) 
    SwitchButton.place(relx=0.5, rely=0.8, anchor="center")


#############################################################################################
#############################################################################################

    def Communication():
        global carrot, cuba

        while system["running"]:
            
            message,address = UDPServer.recvfrom(bufferSize)
            messageDecoded = message.decode('utf-8')
            cuba = address


            if messageDecoded == "start":
                carrot = True

                def Reading():
                    
                    #message, address = UDPServer.recvfrom(bufferSize)
                    while carrot:
                        dataString = str(scaleVariable.get())
                        print(dataString)
                        dataStringEncoded = dataString.encode('utf-8')
                        UDPServer.sendto(dataStringEncoded,address)
                        time.sleep(0.1)
                
                reading = threading.Thread(target= Reading)
                reading.daemon = True
                reading.start()

            if messageDecoded == "kill":
                carrot = False
        
            
            window.update()
            time.sleep(0.016)
            

    test = threading.Thread(target= Communication)
    test.daemon = True
    test.start()
    window.mainloop()

#############################################################################################
#############################################################################################

TestWindow()