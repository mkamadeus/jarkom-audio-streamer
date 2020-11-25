import time
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
from threading import Thread
from banana.client import client_listener, initialize_socket, play_audio, subscribe

sampwidth, nchannel, framerate, frame_count, filename = 0, 0, 0, 0, ''
ip_address = input()
port = int(input())
addr = (ip_address, port)

def start_client():
    global sampwidth, nchannel, framerate, frame_count, filename
    global addr
    global window

    sock, q = initialize_socket()
    sampwidth, nchannel, framerate, frame_count, filename = subscribe(addr, sock, q)

    window['-FILENAME-'].update(filename)
    window['-LENGTH-'].update('Loading...')

    listener_thread = Thread(target=client_listener, args=(sock,q), daemon=True)
    listener_thread.start()
    play_audio(sampwidth, nchannel, framerate, q, frame_count, window)



layout = [
    [sg.Text('Audio played:'), sg.Text(size=(15,1), key='-FILENAME-')],
    [sg.Text(size=(15,1),key='-LENGTH-')]
]

try:
    window = sg.Window('Audio Client', layout, finalize=True)

    audio_thread = Thread(target=start_client, daemon=True)
    audio_thread.start()

    while True:
        event, values = window.read()
        
        # If window is closed, break from main loop
        if event == WIN_CLOSED:
            break
finally:
    window.close()

