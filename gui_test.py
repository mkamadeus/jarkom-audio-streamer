import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
from threading import Thread
from banana.client import client_listener, initialize_socket, play_audio, subscribe

def start_listener():
    sock, q, timeout = initialize_socket()
    sampwidth, nchannel, framerate = subscribe(addr, sock, q, timeout)
    listener_thread = Thread(target=client_listener, args=(sock,q,timeout))
    listener_thread.start()
    play_audio(sampwidth,nchannel, framerate, q)

# Input from user
ip_address = input()
port = int(input())
addr = (ip_address, port)

layout = [
    [gui.Text(f'Audio played: xxxxxx.wav')],
    [gui.Text(f'xx:xx/yy:yy')]
]

window = gui.Window('Audio Client', layout)

audio_thread = Thread(target=start_listener, daemon=True)
audio_thread.start()

while True:
    event, _ = window.read()
    if event == WIN_CLOSED:
        break

window.close()


# gui_thread = Thread(target=start_gui)
# gui_thread.start()


# gui_thread.join()
# audio_thread.join()