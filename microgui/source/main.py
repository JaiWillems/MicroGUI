"""Instantiate the main GUI.

The main module is responsible for calling the required files and dependencies
to run the FAR-IR horizontal microscope.
"""

# Import package dependencies.
from PyQt5.QtWidgets import QApplication
from epics import PV
import sys

# Import file dependencies.
from gui import GUI
from controller import Controller
from thorlabs_motor_control import initMotor
from configuration import load_config, load_pos_config, load_pos_config

# Define the THORLABS "mode" motor.
modeMotor = initMotor()

# Define macro variables.
data, macros = load_config("config.json")
savedPos = load_pos_config("saved_positions.json")


def program_exit(gui: GUI) -> None:
    """Exit the MicroGUI project.

    This program exits the MicroGUI projects and stops all sample and objective
    stage motors in the case that the program is closed during operation.

    Parameters
    ----------
    gui : GUI
        Gui containing macro information of the STOP PV names.
    """
    app.exec_()
    for object in ["S", "O"]:
        for axis in ["X", "Y", "Z"]:
            pv = PV(gui.macros[f"{axis}{object}STOP"])
            pv.put(1)
            pv.put(0)


# Start GUI execution.
app = QApplication([])
app.setStyle("Windows")
gui = GUI(data=data, macros=macros, savedPos=savedPos)
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(program_exit(gui))
