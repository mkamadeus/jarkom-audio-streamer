import socket
import lib
import time
import wave
import audioop
from threading import Thread

buffSize = 32767 + 13
chunk = 1024
subscribersLow = []
subscribersHigh = []
timeout = time.time() + 60 * 5

# Listener function for the server
def serverListener(receiver, metaPacketLow, metaPacketHigh):

    print('listening...')
    while(True):
        try:
            message, addr = receiver.recvfrom(buffSize)
            typ, data = lib.breakPacket(message)
            print(typ)
            if (typ == "SUB"):
                print("sub baru nih")
                q = int.from_bytes(data, 'little') # get quality
                print("kualitas", q)
                if(q == 1): # low quality
                    receiver.sendto(metaPacketLow, addr)
                    subscribersLow.append(addr)
                elif(q == 2):
                    print("tinggi")
                    receiver.sendto(metaPacketHigh, addr)
                    subscribersHigh.append(addr)
            elif(typ == "ANC"):
                print('hiyahiya flooded boi')
                receiver.sendto(lib.createPacket("ANC", ""), addr)

        except:
            print("error")

        if(time.time() > timeout):
            break


def sendPacket(receiver, dataPacket, addr):

    receiver.sendto(dataPacket, addr)

def downsampleWav(src, dst, inrate, outrate=11025, inchannels=2):
    inputFile = wave.open(src, 'r')
    outputFile = wave.open(dst, 'w')

    n_frames = inputFile.getnframes()
    data = inputFile.readframes(n_frames)
    outchannels = inchannels

    converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)

    outputFile.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
    outputFile.writeframes(converted[0])
    
    inputFile.close()
    outputFile.close()

    return True

def sendLowPacket(siz, chunkTime, chunks, receiver):
    for i in range(siz):
        startTime = time.time() * 1000
        dataPacket = b''
        if(i == siz - 1):
            dataPacket = lib.createPacket("DATA", chunks[i], 1, seqnum=i)
        else:
            dataPacket = lib.createPacket("DATA", chunks[i], seqnum=i)
        for addr in subscribersLow:
            print("LOWWWW")
            sendPacket(receiver, dataPacket, addr)

        endTime = time.time() * 1000
        delta = endTime - startTime
        if(delta < chunkTime):
            time.sleep((chunkTime - delta) / 1000)

port = int(input())
filename = input()
dst = './audio/downsample.wav'


# Open a socket connection and bind it to a port
receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
receiver.bind(("", port))

print(socket.gethostbyname(socket.gethostname()))

# Open the WAV file
wfHigh = wave.open(f'./audio/{filename}', 'rb')
fr = wfHigh.getframerate()
dwav = downsampleWav(f'./audio/{filename}', dst, fr)
wfLow = wave.open(dst, 'rb')


metadataLow = [wfLow.getsampwidth(), wfLow.getnchannels(), wfLow.getframerate(),
            wfLow.getnframes(), 'downsample.wav']
metadataHigh = [wfHigh.getsampwidth(), wfHigh.getnchannels(), wfHigh.getframerate(),
            wfHigh.getnframes(), filename]

metaPacketLow = lib.createPacket("META", metadataLow)
metaPacketHigh = lib.createPacket("META", metadataHigh)

t = Thread(target=serverListener, args=(receiver, metaPacketLow, metaPacketHigh), daemon=True)
t.start()

dataHigh = wfHigh.readframes(chunk)
dataLow = wfLow.readframes(chunk)

chunksHigh = []
chunksLow = []

while dataHigh != b'':
    chunksHigh.append(dataHigh)
    dataHigh = wfHigh.readframes(chunk)

while dataLow != b'':
    chunksLow.append(dataLow)
    dataLow = wfLow.readframes(chunk)

sizHigh = len(chunksHigh)
sizLow = len(chunksLow)

time.sleep(3)

frameSizeHigh = metadataHigh[0] * metadataHigh[1]
frameSizeLow = metadataLow[0] * metadataLow[1]
frameCountPerChunkHigh = chunk / frameSizeHigh
frameCountPerChunkLow = chunk / frameSizeLow

chunkTimeHigh = 1000 * frameCountPerChunkHigh / metadataHigh[2]
chunkTimeLow = 1000 * frameCountPerChunkLow / metadataLow[2]

tLow = Thread(target=sendLowPacket, args=(sizLow, chunkTimeLow, chunksLow, receiver), daemon=True)
tLow.start()

for i in range(sizHigh):
    startTime = time.time() * 1000
    # print("packet pengiriman ke ", i)
    dataPacket = b''
    if(i == sizHigh - 1):
        dataPacket = lib.createPacket("DATA", chunksHigh[i], 1, seqnum=i)
    else:
        dataPacket = lib.createPacket("DATA", chunksHigh[i], seqnum=i)
    for addr in subscribersHigh:
        sendPacket(receiver, dataPacket, addr)

    endTime = time.time() * 1000
    delta = endTime - startTime
    if(delta < chunkTimeHigh):
        time.sleep((chunkTimeHigh - delta) / 1000)
