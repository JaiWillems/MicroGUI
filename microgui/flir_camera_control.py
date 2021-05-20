"""FLIR (Point Grey) camera integration.

The flir_camera_control module allows the user to interface with the Blackfly
USB3 camera located within the main GUI display.
"""


from simple_pyspin import Camera
import matplotlib.pyplot as plt
import numpy as np


def getImages():
    """Capture image.

    This function interfaces with a compatible and connected FLIR camera to
    capture an image and return the image data.

    Parameters
    ----------
    None

    Returns
    -------
    nd.array
        Multi-dimensional Numpy array encoding the captured image information.
    """
    with Camera() as cam:

        cam.PixelFormat = "RGB"

        cam.start()
        image = cam.get_array()
        cam.stop()

    return image


# -----------------------------------------------------------------------------
#   Simulation
# -----------------------------------------------------------------------------


def getTestImage():
    """
    """
    return np.random.randint(0, 255, size=(400, 200, 3)).astype('uint8')
