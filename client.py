import socket 
import lib
import time
import pyaudio
import queue
from threading import Thread

q = queue.Queue()

#Input from user
address = input("masukkan IP address server")
port = int(input("masukkan port"))
addr = (address, port)

def client_listener(sock, q):
    run = True
    while(run):
        print("Listen for audio chunk")
        try:
            data, _ = sock.recvfrom(buffSize)
            typ, payload = lib.breakPacket(data)

            if(typ == "DATA"):
                q.put(payload)
            else:
                print("tereter")
                q.put(payload)
                run = False
                break
        except:
            print("error")

        if(time.time() > timeout):
            break

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


t = Thread(target = client_listener, args = (sock, q))
t.start()

while True:
    stream.write(q.get())
    q.task_done()



