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

    # # Calculate timeout
    # timeout = time.time() + time_limit

    return [sock, q]


# Listener function for client
def client_listener(sock: socket.socket, q: queue.Queue, time_limit: int = 300, buff_size: int = 32774):
    
    timeout = time.time() + time_limit
    while(time.time() <= timeout):
        print("Listen for audio chunk")
        try:
            data, _ = sock.recvfrom(buff_size)
            typ, payload = lib.breakPacket(data)


            if(typ == "DATA"):
                print('hehe')
                q.put(payload.copy())
            else:
                print("tereter")
                q.put(payload.copy())
                return
        except:
            print("error")


# Subscribe to a audio server
def subscribe(addr: Tuple[str, int], sock: socket.socket, q: queue.Queue, time_limit: int = 300, buff_size=32774):

    # Create subscription packet to server
    subPacket = lib.createPacket("SUB", "")

    # WAV related data
    # [sampwidth, nchannel, framerate, frame_count, filename]
    wav_metadata = []

    # Wait for META packet
    timeout = time.time() + time_limit
    while(time.time() <= timeout):
        # Send SUB (0x2) packet to server
        sock.sendto(subPacket, addr)

        print("Waiting for META")
        sock.settimeout(2)
        try:
            # Receive packet from server
            fromreceiver, _ = sock.recvfrom(buff_size)
            typ, data = lib.breakPacket(fromreceiver)
            
            # If received packet has type META (0x1)
            if(typ == "META"):
                wav_metadata = data
                return wav_metadata

        except socket.timeout:
            print("Timeout! Retrying...")
        except ConnectionResetError:
            print("No receiver detected, resending packet")
            time.sleep(1)


    return wav_metadata


# Stream audio
def play_audio(sampwidth: int, nchannel: int, framerate: int, q: queue.Queue, frame_count, window):
    
    # Initialize PyAudio instance
    p = pyaudio.PyAudio()

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format=p.get_format_from_width(sampwidth),
                    channels=nchannel,
                    rate=framerate,
                    output=True)

    # Stream audio
    while True:
        print('tes')
        seq, chunk = q.get()
        print(seq, chunk)
        window['-LENGTH-'].update(f'{seq//framerate}/{frame_count//framerate}')
        stream.write(chunk)
        q.task_done()


