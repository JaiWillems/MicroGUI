"""Create the interactive user interface.

This module is responsible for calling the required files and dependencies
to run the FAR-IR horizontal microscope.
"""


from configuration import load_config, load_pos_config, load_pos_config
from controller import Controller
from epics import PV
from gui import GUI
from PyQt5.QtWidgets import QApplication
from thorlabs_motor_control import initMotor
import sys


# Define the THORLABS motor.
modeMotor = initMotor()


# Define macro variables.
data, macros = load_config("config.json")
savedPos = load_pos_config("saved_positions.json")


def program_exit(gui: GUI) -> None:
    """Exit the MicroGUI program.

    This function exits the MicroGUI program and stops all sample and objective
    stage motors in the case that the program is closed during motion.

    Parameters
    ----------
    gui : GUI
        Gui containing macro information of the STOP process variable names.
    
    Notes
    -----
    This exit function is not called when the program crashes in which case,
    the motors will move to the soft limits.
    """

    app.exec_()

    # Stop each motor.
    for object in ["S", "O"]:
        for axis in ["X", "Y", "Z"]:
            pvStop = PV(gui.macros[f"{axis}{object}STOP"])
            pvStop.put(1)
            pvStop.put(0)


# Start GUI execution.
app = QApplication([])
app.setStyle("Windows")
gui = GUI(data=data, macros=macros, savedPos=savedPos)
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(program_exit(gui))
