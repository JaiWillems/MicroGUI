<<<<<<< HEAD:main.py
"""Instantiate the main GUI.

The main module is responsible for calling the required files and dependencies
to run the FAR-IR horizontal microscope.
"""

# Import package dependencies.
from PyQt5.QtWidgets import QApplication
import sys

# Import file dependencies.
from gui import GUI
from controller import Controller
from thorlabs_motor_control import initMotor

# Define the THORLABS mode stage motor.
modeMotor = initMotor()

# Run the GUI.
app = QApplication([])
gui = GUI()
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(app.exec_())
=======
"""Instantiate the main GUI.

The main module is responsible for calling the required files and dependencies
to run the FAR-IR horizontal microscope.
"""

# Import package dependencies.
from PyQt5.QtWidgets import QApplication
import sys

# Import file dependencies.
from gui import GUI
from controller import Controller
from thorlabs_motor_control import initMotor

# Define the THORLABS mode stage motor.
modeMotor = initMotor()

# Run the GUI.
app = QApplication([])
gui = GUI()
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(app.exec_())
>>>>>>> e4616e3fe17b062fd272cf15e5a6d29a42b621e7:microgui/main.py
