# hello_world.py

import PySimpleGUI as sg
import os

layout = [[sg.Text("Boid Flockers")], [sg.Button("Run"), sg.Button("Quit")]]

# Create the window
window = sg.Window("Mes Library", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Run":
        # move to model
        os.system("python examples/boid_flockers/run.py")
        # run model
    if event == "Quit"  or event == sg.WIN_CLOSED:
        break

window.close()
