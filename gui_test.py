from time import time
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
from threading import Thread
from banana.client import client_listener, initialize_socket, play_audio, subscribe

fr, fc, fn = 0, 0, ''

def start_listener():
    global fr
    global fc
    global fn
    global window

    sock, q, timeout = initialize_socket()
    sampwidth, nchannel, framerate, frame_count, filename = subscribe(addr, sock, q, timeout)
    fr, fc, fn = framerate, frame_count, filename

    window['-FILENAME-'].update(fn)
    window['-LENGTH-'].update(fc//fr)


    listener_thread = Thread(target=client_listener, args=(sock,q,timeout), daemon=True)
    listener_thread.start()
    play_audio(sampwidth,nchannel, framerate, q)

# Input from user
ip_address = input()
port = int(input())
addr = (ip_address, port)

layout = [
    [sg.Text('Audio played:'), sg.Text(size=(15,1), key='-FILENAME-')],
    [sg.Text(size=(15,1),key='-LENGTH-')]
]

window = sg.Window('Audio Client', layout)

# Start audio thread for playing music
audio_thread = Thread(target=start_listener, daemon=True)
audio_thread.start()

while True:
    event, _ = window.read()

    # If window is closed, break from main loop
    if event == WIN_CLOSED:
        break
    


# Close the window
window.close()