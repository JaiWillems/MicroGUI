"""Horizontal IR Microscope main GUI file.

Notes
-----
This top level module initiates the GUI for the Far-IR Horizontal Microscope.
"""


from PyQt5.QtWidgets import QApplication
import sys
from gui import GUI
from controller import Controller
from thorlabs_motor_control import defineMotorTEST


modeMotor = defineMotorTEST()

app = QApplication([])
gui = GUI()
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(app.exec_())
