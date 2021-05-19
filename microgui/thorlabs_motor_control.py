"""
THORLAB motor integration.

This script allows a user to interface with the THORLAB motor that defines the
horizontal microscope mode.
"""


import thorlabs_apt as apt


TRANSMISSION_POSITION = 36
REFLECTION_POSITION = 47
VISIBLE_IMAGE_POSITION = 0
BEAMSPLITTER_POSITION = 18


def initMotor():
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
    modeMotor : Motor object defined by thorlabs_apt.
    """
    motorSerialNumber = apt.list_available_devices()[0][1]
    modeMotor = apt.Motor(motorSerialNumber)
    modeMotor.enable
    modeMotor.move_home(True)

    return modeMotor


def changeMode(mode, modeMotor):
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

    Returns
    -------
    None

    Usage
    -----
    Must have initiated motor type using defineMotor().
    """
    if mode == 1:
        x = TRANSMISSION_POSITION
    elif mode == 2:
        x = REFLECTION_POSITION
    elif mode == 3:
        x = VISIBLE_IMAGE_POSITION
    else:
        x = BEAMSPLITTER_POSITION

    modeMotor.move_to(value=x, blocking=False)


# -----------------------------------------------------------------------------
#   Simulation
# -----------------------------------------------------------------------------


def initMotorTEST():
    return None