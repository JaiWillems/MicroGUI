"""THORLAB motor integration.

This script allows a user to interface with the THORLAB motor that defines the
horizontal microscope mode.
"""


import thorlabs_apt as apt
from thorlabs_apt import Motor


TRANSMISSION_POSITION = 36
REFLECTION_POSITION = 47
VISIBLE_IMAGE_POSITION = 0
BEAMSPLITTER_POSITION = 18


def initMotor() -> Motor:
    """
    Defines and instantiates the mode motor.

    This function finds a THORLABS motor connected to the computer and
    initiates the velocity and acceleration constraints. Additionally, the
    motor will be moved to the homing position.

    Parameters
    ----------
    None

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
    modeMotor.set_move_home_parameters(*modeMotor.get_move_home_parameters())
    modeMotor.set_velocity_parameters(*modeMotor.get_velocity_parameters())
    modeMotor.enable()

    try:
        modeMotor.move_home(True)
    except:
        raise Exception("Motor cannot be homed.")

    return modeMotor


def changeMode(mode: int, modeMotor: Motor) -> None:
    """
    Change THORLAB motor position by pre-set ammount.

    This function allows users to change the microscopes mode of operation by
    altering THORLAB motor placement.

    Parameters
    ----------
    mode : int
        The mode values correspond to one of the four microscope modes where
        mode=1 -> Transmission mode, mode=2 -> Reflection mode, mode=3 ->
        Visible Image Mode, and mode=4 -> Beamsplitter Mode.
    modeMotor : Motor
        Motor object to change the mode of.

    Returns
    -------
    None

    Notes
    -----
    modeMotor must have been initiated using initMotor().
    """
    # Set move_to position based on mode.
    if mode == 1:
        pos = TRANSMISSION_POSITION
    elif mode == 2:
        pos = REFLECTION_POSITION
    elif mode == 3:
        pos = VISIBLE_IMAGE_POSITION
    else:
        pos = BEAMSPLITTER_POSITION

    modeMotor.move_to(value=pos, blocking=False) 
