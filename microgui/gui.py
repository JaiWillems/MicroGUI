"""Main GUI display.

The gui module has both the GUI and MyTableWidget class'
responsible for creating the main user interface with the FAR-IR Horizontal
Microscope.
"""

# Import package dependencies.
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from typing import Any, Dict
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRectF, QTimer
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QWidget,\
                            QLabel, QPushButton, QLineEdit, QRadioButton,\
                            QTabWidget

# Import file dependencies.
from flir_camera_control import getTestImage
from globals import *


class GUI(QMainWindow):
    """Main GUI window.

    The GUI class creates the main gui window which allows users to monitor
    and control the main functionality of the microscope.

    Parameters
    ----------
    None

    Attributes
    ----------
    cameraWindow : QWidget
        QWidget window containing camera feed and interface.
    img : pg.ImageItem
        Live feed image from Blackfly camera.
    image : nd.array
        Current image displayed in an array representation.
    WCB : QPushButton
        Image capture push button.
    SIFN : QLineEdit
        File name to label the live feed image capture.
    tab : MyTableWidget object
        The tabular display located on the main GUI window.
    xSN : QPushButton
        Negative incrment button for the Sample's x dimension.
    xSP : QPushButton
        Positive incrment button for the Sample's x dimension.
    xSStep : QLineEdit
        Step size line edit for the sample's x dimension.
    xSAbsPos : QPushButton
        Absolute position button for the sample's x dimension.
    xSMove : QPushButton
        Move to absolute position button for the sample's x dimension.
    xSCn : QPushButton
        Continuous negative motion buttonfor the sample's x dimension.
    xSStop : QPushButton
        Stop continuous motion button for the sample's x dimension.
    xSCp : QPushButton
        Continuous positive motion buttonfor the sample's x dimension.
    xSSn : QLineEdit
        Negative soft limit label for the sample's x dimension.
    xSSp : QLineEdit
        Positive soft limit label for the sample's x dimension.
    xSHn : QLineEdit
        Negative hard limit label for the sample's x dimension.
    xSHp : QLineEdit
        Positive hard limit label for the sample's x dimension.
    ySN : QPushButton
        Negative incrment button for the Sample's y dimension.
    ySP : QPushButton
        Positive incrment button for the Sample's y dimension.
    ySStep : QPushButton
        Step size line edit for the sample's y dimension.
    ySAbsPos : QPushButton
        Absolute position button for the sample's y dimension.
    ySMove : QPushButton
        Move to absolute position button for the sample's y dimension.
    ySCn : QPushButton
        Continuous negative motion buttonfor the sample's y dimension.
    ySStop : QPushButton
        Stop continuous motion button for the sample's y dimension.
    ySCp : QPushButton
        Continuous positive motion buttonfor the sample's y dimension.
    ySSn : QLineEdit
        Negative soft limit label for the sample's y dimension.
    ySSp : QLineEdit
        Positive soft limit label for the sample's y dimension.
    ySHn : QLineEdit
        Negative hard limit label for the sample's y dimension.
    ySHp : QLineEdit
        Positive hard limit label for the sample's y dimension.
    zSN : QPushButton
        Negative incrment button for the Sample's z dimension.
    zSP : QPushButton
        Positive incrment button for the Sample's z dimension.
    zSStep : QLineEdit
        Step size line edit for the sample's z dimension.
    zSAbsPos : QPushButton
        Absolute position button for the sample's z dimension.
    zSMove : QPushButton
        Move to absolute position button for the sample's z dimension.
    zSCn : QPushButton
        Continuous negative motion buttonfor the sample's z dimension.
    zSStop : QPushButton
        Stop continuous motion button for the sample's z dimension.
    zSCp : QPushButton
        Continuous positive motion buttonfor the sample's z dimension.
    zSSn : QLineEdit
        Negative soft limit label for the sample's z dimension.
    zSSp : QLineEdit
        Positive soft limit label for the sample's z dimension.
    zSHn : QLineEdit
        Negative hard limit label for the sample's z dimension.
    zSHp : QLineEdit
        Positive hard limit label for the sample's z dimension.
    xON : QPushButton
        Negative incrment button for the objective' x dimension.
    xOP : QPushButton
        Positive incrment button for the objective' x dimension.
    xOStep : QLineEdit
        Step size line edit for the objective's x dimension.
    xOAbsPos : QPushButton
        Absolute position button for the objective's x dimension.
    xOMove : QPushButton
        Move to absolute position button for the objective's x dimension.
    xOCn : QPushButton
        Continuous negative motion buttonfor the objective's x dimension.
    xOStop : QPushButton
        Stop continuous motion button for the objective's x dimension.
    xOCp : QPushButton
        Continuous positive motion buttonfor the objective's x dimension.
    xOSn : QLineEdit
        Negative soft limit label for the objective's x dimension.
    xOSp : QLineEdit
        Positive soft limit label for the objective's x dimension.
    xOHn : QLineEdit
        Negative hard limit label for the objective's x dimension.
    xOHp : QLineEdit
        Positive hard limit label for the objective's x dimension.
    yON : QPushButton
        Negative incrment button for the objective' y dimension.
    yOP : QPushButton
        Positive incrment button for the objective' y dimension.
    yOStep : QLineEdit
        Step size line edit for the objective's y dimension.
    yOAbsPos : QPushButton
        Absolute position button for the objective's y dimension.
    yOMove : QPushButton
        Move to absolute position button for the objective's y dimension.
    yOCn : QPushButton
        Continuous negative motion buttonfor the objective's y dimension.
    yOStop : QPushButton
        Stop continuous motion button for the objective's y dimension.
    yOCp : QPushButton
        Continuous poditive motion buttonfor the objective's y dimension.
    yOSn : QLineEdit
        Negative soft limit label for the objective's y dimension.
    yOSp : QLineEdit
        Positive soft limit label for the objective's y dimension.
    yOHn : QLineEdit
        Negative hard limit label for the objective's y dimension.
    yOHp : QLineEdit
        Positive hard limit label for the objective's y dimension.
    zON : QPushButton
        Negative incrment button for the objective' z dimension.
    zOP : QPushButton
        Positive incrment button for the objective' z dimension.
    zOStep : QLineEdit
        Step size line edit for the objective's z dimension.
    zOAbsPos : QPushButton
        Absolute position button for the objective's z dimension.
    zOMove : QPushButton
        Move to absolute position button for the objective's z dimension.
    zOCn : QPushButton
        Continuous negative motion buttonfor the objective's z dimension.
    zOStop : QPushButton
        Stop continuous motion button for the objective's z dimension.
    zOCp : QPushButton
        Continuous positive motion buttonfor the objective's z dimension.
    zOSn : QLineEdit
        Negative soft limit label for the objective's z dimension.
    zOSp : QLineEdit
        Positive hard limit label for the objective's z dimension.
    zOHn : QLineEdit
        Negative hard limit label for the objective's z dimension.
    zOHp : QLineEdit
        Positive hard limit label for the objective's z dimension.

    Methods
    -------
    getDiagramWindow()
        Creates the diagram window.
    getCameraWindow()
        Creates the camera window.
    getTabularWindow()
        Creates the table window.
    getSampleWindow()
        Creates the sample window.
    getObjectiveWindow()
        Creates the objective window.
    """

    def __init__(self) -> None:
        """Initialize the GUI."""

        super().__init__()

        # Define main GUI window.
        self.setWindowTitle("Horizontal Microscope Control")
        self.setFixedWidth(1300)
        self.setFixedHeight(525)

        # Add sub-windows to main window layout.
        self.layout = QGridLayout()
        self.layout.addWidget(self.getDiagramWindow(), 0, 0, 2, 1)
        self.layout.addWidget(self.getCameraWindow(), 0, 1, 2, 1)
        self.layout.addWidget(self.getTabularWindow(), 0, 2, 2, 1)
        self.layout.addWidget(self.getSampleWindow(), 2, 0, 1, 3)
        self.layout.addWidget(self.getObjectiveWindow(), 3, 0, 1, 3)

        # Set main window layout.
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

        self.show()

    def getDiagramWindow(self) -> QLabel:
        """Create diagram window.

        Parameters
        ----------
        None

        Returns
        -------
        window : QLabel
            Window representing the diagram display.
        """
        window = QLabel()
        window.setPixmap(QPixmap("example_diagram.jpg"))

        return window

    def getCameraWindow(self) -> QWidget:
        """Create camera window.

        Parameters
        ----------
        None

        Returns
        -------
        window : QWidget
            Window representing the live feed and interactive widgets.
        """
        def updateData() -> None:
            """Update live feed display.

            Parameters
            ----------
            None

            Returns
            -------
            None

            Notes
            -----
            The red cross hair is added by changing the central three rows and
            columns of pixels in the image to red (RGB=[225, 0, 0]).
            """
            # Get new image.
            self.image = getTestImage()
            height = self.image.shape[0]
            width = self.image.shape[1]

            # Generate cross hairs
            xLine = np.full((3, width, 3), [225, 0, 0])
            yLine = np.full((height, 3, 3), [225, 0, 0])
            self.image[height // 2 - 1:height // 2 + 2, :] = xLine
            self.image[:, width // 2 - 1:width // 2 + 2] = yLine

            # Update image.
            self.img.setImage(self.image)
            QTimer.singleShot(1, updateData)

            # Initialize timer.
            now = ptime.time()
            fps2 = 1.0 / (now - self.updateTime)
            self.updateTime = now
            self.fps = self.fps * 0.9 + fps2 * 0.1

        # Configure camera window.
        self.cameraWindow = QWidget()
        pg.setConfigOptions(antialias=True)
        win = pg.GraphicsLayoutWidget()
        self.img = pg.ImageItem(border='w')

        # Create viewing box.
        view = win.addViewBox()
        view.setAspectLocked(True)
        view.addItem(self.img)
        view.setRange(QRectF(0, 0, 400, 200))

        self.updateTime = ptime.time()
        self.fps = 0

        updateData()

        layout = QGridLayout()

        # Create, modify, and place image capture button and line-edit.
        self.WCB = QPushButton("Image Capture")
        self.SIFN = QLineEdit("File Name")
        self.WCB.setStyleSheet("background-color: lightgrey")
        layout.addWidget(win, 0, 0, 1, 2)
        layout.addWidget(self.WCB, 1, 0, 1, 1)
        layout.addWidget(self.SIFN, 1, 1, 1, 1)

        self.cameraWindow.setLayout(layout)

        return self.cameraWindow

    def getTabularWindow(self) -> QWidget:
        """Create tabular window.

        Parameters
        ----------
        None

        Returns
        -------
        tab : MyTableWidget(QWidget)
            Object representing the tabular widget.
        """
        self.tab = MyTableWidget(self)
        return self.tab

    def getSampleWindow(self) -> QWidget:
        """Create sample window.

        Parameters
        ----------
        None

        Returns
        -------
        window : QWidget
            Window representing the sample interactive widgets.
        """
        window = QWidget()
        layout = QGridLayout()

        # Set column labels.
        layout.addWidget(QLabel("<b>Axis</b>"), 0, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 0, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 0, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 0, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 0, 6, 1, 3)
        layout.addWidget(QLabel("<b>Limits</b>"), 0, 9, 1, 4)

        # ---------------------------------------------------------------------
        #   X Sample Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.xSN = QPushButton("-")
        self.xSP = QPushButton("+")
        self.xSStep = QLineEdit("0")
        self.xSAbsPos = QLineEdit("0")
        self.xSMove = QPushButton("MOVE")
        self.xSCn = QPushButton("-")
        self.xSStop = QPushButton("STOP")
        self.xSCp = QPushButton("+")
        self.xSSn = QLabel("Soft -")
        self.xSSp = QLabel("Soft +")
        self.xSHn = QLabel("Hard -")
        self.xSHp = QLabel("Hard +")

        # Style interactive widgets.
        self.xSN.setStyleSheet("background-color: lightgrey")
        self.xSP.setStyleSheet("background-color: lightgrey")
        self.xSMove.setStyleSheet("background-color: lightgrey")
        self.xSCn.setStyleSheet("background-color: lightgrey")
        self.xSStop.setStyleSheet("background-color: red")
        self.xSCp.setStyleSheet("background-color: lightgrey")
        self.xSSn.setStyleSheet("border: 1px solid black;")
        self.xSSp.setStyleSheet("border: 1px solid black;")
        self.xSHn.setStyleSheet("border: 1px solid black;")
        self.xSHp.setStyleSheet("border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("X:"), 1, 0, 1, 1)
        layout.addWidget(self.xSN, 1, 1, 1, 1)
        layout.addWidget(self.xSP, 1, 2, 1, 1)
        layout.addWidget(self.xSStep, 1, 3, 1, 1)
        layout.addWidget(self.xSAbsPos, 1, 4, 1, 1)
        layout.addWidget(self.xSMove, 1, 5, 1, 1)
        layout.addWidget(self.xSCn, 1, 6, 1, 1)
        layout.addWidget(self.xSStop, 1, 7, 1, 1)
        layout.addWidget(self.xSCp, 1, 8, 1, 1)
        layout.addWidget(self.xSSn, 1, 9, 1, 1)
        layout.addWidget(self.xSSp, 1, 10, 1, 1)
        layout.addWidget(self.xSHn, 1, 11, 1, 1)
        layout.addWidget(self.xSHp, 1, 12, 1, 1)

        # ---------------------------------------------------------------------
        #   Y Sample Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.ySN = QPushButton("-")
        self.ySP = QPushButton("+")
        self.ySStep = QLineEdit("0")
        self.ySAbsPos = QLineEdit("0")
        self.ySMove = QPushButton("MOVE")
        self.ySCn = QPushButton("-")
        self.ySStop = QPushButton("STOP")
        self.ySCp = QPushButton("+")
        self.ySSn = QLabel("Soft -")
        self.ySSp = QLabel("Soft +")
        self.ySHn = QLabel("Hard -")
        self.ySHp = QLabel("Hard +")

        # Style interactive widgets.
        self.ySN.setStyleSheet("background-color: lightgrey")
        self.ySP.setStyleSheet("background-color: lightgrey")
        self.ySMove.setStyleSheet("background-color: lightgrey")
        self.ySCn.setStyleSheet("background-color: lightgrey")
        self.ySStop.setStyleSheet("background-color: red")
        self.ySCp.setStyleSheet("background-color: lightgrey")
        self.ySSn.setStyleSheet("border: 1px solid black;")
        self.ySSp.setStyleSheet("border: 1px solid black;")
        self.ySHn.setStyleSheet("border: 1px solid black;")
        self.ySHp.setStyleSheet("border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Y:"), 2, 0, 1, 1)
        layout.addWidget(self.ySN, 2, 1, 1, 1)
        layout.addWidget(self.ySP, 2, 2, 1, 1)
        layout.addWidget(self.ySStep, 2, 3, 1, 1)
        layout.addWidget(self.ySAbsPos, 2, 4, 1, 1)
        layout.addWidget(self.ySMove, 2, 5, 1, 1)
        layout.addWidget(self.ySCn, 2, 6, 1, 1)
        layout.addWidget(self.ySStop, 2, 7, 1, 1)
        layout.addWidget(self.ySCp, 2, 8, 1, 1)
        layout.addWidget(self.ySSn, 2, 9, 1, 1)
        layout.addWidget(self.ySSp, 2, 10, 1, 1)
        layout.addWidget(self.ySHn, 2, 11, 1, 1)
        layout.addWidget(self.ySHp, 2, 12, 1, 1)

        # ---------------------------------------------------------------------
        #   Z Sample Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.zSN = QPushButton("-")
        self.zSP = QPushButton("+")
        self.zSStep = QLineEdit("0")
        self.zSAbsPos = QLineEdit("0")
        self.zSMove = QPushButton("MOVE")
        self.zSCn = QPushButton("-")
        self.zSStop = QPushButton("STOP")
        self.zSCp = QPushButton("+")
        self.zSSn = QLabel("Soft -")
        self.zSSp = QLabel("Soft +")
        self.zSHn = QLabel("Hard -")
        self.zSHp = QLabel("Hard +")

        # Style interactive widgets.
        self.zSN.setStyleSheet("background-color: lightgrey")
        self.zSP.setStyleSheet("background-color: lightgrey")
        self.zSMove.setStyleSheet("background-color: lightgrey")
        self.zSCn.setStyleSheet("background-color: lightgrey")
        self.zSStop.setStyleSheet("background-color: red")
        self.zSCp.setStyleSheet("background-color: lightgrey")
        self.zSSn.setStyleSheet("border: 1px solid black;")
        self.zSSp.setStyleSheet("border: 1px solid black;")
        self.zSHn.setStyleSheet("border: 1px solid black;")
        self.zSHp.setStyleSheet("border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Z:"), 3, 0, 1, 1)
        layout.addWidget(self.zSN, 3, 1, 1, 1)
        layout.addWidget(self.zSP, 3, 2, 1, 1)
        layout.addWidget(self.zSStep, 3, 3, 1, 1)
        layout.addWidget(self.zSAbsPos, 3, 4, 1, 1)
        layout.addWidget(self.zSMove, 3, 5, 1, 1)
        layout.addWidget(self.zSCn, 3, 6, 1, 1)
        layout.addWidget(self.zSStop, 3, 7, 1, 1)
        layout.addWidget(self.zSCp, 3, 8, 1, 1)
        layout.addWidget(self.zSSn, 3, 9, 1, 1)
        layout.addWidget(self.zSSp, 3, 10, 1, 1)
        layout.addWidget(self.zSHn, 3, 11, 1, 1)
        layout.addWidget(self.zSHp, 3, 12, 1, 1)

        # Set window layout.
        window.setLayout(layout)
        return window

    def getObjectiveWindow(self) -> QWidget:
        """Create objective window.

        Parameters
        ----------
        None

        Returns
        -------
        window : QWidget
            Window representing the objective interactive widgets.
        """
        window = QWidget()
        layout = QGridLayout()

        # Set column labels.
        layout.addWidget(QLabel("<b>Axis</b>"), 0, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 0, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 0, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 0, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 0, 6, 1, 3)
        layout.addWidget(QLabel("<b>Limits</b>"), 0, 9, 1, 4)

        # ----------------------------------------------------------------------
        #   X Objective Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.xON = QPushButton("-")
        self.xOP = QPushButton("+")
        self.xOStep = QLineEdit("0")
        self.xOAbsPos = QLineEdit("0")
        self.xOMove = QPushButton("MOVE")
        self.xOCn = QPushButton("-")
        self.xOStop = QPushButton("STOP")
        self.xOCp = QPushButton("+")
        self.xOSn = QLabel("Soft -")
        self.xOSp = QLabel("Soft +")
        self.xOHn = QLabel("Hard -")
        self.xOHp = QLabel("Hard +")

        # Style interactive widgets.
        self.xON.setStyleSheet("background-color: lightgrey")
        self.xOP.setStyleSheet("background-color: lightgrey")
        self.xOMove.setStyleSheet("background-color: lightgrey")
        self.xOCn.setStyleSheet("background-color: lightgrey")
        self.xOStop.setStyleSheet("background-color: red")
        self.xOCp.setStyleSheet("background-color: lightgrey")
        self.xOSn.setStyleSheet("border: 1px solid black;")
        self.xOSp.setStyleSheet("border: 1px solid black;")
        self.xOHn.setStyleSheet("border: 1px solid black;")
        self.xOHp.setStyleSheet("border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("X:"), 1, 0, 1, 1)
        layout.addWidget(self.xON, 1, 1, 1, 1)
        layout.addWidget(self.xOP, 1, 2, 1, 1)
        layout.addWidget(self.xOStep, 1, 3, 1, 1)
        layout.addWidget(self.xOAbsPos, 1, 4, 1, 1)
        layout.addWidget(self.xOMove, 1, 5, 1, 1)
        layout.addWidget(self.xOCn, 1, 6, 1, 1)
        layout.addWidget(self.xOStop, 1, 7, 1, 1)
        layout.addWidget(self.xOCp, 1, 8, 1, 1)
        layout.addWidget(self.xOSn, 1, 9, 1, 1)
        layout.addWidget(self.xOSp, 1, 10, 1, 1)
        layout.addWidget(self.xOHn, 1, 11, 1, 1)
        layout.addWidget(self.xOHp, 1, 12, 1, 1)

        # ---------------------------------------------------------------------
        #   Y Objectivs Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.yON = QPushButton("-")
        self.yOP = QPushButton("+")
        self.yOStep = QLineEdit("0")
        self.yOAbsPos = QLineEdit("0")
        self.yOMove = QPushButton("MOVE")
        self.yOCn = QPushButton("-")
        self.yOStop = QPushButton("STOP")
        self.yOCp = QPushButton("+")
        self.yOSn = QLabel("Soft -")
        self.yOSp = QLabel("Soft +")
        self.yOHn = QLabel("Hard -")
        self.yOHp = QLabel("Hard +")

        # Style interactive widgets.
        self.yON.setStyleSheet("background-color: lightgrey")
        self.yOP.setStyleSheet("background-color: lightgrey")
        self.yOMove.setStyleSheet("background-color: lightgrey")
        self.yOCn.setStyleSheet("background-color: lightgrey")
        self.yOStop.setStyleSheet("background-color: red")
        self.yOCp.setStyleSheet("background-color: lightgrey")
        self.yOSn.setStyleSheet("border: 1px solid black;")
        self.yOSp.setStyleSheet("border: 1px solid black;")
        self.yOHn.setStyleSheet("border: 1px solid black;")
        self.yOHp.setStyleSheet("border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Y:"), 2, 0, 1, 1)
        layout.addWidget(self.yON, 2, 1, 1, 1)
        layout.addWidget(self.yOP, 2, 2, 1, 1)
        layout.addWidget(self.yOStep, 2, 3, 1, 1)
        layout.addWidget(self.yOAbsPos, 2, 4, 1, 1)
        layout.addWidget(self.yOMove, 2, 5, 1, 1)
        layout.addWidget(self.yOCn, 2, 6, 1, 1)
        layout.addWidget(self.yOStop, 2, 7, 1, 1)
        layout.addWidget(self.yOCp, 2, 8, 1, 1)
        layout.addWidget(self.yOSn, 2, 9, 1, 1)
        layout.addWidget(self.yOSp, 2, 10, 1, 1)
        layout.addWidget(self.yOHn, 2, 11, 1, 1)
        layout.addWidget(self.yOHp, 2, 12, 1, 1)

        # ---------------------------------------------------------------------
        #   Z Objective Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.zON = QPushButton("-")
        self.zOP = QPushButton("+")
        self.zOStep = QLineEdit("0")
        self.zOAbsPos = QLineEdit("0")
        self.zOMove = QPushButton("MOVE")
        self.zOCn = QPushButton("-")
        self.zOStop = QPushButton("STOP")
        self.zOCp = QPushButton("+")
        self.zOSn = QLabel("Soft -")
        self.zOSp = QLabel("Soft +")
        self.zOHn = QLabel("Hard -")
        self.zOHp = QLabel("Hard +")

        # Style interactive widgets.
        self.zON.setStyleSheet("background-color: lightgrey")
        self.zOP.setStyleSheet("background-color: lightgrey")
        self.zOMove.setStyleSheet("background-color: lightgrey")
        self.zOCn.setStyleSheet("background-color: lightgrey")
        self.zOStop.setStyleSheet("background-color: red")
        self.zOCp.setStyleSheet("background-color: lightgrey")
        self.zOSn.setStyleSheet("border: 1px solid black;")
        self.zOSp.setStyleSheet("border: 1px solid black;")
        self.zOHn.setStyleSheet("border: 1px solid black;")
        self.zOHp.setStyleSheet("border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Z:"), 3, 0, 1, 1)
        layout.addWidget(self.zON, 3, 1, 1, 1)
        layout.addWidget(self.zOP, 3, 2, 1, 1)
        layout.addWidget(self.zOStep, 3, 3, 1, 1)
        layout.addWidget(self.zOAbsPos, 3, 4, 1, 1)
        layout.addWidget(self.zOMove, 3, 5, 1, 1)
        layout.addWidget(self.zOCn, 3, 6, 1, 1)
        layout.addWidget(self.zOStop, 3, 7, 1, 1)
        layout.addWidget(self.zOCp, 3, 8, 1, 1)
        layout.addWidget(self.zOSn, 3, 9, 1, 1)
        layout.addWidget(self.zOSp, 3, 10, 1, 1)
        layout.addWidget(self.zOHn, 3, 11, 1, 1)
        layout.addWidget(self.zOHp, 3, 12, 1, 1)

        # Set window layout.
        window.setLayout(layout)
        return window


