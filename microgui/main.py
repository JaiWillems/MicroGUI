"""Instantiate the main GUI.

The main module is responsible for calling the required files and dependencies
to run the FAR-IR horizontal microscope.
"""

# Import package dependencies.
from PyQt5.QtWidgets import QApplication
import sys
import epics
import thorlabs_apt as apt

# Import file dependencies.
from gui import GUI
from controller import Controller
from thorlabs_motor_control import initMotor

# Set up epics environment.
epics.ca.find_libca()

# Define the THORLABS mode stage motor.
#modeMotor = initMotor()
try:
    motorSerialNumber = apt.list_available_devices()[0][1]
except:
    raise Exception("No motor detected. Ensure the device is connected.")

modeMotor = apt.Motor(motorSerialNumber)
modeMotor.enable

try:
    modeMotor.move_home()
except:
    raise Exception("Motor cannot be homed.")

# Run the GUI.
app = QApplication([])
gui = GUI()
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(app.exec_())
