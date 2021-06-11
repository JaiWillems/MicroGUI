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

# Define the THORLABS mode stage motor.
modeMotor = initMotor()


def initMacros(baseDict: Dict, macroDict: Dict) -> None:
    """Initialize macro variables.
    
    This function transforms a nested dictionary into a planar dictionary.

    Parameters
    ----------
    baseDict : Dict
        Nested dictionary of values.
    macroDict : Dict
        New planar dictionary to add key/value pairs to from `baseDict`.
    
    Returns
    -------
    None
    """
    keys = baseDict.keys()
    for key in keys:
        try:
            initMacros(baseDict[key], macroDict)
        except:
            macroDict[key] = baseDict[key]


def saveMacros(baseDict: Dict, macroDict: Dict) -> None:
    """Save macro variables.
    
    This function updates the values of a nested dictionary from the a planar
    dictionary with common keys.

    Parameters
    ----------
    baseDict : Dict
        Nested dictionary of values.
    macroDict : Dict
        New planar dictionary to add key/value pairs to from `baseDict`.
    
    Returns
    -------
    None
    """
    keys = baseDict.keys()
    for key in keys:
        try:
            saveMacros(baseDict[key], macroDict)
        except:
            baseDict[key] = macroDict[key]


def exitGUI(data: Dict, macros: Dict) -> None:
    """Exit the program and save macro variables.

    Parameters
    ----------
    data : Dict
        Nested dictionary of values from `config.json` file.
    macroDict : Dict
        Planar dictionary representing the gui macros attribute.
    
    Returns
    -------
    None
    """
    app.exec_()
    saveMacros(data, macros)
    with open("config.json", "w") as jsonfile:
        myJSON = (json.dumps(data, indent=4))
        jsonfile.write(myJSON)


# Define macro variables.
with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    jsonfile.close()

macros = {}
initMacros(data, macros)

# Run the GUI.
app = QApplication([])
app.setStyle("Windows")
gui = GUI(macros=macros)
gui.show()
Controller(gui=gui, modeMotor=modeMotor)
sys.exit(exitGUI(data, gui.macros))
