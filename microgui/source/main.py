"""Instantiate the main GUI.

The main module is responsible for calling the required files and dependencies
to run the FAR-IR horizontal microscope.
"""

# Import package dependencies.
from PyQt5.QtWidgets import QApplication
import sys
import json
from typing import Dict

# Import file dependencies.
from gui import GUI
from controller import Controller
from thorlabs_motor_control import initMotor
from configuration import load_config

# Define the THORLABS mode stage motor.
modeMotor = initMotor()

# Define macro variables.
data, macros = load_config("config.json")

# Run the GUI.
app = QApplication([])
app.setStyle("Windows")
gui = GUI(data=data, macros=macros)
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(app.exec_())
