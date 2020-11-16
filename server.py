import socket 
import sys 
import lib
import time
import random
import os
import pyaudio
import wave
from threading import Thread

buffSize = 32767 + 13
chunkSize = 1024
subscribers = []
timeout = time.time() + 60 * 5

def serverListener(receiver, metaPacket):

    while(True):
        print("listnerer")
        time.sleep(2)
        try:
            message, addr = receiver.recvfrom(buffSize)
            
            typ, data = lib.breakPacket(message)

            if (typ == "SUB"):
                receiver.sendto(metaPacket, addr)
                subscribers.append(addr) 

        except:
            print("error")

        if(time.time() > timeout):
            break




port = int(input("Masukkan port yang akan dibind: "))
filename = input("Masukkan nama file WAV yang ingin dibroadcast ke seluruh client: ")


#Open a socket connection and bind it to a port
receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver.bind((socket.gethostbyname(socket.gethostname()), port))

# Open the WAV file
wf = wave.open(filename, 'rb')


metadata = [wf.getsampwidth(), wf.getnchannels(), wf.getframerate()]

metaPacket = lib.createPacket("META", metadata)

t = Thread(target = serverListener, args = (receiver, metaPacket))
t.start()

while(True):
    print("notlis")
    time.sleep(2)











