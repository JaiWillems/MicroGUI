"""JSON file handling.

This module contains a series of functions to handle the load and save
functionality of program configuration files.
"""


from typing import Tuple
import json


def load_config(path: str) -> Tuple[dict, dict]:
    """Load configuration file.

    Parameters
    ----------
    path : str
        Path to the configuration file to upload.

    Returns
    -------
    dict
        Configuration data in nested dictionary format.
    dict
        Macro parameters in a dictionary format.
    
    Notes
    -----
    This function uploads the data from a `.json` configuration file in a
    nested dictionary format. It then transforms the data into a linear
    dictionary which it returns.
    """

    # Load configuration file data.
    with open(path, "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

    # Convert dictionary from nested to linear.
    macros = {}
    init_macros(data, macros)

    return data, macros


def save_config(path: str, data: dict, macros: dict) -> None:
    """Save data to a configuration file.

    Parameters
    ----------
    path : str
        Path defining where to save the configuration file.
    data : dict
        Imported data in nested dictionary format.
    macros : dict
        Macro parameters in linear format.

    Notes
    -----
    This functions takes a linear dictionary and a nested dictionary to update
    the nested dictionary values before saving the configuration file.
    """

    # Convert linear dictionary to a nested dictionary.
    condense_macros(data, macros)

    # Save data as a configuration file.
    with open(path, "w") as jsonfile:
        myJSON = json.dumps(data, indent=4)
        jsonfile.write(myJSON)


def init_macros(baseDict: dict, macroDict: dict) -> None:
    """Initialize macro variables.

    This function transforms a nested dictionary into a planar dictionary for
    macro return.

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

    This function updates the values of a nested dictionary from the values of
    a planar dictionary with common keys.

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
        Dictionary with position labels as the keys and a dictionary of the
        corresponding positions as values.
    """

    with open(path, "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()

    return data


def save_pos_config(path: str, data: dict) -> None:
    """Save positions to the saved positions configuration file.

    Parameters
    ----------
    path : str
        Path to save the file to.
    dict
        Dictionary with position labels as the keys and a dictionary of the
        positions positions as values.
    """

    with open(path, "w") as jsonfile:
        myJSON = json.dumps(data, indent=4)
        jsonfile.write(myJSON)
