import socket 
import lib
import time
import wave
from threading import Thread

buffSize = 32767 + 13 
chunk = 1024
subscribers = []
timeout = time.time() + 60 * 5

# Listener function for the server
def serverListener(receiver, metaPacket):

    while(True):
        try:
            message, addr = receiver.recvfrom(buffSize)
            print('pesan', message)
            typ, data = lib.breakPacket(message)
            print(typ)
            if (typ == "SUB"):
                print("sub baru nih")
                receiver.sendto(metaPacket, addr)
                subscribers.append(addr) 

        except:
            print("error")

        if(time.time() > timeout):
            break

def sendPacket(receiver, dataPacket, addr):

    receiver.sendto(dataPacket, addr)




port = int(input("Masukkan port yang akan dibind: "))
filename = input("Masukkan nama file WAV yang ingin dibroadcast ke seluruh client: ")



#Open a socket connection and bind it to a port
receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver.bind((socket.gethostbyname(socket.gethostname()), port))

print(socket.gethostbyname(socket.gethostname()))

# Open the WAV file
wf = wave.open(filename, 'rb')


metadata = [wf.getsampwidth(), wf.getnchannels(), wf.getframerate(), wf.getnframes(), filename]

metaPacket = lib.createPacket("META", metadata)
print('pisang', metaPacket)

t = Thread(target = serverListener, args = (receiver, metaPacket))
t.start()

data = wf.readframes(chunk)

chunks = []

while data != b'':
    chunks.append(data)
    data = wf.readframes(chunk)

siz = len(chunks)

time.sleep(3)

frameSize = metadata[0] * metadata[1] 
frameCountPerChunk = chunk / frameSize 

chunkTime = 1000 * frameCountPerChunk / metadata[2]


for i in range(siz):
    startTime = time.time() * 1000
    # print("packet pengiriman ke ", i)
    dataPacket = b''
    if(i == siz - 1):
        dataPacket = lib.createPacket("DATA", chunks[i], 1)
    else:
        dataPacket = lib.createPacket("DATA", chunks[i])
    for addr in subscribers:
        sendPacket(receiver, dataPacket, addr)

    endTime = time.time() * 1000 
    delta = endTime - startTime 
    if(delta < chunkTime):
        time.sleep((chunkTime - delta) / 1000)
    











