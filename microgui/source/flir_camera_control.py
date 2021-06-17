"""FLIR (Point Grey) camera integration.

The flir_camera_control module allows the user to interface with the Blackfly
USB3 camera located within the main GUI display.
"""


from simple_pyspin import Camera
import numpy as np


def get_image() -> np.array:
    """Capture image.

    This function interfaces with a compatible and connected FLIR camera to
    capture an image and return the image data.

    Returns
    -------
    np.array
        Multi-dimensional Numpy array encoding the captured image information.
    """
    with Camera() as cam:

        cam.PixelFormat = "RGB8"

        cam.start()
        image = cam.get_array()
        cam.stop()

    return image
