import PySimpleGUI as gui
from threading import Thread
from PySimpleGUI.PySimpleGUI import WIN_CLOSED

def start_gui():
    layout = [
        [gui.Text(f'Audio played: xxxxxx.wav')],
        [gui.Text(f'xx:xx/yy:yy')]
    ]

    window = gui.Window('Audio Client', layout)

    while True:
        event, values = window.read()
        if event == WIN_CLOSED:
            break

    window.close()

gui_thread = Thread(target=start_gui)
gui_thread.start()
gui_thread.join()
