"""JSON file handling.

The configuration module handles the load and save functionality of the
programs configuration files.
"""


import json
from typing import Tuple


def load_config(path: str) -> Tuple[dict, dict]:
    """Load configuration file.

    Parameters
    ----------
    path : str
        Path to configuration file to upload.

    Returns
    -------
    dict
        Configuration data in nested dictionary format.
    dict
        Macro parameters in a dictionary format.
    """
    with open(path, "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    macros = {}
    init_macros(data, macros)

    return data, macros


def save_config(path: str, data: dict, macros: dict) -> None:
    """Save configuration file data.

    Parameters
    ----------
    path : str
        Path to saved configuration file.
    data : dict
        Imported data in nested dictionary format.
    macros : dict
        Macro parameters in macro format.
    """
    condense_macros(data, macros)
    with open(path, "w") as jsonfile:
        myJSON = json.dumps(data, indent=4)
        jsonfile.write(myJSON)


def init_macros(baseDict: dict, macroDict: dict) -> None:
    """Initialize macro variables.

    This function transforms, in place, a nested dictionary into a planar
    dictionary.

    Parameters
    ----------
    baseDict : dict
        Nested dictionary of values.
    macroDict : dict
        New planar dictionary to add key/value pairs to from `baseDict`.
    """
    keys = baseDict.keys()
    for key in keys:
        try:
            init_macros(baseDict[key], macroDict)
        except:
            macroDict[key] = baseDict[key]


def condense_macros(baseDict: dict, macroDict: dict) -> None:
    """Save macro variables.

    This function updates the values of a nested dictionary from the a planar
    dictionary with common keys.

    Parameters
    ----------
    baseDict : dict
        Nested dictionary of values.
    macroDict : dict
        New planar dictionary to add key/value pairs to from `baseDict`.
    """
    keys = baseDict.keys()
    for key in keys:
        try:
            condense_macros(baseDict[key], macroDict)
        except:
            baseDict[key] = macroDict[key]


def load_pos_config(path: str) -> dict:
    """Load the saved positions configuration file.

    Parameters
    ----------
    path : str
        Path to the file to load.
    
    Returns
    -------
    dict
        Dictionary with position labels as keys and a dictionary of positions
        as values.
    """
    with open(path, "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

    return data


def save_pos_config(path: str, data: dict) -> None:
    """Save the current saved positions to the saved positions configuration
    file.

    Parameters
    ----------
    path : str
        Path to save the file to.
    dict
        Dictionary with position labels as keys and a dictionary of positions
        as values.
    """
    with open(path, "w") as jsonfile:
        myJSON = json.dumps(data, indent=4)
        jsonfile.write(myJSON)
