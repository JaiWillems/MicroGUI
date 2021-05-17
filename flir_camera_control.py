

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


global FIGURE
FIGURE = plt.figure(1)

def display():
    """
    """
    while 1:
            # Getting the image data as a numpy array
            image_data = getTestImage()

            # Draws an image on the current figure
            plt.imshow(image_data, cmap='gray')

                        # Interval in plt.pause(interval) determines how fast the images are displayed in a GUI
                        # Interval is in seconds.
            plt.pause(0.001)

                        # Clear current reference of a figure. This will improve display speed significantly
            plt.clf()
