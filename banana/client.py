import socket
from typing import Tuple 
import lib
import time
import pyaudio
import queue
from threading import Thread


# Function for initializing the socket
def initialize_socket(time_limit=300) -> Tuple[socket.socket, queue.Queue, float]:

    # Setup socket and timeout, using Datagram Sockets
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Initialize thread-safe queue
    q = queue.Queue()

    # Calculate timeout
    timeout = time.time() + time_limit

    return [sock, q, timeout]

# Listener function for client
def client_listener(sock: socket.socket, q: queue.Queue, timeout: int, buff_size: int = 32774):
    run = True
    while(run):
        print("Listen for audio chunk")
        try:
            data, _ = sock.recvfrom(buff_size)
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

# Subscribe to a audio server
def subscribe(addr: Tuple[str, int], sock : socket.socket, q:queue.Queue, timeout: int, buff_size = 32774):

    # Create subscription packet to server
    subPacket = lib.createPacket("SUB", "")

    # WAV related data
    sampwidth = 0
    nchannel = 0
    framerate = 0

    # Wait for META packet
    run = True
    while(run):
        sock.sendto(subPacket, addr)
        print("Waiting for META")
        sock.settimeout(2)
        try:
            fromreceiver, _ = sock.recvfrom(buff_size)
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
            print("Timeout! Retrying...")
        except ConnectionResetError:
            print("No receiver detected, resending packet")
            time.sleep(1)

        if(time.time() > timeout):
            break

    return [sampwidth, nchannel, framerate]


# Play Audio
def play_audio(sampwidth: int, nchannel: int, framerate: int, q: queue.Queue):
    # Initialize PyAudio instance
    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format = p.get_format_from_width(sampwidth),
                    channels = nchannel,
                    rate = framerate,
                    output = True)

    while True:
        # v = q.get()
        # print(v)
        stream.write(q.get())
        q.task_done()
        

# t = Thread(target = client_listener, args = (sock, q))
# t.start()




