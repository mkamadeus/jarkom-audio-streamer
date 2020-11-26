import os
from typing import List, Tuple
import socket
import lib
import time
import pyaudio
import queue
import traceback
import logging
from threading import Thread

logging.basicConfig(format='[%(asctime)s.%(msecs)03d] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


# Function for initializing the socket
def initialize_socket() -> Tuple[socket.socket, queue.Queue, float]:

    # Setup socket and timeout, using Datagram Sockets
    logging.info('Setting up socket and packet queue')
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


    # Initialize thread-safe queue
    q = queue.Queue()

    return [sock, q]


# Listener function for client
def client_listener(sock: socket.socket, q: queue.Queue, time_limit: int = 300, buff_size: int = 32774):
    
    timeout = time.time() + time_limit
    logging.info('Listening to server')

    while(time.time() <= timeout):
        logging.debug("Listening for audio chunk")
        try:
            data, _ = sock.recvfrom(buff_size)
            typ, payload = lib.breakPacket(data)


            if(typ == "DATA"):
                logging.debug(f"Received packet {payload[0]//1000}")
                q.put(payload.copy())
            else:
                logging.debug(f'FIN packet found at  {payload[0]//1000}')
                q.put(payload.copy())
                return

        except Exception as e:
            logging.error(traceback.format_exc())

# Subscribe to a audio server
def subscribe(addr: Tuple[str, int], sock: socket.socket, q: queue.Queue, time_limit: int = 300, buff_size=32774):

    # Get port from adress
    port = addr[1]
    new_addr : Tuple[str, int]

    # Autodiscover using broadcast
    que = queue.Queue()
    discovered = False
    while not discovered:
        try:
            sock.sendto(lib.createPacket("ANC", ''), ('<broadcast>', port))
            sock.settimeout(0.2)
            logging.info(f'Broadcasted packet to port {port}')

            fromreceiver, ad = sock.recvfrom(buff_size)
            typ, _ = lib.breakPacket(fromreceiver)
            discovered = True
            logging.info(f'Received from {ad[0]}')

            if(typ == 'ANC'):
                que.put(ad)
                que.task_done()
        except Exception as e:
            print(e)
            pass

    if(que.empty()):
        logging.info('No server was found')
        exit()

    new_addr = que.get()
    logging.info(f'Server found at {new_addr[0]}:{new_addr[1]}')

    # Create subscription packet to server
    subPacket = lib.createPacket("SUB", "")

    # WAV related data [sampwidth, nchannel, framerate, frame_count, filename]
    wav_metadata = []

    # Wait for META (0x1) packet
    timeout = time.time() + time_limit
    logging.info(f'Getting information from {new_addr[0]}:{new_addr[1]}')
    while(time.time() <= timeout):
        # Send SUB (0x2) packet to server
        sock.sendto(subPacket, new_addr)

        logging.debug("Waiting for audio metadata")
        sock.settimeout(2)
        try:
            # Receive packet from server
            fromreceiver, _ = sock.recvfrom(buff_size)
            typ, data = lib.breakPacket(fromreceiver)
            
            # If received packet has type META (0x1)
            if(typ == "META"):
                logging.debug('Metadata received')
                wav_metadata = data.copy()
                return wav_metadata

        except socket.timeout:
            logging.warning("Timeout!")
        except ConnectionResetError:
            logging.warning("No receiver detected!")
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
        seq, chunk = q.get()
        stream.write(chunk)
        q.task_done()

        current_time = seq//framerate
        current_time_string = "{:02d}:{:02d}".format(current_time//60,current_time%60)
        max_time = frame_count//framerate
        max_time_string = "{:02d}:{:02d}".format(max_time//60,max_time%60)

        window['-LENGTH-'].update(f'{current_time_string}/{max_time_string}')
        


