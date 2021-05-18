

# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------


from simple_pyspin import Camera
import matplotlib.pyplot as plt
import numpy as np


# -----------------------------------------------------------------------------
#   Parameters
# -----------------------------------------------------------------------------


IMAGE_INTERVAL = 0.001


# -----------------------------------------------------------------------------
#   Control Code
# -----------------------------------------------------------------------------


def getImages():
    """
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
