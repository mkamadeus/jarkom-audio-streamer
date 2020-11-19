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

    sock, q, timeout = initialize_socket()
    sampwidth, nchannel, framerate, frame_count, filename = subscribe(addr, sock, q, timeout)
    fr, fc, fn = framerate, frame_count, filename

    listener_thread = Thread(target=client_listener, args=(sock,q,timeout), daemon=True)
    listener_thread.start()
    play_audio(sampwidth,nchannel, framerate, q)

# Input from user
ip_address = input()
port = int(input())
addr = (ip_address, port)

layout = [
    [sg.Text('Audio played:'), sg.Text(auto_size_text=True, key='-FILENAME-')],
    [sg.Text(auto_size_text=True,key='-LENGTH-')]
]

window = sg.Window('Audio Client', layout)

# Start audio thread for playing music
audio_thread = Thread(target=start_listener, daemon=True)
audio_thread.start()

while True:
    event, _ = window.read()

    print('pisang', fn, fc, fr)
    # If window is closed, break from main loop
    if event == WIN_CLOSED:
        break
    
    window['-FILENAME-'].update(fn)
    window['-LENGTH-'].update(fc//fr)
    time.sleep(1)


# Close the window
window.close()