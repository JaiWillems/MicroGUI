"""THORLAB motor integration.

This module contains a series of functions to allow the program to interface
with the THORLAB motor that defines the microscope's mode.
"""


import thorlabs_apt as apt


def initMotor() -> apt.Motor:
    """Defines and instantiate the THORLABS motor.

    This function finds the THORLABS motor connected to the local computer and
    initializes it by setting the velocity and acceleration constraints and
    moving the motor to its homed position.

    Returns
    -------
    Motor
        Motor object defined by thorlabs_apt.
    """

    # Find devices connected to the computer.
    devices = apt.list_available_devices()

    # Check a motor is found.
    try:
        motorSerialNumber = devices[0][1]
    except:
        raise Exception("No motor detected. Ensure the device is connected.")

    # Initialize detected motor.
    modeMotor = apt.Motor(motorSerialNumber)

    # Configure motor settings.
    modeMotor.set_move_home_parameters(*modeMotor.get_move_home_parameters())
    modeMotor.set_velocity_parameters(*modeMotor.get_velocity_parameters())

    return modeMotor


def enable(modeMotor: apt.Motor) -> None:
    """Enable THORLABS motor.

    Parameters
    ----------
    modeMotor : Motor
        THORLABS mode motor.

    Notes
    -----
    The THORLABS motor must be enabled before motion control is available.
    """

    modeMotor.enable()


def disable(modeMotor: apt.Motor) -> None:
    """Disable THORLABS motor.

    Parameters
    ----------
    modeMotor : Motor
        THORLABS mode motor.

    Notes
    -----
    The THORLABS motor must be enabled before motion control is available.
    """

    modeMotor.disable()


def home(modeMotor: apt.Motor) -> None:
    """Home THORLABS motor.

    Parameters
    ----------
    modeMotor : Motor
        Motor object representing the modeMotor.

    Notes
    -----
    The THORLABS motor must be enabled before motor homing is available.
    """

    modeMotor.move_home()


def changeMode(pos: int, modeMotor: apt.Motor) -> float:
    """Set the THORLABBS motor position.

    This function allows users to change the microscopes mode of operation by
    altering the THORLABs motor placement.

    Parameters
    ----------
    pos : int
        The position to set the motor to.
    modeMotor : Motor
        THORLABS mode motor.

    Returns
    -------
    float
        A positive value signifies the positon set whereas `-1` indicates an
        error in changing modes.

    Notes
    -----
    The THORLABS motor must be enabled before motion control is available.
    """

    # Try changing motor positions.
    try:
        modeMotor.move_to(value=pos, blocking=False)
        return pos
    except:
        return -1
