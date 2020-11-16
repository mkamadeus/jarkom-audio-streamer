import socket 
import sys 
import lib
import time
import random
import pyaudio
import wave

#Input from user
address = input("masukkan IP address server")
port = int(input("masukkan port"))
addr = (address, port)

buffSize = 32767 + 7
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
timeout = time.time() + 60*5

subPacket = lib.createPacket("SUB", "")

sampwidth = 0
nchannel = 0
framerate = 0

run = True
while(run):
    sock.sendto(subPacket, addr)
    print("menunggu...")
    sock.settimeout(2)
    try:
        fromreceiver, _ = sock.recvfrom(buffSize)
        typ, data = lib.breakPacket(fromreceiver)
        print(typ)
        print(data)
        if(typ == "META"):
            sampwidth = data[0]
            nchannel = data[1]
            framerate = data[2]
            print(framerate)
            run = False
            break

    except socket.timeout:
        print("Timeout! Ulang")
    except ConnectionResetError:
        print("belom ada receiver, kirim ulang")
        time.sleep(1)
    if(time.time() > timeout):
        break

p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format = p.get_format_from_width(sampwidth),
                channels = nchannel,
                rate = framerate,
                output = True)

queue = []

ptr = 0

while(True):
    print("Hello from receiver")
    try:
        data, _ = sock.recvfrom(buffSize)
        typ, payload = lib.breakPacket(data)

        if(typ == "DATA"):
            print("playdong")
            queue.append(payload)
            stream.write(queue[ptr])
            ptr += 1
    except:
        print("error")

    if(time.time() > timeout):
        break


