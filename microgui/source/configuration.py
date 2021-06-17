"""JSON file handling.

The configuration module handles the load and save functionality of the
programs configuration files.
"""


import json
from typing import Dict


def load_config(path: str) -> Dict:
    """Load configuration file.

    Parameters
    ----------
    path : str
        Path to configuration file to upload.

    Returns
    -------
    Dict
        Configuration data in nested dictionary format.
    Dict
        Macro parameters in a dictionary format.
    """
    with open(path, "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    macros = {}
    init_macros(data, macros)

    return data, macros


def save_config(path: str, data: Dict, macros: Dict) -> None:
    """Save configuration file data.

    Parameters
    ----------
    path : str
        Path to saved configuration file.
    data : Dict
        Imported data in nested dictionary format.
    macros : Dict
        Macro parameters in macro format.
    """
    condense_macros(data, macros)
    with open(path, "w") as jsonfile:
        myJSON = json.dumps(data, indent=4)
        jsonfile.write(myJSON)


def init_macros(baseDict: Dict, macroDict: Dict) -> None:
    """Initialize macro variables.

    This function transforms, in place, a nested dictionary into a planar
    dictionary.

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
            init_macros(baseDict[key], macroDict)
        except:
            macroDict[key] = baseDict[key]


def condense_macros(baseDict: Dict, macroDict: Dict) -> None:
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
            condense_macros(baseDict[key], macroDict)
        except:
            baseDict[key] = macroDict[key]
