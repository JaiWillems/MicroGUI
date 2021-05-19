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

def getTestImageGUI():
    """
    """
    return np.random.randint(0, 255, size=(200, 400, 3)).astype('uint8')

def getDisplay():
    """
    """
    plt.figure(1)

    for i in range(50):
        index = i/25 * np.pi
        image_data = np.sin(np.array([np.linspace(index+0, index+2*np.pi, 400) for n in range(0, 200)]))*255

        plt.imshow(image_data)

        plt.pause(0.001)

        plt.clf()

