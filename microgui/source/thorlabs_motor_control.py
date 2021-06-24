"""THORLAB motor integration.

This script allows a user to interface with the THORLAB motor that defines the
horizontal microscope mode.
"""


import thorlabs_apt as apt


def initMotor() -> apt.Motor:
    """
    Defines and instantiates the mode motor.

    This function finds a THORLABS motor connected to the computer and
    initiates the velocity and acceleration constraints. Additionally, the
    motor will be moved to the homing position.

    Returns
    -------
    Motor
        Motor object defined by thorlabs_apt.
    """

    devices = apt.list_available_devices()

    try:
        motorSerialNumber = devices[0][1]
    except:
        raise Exception("No motor detected. Ensure the device is connected.")

    # Initialize motor if detected.
    modeMotor = apt.Motor(motorSerialNumber)
    
    return modeMotor


def enable(modeMotor: apt.Motor) -> None:
    """Enable THORLABS motor.

    Parameters
    ----------
    modeMotor : Motor
        Motor object representing the modeMotor.
    """
    modeMotor.set_move_home_parameters(*modeMotor.get_move_home_parameters())
    modeMotor.set_velocity_parameters(*modeMotor.get_velocity_parameters())
    modeMotor.enable()


def disable(modeMotor: apt.Motor) -> None:
    """Enable THORLABS motor.

    Parameters
    ----------
    modeMotor : Motor
        Motor object representing the modeMotor.
    """
    modeMotor.disable()


def home(modeMotor: apt.Motor) -> None:
    """Home THORLABS motor.

    Parameters
    ----------
    modeMotor : Motor
        Motor object representing the modeMotor.
    """
    modeMotor.move_home()


def changeMode(pos: int, modeMotor: apt.Motor) -> float:
    """
    Change THORLAB motor position by pre-set ammount.

    This function allows users to change the microscopes mode of operation by
    altering THORLAB motor placement.

    Parameters
    ----------
    pos : int
        The position to move to corresponding to one of the four modes:
        transmission, reflection, visible image, and the beamsplitter mode.
    modeMotor : Motor
        Motor object to change the mode of.

    Returns
    -------
    float
        A positive value signifies the positon moved to whereas `-1` indicates
        error in changing modes.

    Notes
    -----
    modeMotor must have been initiated using initMotor().
    """
    try:
        modeMotor.move_to(value=pos, blocking=False)
        return pos
    except:
        return -1
