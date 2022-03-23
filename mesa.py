# hello_world.py

import PySimpleGUI as sg
import os, signal

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse("examples"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

#layout = [sg.Column(file_list_column), 
 #         [sg.Button("Quit")]]

# Create the window
window = sg.Window("Mesa Library", file_list_column)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Run":
        # open a child process
        #pid = os.fork()
        # move to model
        os.system("./run_examples/run_ex.sh boid_flockers")
        # run model
        #if event == "Stop":
            #os.kill(pid, signal.SIGSTOP)
    if event == "Quit"  or event == sg.WIN_CLOSED:
        break

window.close()