class MyTableWidget(QWidget):
    """GUI table window.

    The MytableWidget class creates the table widget which extends the
    functionality of the main gui window.

    Parameters
    ----------
    parent : Any
        Defines parent object of the MyTableWidget object.

    Attributes
    ----------
    tabs : QTabWidget
        Points to the object defining the table window.
    tab1 : QWidget
        Status tab of the table window.
    tab2 : QWidget
        Mode tab of the table window.
    tab3 : QWidget
        Specifications tab of the table window.
    tab4 : QWidget
        Limits tab of the table window.
    tab5 : QWidget
        Calibration tab of the table window.
    xIdleS : QLabel
        Idle label for the sample's x dimension.
    yIdleS : QLabel
        Idle label for the sample's y dimension.
    zIdleS : QLabel
        Idle label for the sample's z dimension.
    xStopS : QLabel
        In-Motion label for the sample's x dimension.
    yStopS : QLabel
        In-Motion label for the sample's y dimension.
    zStopS : QLabel
        In-Motion label for the sample's z dimension.
    xIdleO : QLabel
        Idle label for the objective's x dimension.
    yIdleO : QLabel
        Idle label for the objective's y dimension.
    zIdleO : QLabel
        Idle label for the objective's z dimension.
    xStopO : QLabel
        In-Motion label for the objective's x dimension.
    yStopO : QLabel
        In-Motion label for the objective's y dimension.
    zStopO : QLabel
        In-Motion label for the objective's z dimension.
    RDM1 : QRadioButton
        Transmission mode radio button.
    RDM2 : QRadioButton
        Reflection mode radio button.
    RDM3 : QRadioButton
        Visible Image mode radio button.
    RDM4 : QRadioButton
        Beamsplitter mode radio button.
    xSMM : QLabel
        Minimum and maximum label for the sample's x dimension.
    ySMM : QLabel
        Minimum and maximum label for the sample's y dimension.
    zSMM : QLabel
        Minimum and maximum label for the sample's z dimension.
    xOMM : QLabel
        Minimum and maximum label for the objective's x dimension.
    yOMM : QLabel
        Minimum and maximum label for the objective's y dimension.
    zOMM : QLabel
        Minimum and maximum label for the objective's z dimension.
    xSMin : QLineEdit
        Soft limit minimum for the sample's x dimension.
    xSMax : QLineEdit
        Soft limit maximum for the sample's x dimension.
    ySMin : QLineEdit
        Soft limit minimum for the sample's y dimension.
    ySMax : QLineEdit
        Soft limit maximum for the sample's y dimension.
    zSMin : QLineEdit
        Soft limit minimum for the sample's z dimension.
    zSMax : QLineEdit
        Soft limit maximum for the sample's z dimension.
    xOMin : QLineEdit
        Soft limit minimum for the objective's x dimension.
    xOMax : QLineEdit
        Soft limit maximum for the objective's x dimension.
    yOMin : QLineEdit
        Soft limit minimum for the objective's y dimension.
    yOMax : QLineEdit
        Soft limit maximum for the objective's y dimension.
    zOMin : QLineEdit
        Soft limit minimum for the objective's z dimension.
    zOMax : QLineEdit
        Soft limit maximum for the objective's z dimension.
    SSL : QPushButton
        Set soft limits button.
    SSL : QPushButton
        Set extreme soft limits button.
    xSZero : QPushButton
        Button to zero the sample's x dimension.
    ySZero : QPushButton
        Button to zero the sample's y dimension.
    zSZero : QPushButton
        Button to zero the sample's z dimension.
    xSB : QLineEdit
        Backlash input for the sample's x dimension.
    ySB : QLineEdit
        Backlash input for the sample's y dimension.
    zSB : QLineEdit
        Backlash input for the sample's z dimension.
    xOZero : QPushButton
        Button to zero the objective's x dimension.
    yOZero : QPushButton
        Button to zero the objective's y dimension.
    zOZero : QPushButton
        Button to zero the objective's z dimension.
    xOB : QLineEdit
        Backlash input for the objective's x dimension.
    yOB : QLineEdit
        Backlash input for the objective's y dimension.
    zOB : QLineEdit
        Backlash input for the objective's z dimension.
    SBL : QPushButton
        Update all backlash values button.

    Methods
    -------
    None
    """

    def __init__(self, parent: Any) -> None:
        """Initialize Class."""

        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Define tab windows.
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        self.tabs.resize(3000, 1000)

        # Add tabs to window layout.
        self.tabs.addTab(self.tab1, "Status")
        self.tabs.addTab(self.tab2, "Mode")
        self.tabs.addTab(self.tab3, "Specifications")
        self.tabs.addTab(self.tab4, "Limits")
        self.tabs.addTab(self.tab5, "Calibration")

        # ---------------------------------------------------------------------
        #   Tab 1
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab1.layout = QGridLayout(self)

        # Define interactive sample widgets.
        self.xIdleS = QLabel("IDLE")
        self.yIdleS = QLabel("IDLE")
        self.zIdleS = QLabel("IDLE")
        self.xStopS = QLabel("In Motion")
        self.yStopS = QLabel("In Motion")
        self.zStopS = QLabel("In Motion")

        # Style interactive sample widgets.
        self.xIdleS.setStyleSheet("border: 1px solid black;")
        self.yIdleS.setStyleSheet("border: 1px solid black;")
        self.zIdleS.setStyleSheet("border: 1px solid black;")
        self.xStopS.setStyleSheet("border: 1px solid black;")
        self.yStopS.setStyleSheet("border: 1px solid black;")
        self.zStopS.setStyleSheet("border: 1px solid black;")

        # Organize sample widgets in the tab layout.
        self.tab1.layout.addWidget(QLabel("<b>Sample</b>"), 0, 1, 1, 3)
        self.tab1.layout.addWidget(QLabel("X:"), 1, 1, 1, 1)
        self.tab1.layout.addWidget(QLabel("Y:"), 2, 1, 1, 1)
        self.tab1.layout.addWidget(QLabel("Z:"), 3, 1, 1, 1)
        self.tab1.layout.addWidget(self.xIdleS, 1, 2, 1, 1)
        self.tab1.layout.addWidget(self.yIdleS, 2, 2, 1, 1)
        self.tab1.layout.addWidget(self.zIdleS, 3, 2, 1, 1)
        self.tab1.layout.addWidget(self.xStopS, 1, 3, 1, 1)
        self.tab1.layout.addWidget(self.yStopS, 2, 3, 1, 1)
        self.tab1.layout.addWidget(self.zStopS, 3, 3, 1, 1)

        # Interactive objective widgets.
        self.xIdleO = QLabel("IDLE")
        self.yIdleO = QLabel("IDLE")
        self.zIdleS = QLabel("IDLE")
        self.xStopO = QLabel("In Motion")
        self.yStopO = QLabel("In Motion")
        self.zStopO = QLabel("In Motion")

        # Style interactive sample widgets.
        self.xIdleO.setStyleSheet("border: 1px solid black;")
        self.yIdleO.setStyleSheet("border: 1px solid black;")
        self.zIdleS.setStyleSheet("border: 1px solid black;")
        self.xStopO.setStyleSheet("border: 1px solid black;")
        self.yStopO.setStyleSheet("border: 1px solid black;")
        self.zStopO.setStyleSheet("border: 1px solid black;")

        # Organize sample widgets in the tab layout.
        self.tab1.layout.addWidget(QLabel("<b>Objective</b>"), 0, 4, 1, 3)
        self.tab1.layout.addWidget(QLabel("X:"), 1, 4, 1, 1)
        self.tab1.layout.addWidget(QLabel("Y:"), 2, 4, 1, 1)
        self.tab1.layout.addWidget(QLabel("Z:"), 3, 4, 1, 1)
        self.tab1.layout.addWidget(self.xIdleO, 1, 5, 1, 1)
        self.tab1.layout.addWidget(self.yIdleO, 2, 5, 1, 1)
        self.tab1.layout.addWidget(self.zIdleS, 3, 5, 1, 1)
        self.tab1.layout.addWidget(self.xStopO, 1, 6, 1, 1)
        self.tab1.layout.addWidget(self.yStopO, 2, 6, 1, 1)
        self.tab1.layout.addWidget(self.zStopO, 3, 6, 1, 1)

        # Set tab layout.
        self.tab1.setLayout(self.tab1.layout)

        # ---------------------------------------------------------------------
        #   Tab 2
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab2.layout = QVBoxLayout()

        # Define mode select buttons.
        self.RDM1 = QRadioButton("Transmission")
        self.RDM2 = QRadioButton("Reflection")
        self.RDM3 = QRadioButton("Visible Image")
        self.RDM4 = QRadioButton("Beamsplitter")

        # Organize widgets on tab layout.
        self.tab2.layout.addWidget(self.RDM1)
        self.tab2.layout.addWidget(self.RDM2)
        self.tab2.layout.addWidget(self.RDM3)
        self.tab2.layout.addWidget(self.RDM4)

        # Set tab layout.
        self.tab2.setLayout(self.tab2.layout)

        # ---------------------------------------------------------------------
        #   Tab 3
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab3.layout = QGridLayout()

        # Define interactive sample widgets.
        self.xSMM = QLabel(f"{XSMIN_HARD_LIMIT} to {XSMAX_HARD_LIMIT}")
        self.ySMM = QLabel(f"{YSMIN_HARD_LIMIT} to {YSMAX_HARD_LIMIT}")
        self.zSMM = QLabel(f"{ZSMIN_HARD_LIMIT} to {ZSMAX_HARD_LIMIT}")

        # Organize sample widgets in the tab layout.
        self.tab3.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 2)
        self.tab3.layout.addWidget(QLabel("<i>Min to Max</i>"), 1, 1, 1, 1)
        self.tab3.layout.addWidget(QLabel("X:"), 2, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("Y:"), 3, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("Z:"), 4, 0, 1, 1)
        self.tab3.layout.addWidget(self.xSMM, 2, 1, 1, 1)
        self.tab3.layout.addWidget(self.ySMM, 3, 1, 1, 1)
        self.tab3.layout.addWidget(self.zSMM, 4, 1, 1, 1)

        # Define interactive objective widgets.
        self.xOMM = QLabel(f"{XOMIN_HARD_LIMIT} to {XOMAX_HARD_LIMIT}")
        self.yOMM = QLabel(f"{YOMIN_HARD_LIMIT} to {YOMAX_HARD_LIMIT}")
        self.zOMM = QLabel(f"{ZOMIN_HARD_LIMIT} to {ZOMAX_HARD_LIMIT}")

        # Organize objective widgets in the tab layout.
        self.tab3.layout.addWidget(QLabel("<b>Objective</b>"), 0, 2, 1, 2)
        self.tab3.layout.addWidget(QLabel("<i>Min to Max</i>"), 1, 3, 1, 1)
        self.tab3.layout.addWidget(QLabel("X:"), 2, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("Y:"), 3, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("Z:"), 4, 2, 1, 1)
        self.tab3.layout.addWidget(self.xOMM, 2, 3, 1, 1)
        self.tab3.layout.addWidget(self.yOMM, 3, 3, 1, 1)
        self.tab3.layout.addWidget(self.zOMM, 4, 3, 1, 1)

        # Set tab layout.
        self.tab3.setLayout(self.tab3.layout)

        # ---------------------------------------------------------------------
        #   Tab 4
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab4.layout = QGridLayout()

        # Define interactive sample widgets.
        self.xSMin = QLineEdit("0")
        self.ySMin = QLineEdit("0")
        self.zSMin = QLineEdit("0")
        self.xSMax = QLineEdit("0")
        self.ySMax = QLineEdit("0")
        self.zSMax = QLineEdit("0")

        # Organize sample widgets in the tab layout.
        self.tab4.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 3)
        self.tab4.layout.addWidget(QLabel("<i>Min</i>"), 1, 1, 1, 1)
        self.tab4.layout.addWidget(QLabel("<i>Max</i>"), 1, 2, 1, 1)
        self.tab4.layout.addWidget(QLabel("X:"), 2, 0, 1, 1)
        self.tab4.layout.addWidget(QLabel("Y:"), 3, 0, 1, 1)
        self.tab4.layout.addWidget(QLabel("Z:"), 4, 0, 1, 1)
        self.tab4.layout.addWidget(self.xSMin, 2, 1, 1, 1)
        self.tab4.layout.addWidget(self.ySMin, 3, 1, 1, 1)
        self.tab4.layout.addWidget(self.zSMin, 4, 1, 1, 1)
        self.tab4.layout.addWidget(self.xSMax, 2, 2, 1, 1)
        self.tab4.layout.addWidget(self.ySMax, 3, 2, 1, 1)
        self.tab4.layout.addWidget(self.zSMax, 4, 2, 1, 1)

        # Define interactive objective widgets.
        self.xOMin = QLineEdit("0")
        self.yOMin = QLineEdit("0")
        self.zOMin = QLineEdit("0")
        self.xOMax = QLineEdit("0")
        self.yOMax = QLineEdit("0")
        self.zOMax = QLineEdit("0")

        # Organize objective widgets in the tab layout.
        self.tab4.layout.addWidget(QLabel("<b>Objective</b>"), 0, 3, 1, 3)
        self.tab4.layout.addWidget(QLabel("<i>Min</i>"), 1, 4, 1, 1)
        self.tab4.layout.addWidget(QLabel("<i>Max</i>"), 1, 5, 1, 1)
        self.tab4.layout.addWidget(QLabel("X:"), 2, 3, 1, 1)
        self.tab4.layout.addWidget(QLabel("Y:"), 3, 3, 1, 1)
        self.tab4.layout.addWidget(QLabel("Z:"), 4, 3, 1, 1)
        self.tab4.layout.addWidget(self.xOMin, 2, 4, 1, 1)
        self.tab4.layout.addWidget(self.yOMin, 3, 4, 1, 1)
        self.tab4.layout.addWidget(self.zOMin, 4, 4, 1, 1)
        self.tab4.layout.addWidget(self.xOMax, 2, 5, 1, 1)
        self.tab4.layout.addWidget(self.yOMax, 3, 5, 1, 1)
        self.tab4.layout.addWidget(self.zOMax, 4, 5, 1, 1)

        # Define, style, and organize additional interactive widgets.
        self.SSL = QPushButton("Set Soft Limits")
        self.SESL = QPushButton("Set Extreme Soft Limits")
        self.SSL.setStyleSheet("background-color: lightgrey")
        self.SESL.setStyleSheet("background-color: lightgrey")
        self.tab4.layout.addWidget(self.SSL, 5, 0, 1, 3)
        self.tab4.layout.addWidget(self.SESL, 5, 4, 1, 3)

        # Set tab layout.
        self.tab4.setLayout(self.tab4.layout)

        # ---------------------------------------------------------------------
        #   Tab 5
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab5.layout = QGridLayout()

        # Define interactive sample widgets.
        self.xSZero = QPushButton("ZERO")
        self.ySZero = QPushButton("ZERO")
        self.zSZero = QPushButton("ZERO")
        self.xSB = QLineEdit(str(XS_BACKLASH))
        self.ySB = QLineEdit(str(YS_BACKLASH))
        self.zSB = QLineEdit(str(ZS_BACKLASH))

        # Style interactive sample widgets.
        self.xSZero.setStyleSheet("background-color: lightgrey")
        self.ySZero.setStyleSheet("background-color: lightgrey")
        self.zSZero.setStyleSheet("background-color: lightgrey")

        # Organize sample widgets in the tab layout.
        self.tab5.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 3)
        self.tab5.layout.addWidget(QLabel("<i>Backlash</i>"), 1, 2, 1, 1)
        self.tab5.layout.addWidget(QLabel("X:"), 2, 0, 1, 1)
        self.tab5.layout.addWidget(QLabel("Y:"), 3, 0, 1, 1)
        self.tab5.layout.addWidget(QLabel("Z:"), 4, 0, 1, 1)
        self.tab5.layout.addWidget(self.xSZero, 2, 1, 1, 1)
        self.tab5.layout.addWidget(self.ySZero, 3, 1, 1, 1)
        self.tab5.layout.addWidget(self.zSZero, 4, 1, 1, 1)
        self.tab5.layout.addWidget(self.xSB, 2, 2, 1, 1)
        self.tab5.layout.addWidget(self.ySB, 3, 2, 1, 1)
        self.tab5.layout.addWidget(self.zSB, 4, 2, 1, 1)

        # Define interactive objective widgets.
        self.xOZero = QPushButton("ZERO")
        self.yOZero = QPushButton("ZERO")
        self.zOZero = QPushButton("ZERO")
        self.xOB = QLineEdit(str(XO_BACKLASH))
        self.yOB = QLineEdit(str(YO_BACKLASH))
        self.zOB = QLineEdit(str(ZO_BACKLASH))

        # Style interactive objective widgets.
        self.xOZero.setStyleSheet("background-color: lightgrey")
        self.yOZero.setStyleSheet("background-color: lightgrey")
        self.zOZero.setStyleSheet("background-color: lightgrey")

        # Organize objective widgets in the tab layout.
        self.tab5.layout.addWidget(QLabel("<b>Objective</b>"), 0, 3, 1, 3)
        self.tab5.layout.addWidget(QLabel("<i>Backlash</i>"), 1, 5, 1, 1)
        self.tab5.layout.addWidget(QLabel("X:"), 2, 3, 1, 1)
        self.tab5.layout.addWidget(QLabel("Y:"), 3, 3, 1, 1)
        self.tab5.layout.addWidget(QLabel("Z:"), 4, 3, 1, 1)
        self.tab5.layout.addWidget(self.xOZero, 2, 4, 1, 1)
        self.tab5.layout.addWidget(self.yOZero, 3, 4, 1, 1)
        self.tab5.layout.addWidget(self.zOZero, 4, 4, 1, 1)
        self.tab5.layout.addWidget(self.xOB, 2, 5, 1, 1)
        self.tab5.layout.addWidget(self.yOB, 3, 5, 1, 1)
        self.tab5.layout.addWidget(self.zOB, 4, 5, 1, 1)

        # Define, style, and organize additional interactive widgets.
        self.SBL = QPushButton("Update Backlash Values")
        self.SBL.setStyleSheet("background-color: lightgrey")
        self.tab5.layout.addWidget(self.SBL, 5, 0, 1, 6)

        # Set tab layout.
        self.tab5.setLayout(self.tab5.layout)

        # Set window layout.
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
