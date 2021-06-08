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
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QRectF, QTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QWidget,\
    QLabel, QPushButton, QLineEdit, QRadioButton,\
    QTabWidget

# Import file dependencies.
from .flir_camera_control import getImage


class GUI(QMainWindow):
    """Main GUI window.

    The GUI class creates the main gui window which allows users to monitor
    and control the main functionality of the microscope.

    Parameters
    ----------
    macros : Dict
        Dictionary of macro variables.

    Attributes
    ----------
    macros : Dict
        Dictionary containing macro variables.
    cameraWindow : QWidget
        QWidget window containing camera feed and interface.
    img : pg.ImageItem
        Live feed image from Blackfly camera.
    image : nd.array
        Current image displayed in an array representation.
    WCB : QPushButton
        Image capture push button.
    tab : MyTableWidget object
        The tabular display located on the main GUI window.
    xSN : QPushButton
        Negative incrment button for the Sample's x dimension.
    xSP : QPushButton
        Positive incrment button for the Sample's x dimension.
    xSStep : QLineEdit
        Step size line edit for the sample's x dimension.
    xSAbsPos : QLineEdit
        Absolute position line edit for the sample's x dimension.
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
    ySAbsPos : QLineEdit
        Absolute position line edit for the sample's y dimension
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
    zSAbsPos : QLineEdit
        Absolute position line edit for the sample's z dimension
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
    xOAbsPos : QLineEdit
        Absolute position line edit for the objective's x dimension
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
    yOAbsPos : QLineEdit
        Absolute position line edit for the objective's y dimension
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
    zOAbsPos : QLineEdit
        Absolute position line edit for the objective's z dimension
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
    _diagram_window()
        Creates the diagram window.
    _camera_window()
        Creates the camera window.
    _tabular_window()
        Creates the table window.
    _sample_window()
        Creates the sample window.
    _objective_window()
        Creates the objective window.
    """

    def __init__(self, macros: Dict) -> None:
        """Initialize the GUI."""

        super().__init__()

        self.macros = macros

        self.setWindowIcon(QIcon('CLS_logo.png'))

        # Define main GUI window.
        self.setWindowTitle("Horizontal Microscope Control")
        self.setFixedWidth(1500)
        self.setFixedHeight(650)

        # Add sub-windows to main window layout.
        self.layout = QGridLayout()
        self.layout.addWidget(self._diagram_window(), 0, 0, 2, 1)
        self.layout.addWidget(self._camera_window(), 0, 1, 2, 1)
        self.layout.addWidget(self._tabular_window(), 0, 2, 2, 1)
        self.layout.addWidget(self._sample_window(), 2, 0, 1, 3)
        self.layout.addWidget(self._objective_window(), 3, 0, 1, 3)

        # Set main window layout.
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

        self.show()

    def _diagram_window(self) -> QLabel:
        """Create diagram window.

        Parameters
        ----------
        None

        Returns
        -------
        QLabel
            Window representing the diagram display.
        """
        window = QLabel()
        window.setPixmap(QPixmap("example_diagram.jpg"))

        return window

    def _camera_window(self) -> QWidget:
        """Create camera window.

        Parameters
        ----------
        None

        Returns
        -------
        QWidget
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
            self.image = np.copy(np.rot90(getImage()))
            height = self.image.shape[0]
            width = self.image.shape[1]

            # Generate cross hairs
            length = int(0.1 * min(height, width))
            xLine = np.full((5, 2 * length, 3), [225, 0, 0])
            yLine = np.full((length * 2, 5, 3), [225, 0, 0])
            self.image[height // 2 - 2:height // 2 + 3,
                       width // 2 - length:width // 2 + length] = xLine
            self.image[height // 2 - length:height // 2 +
                       length:, width // 2 - 2:width // 2 + 3] = yLine

            # Update image.
            self.img.setImage(np.rot90(self.image, 2))
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
        view.setRange(QRectF(300, 0, 700, 1000))

        self.updateTime = ptime.time()
        self.fps = 0

        updateData()

        layout = QGridLayout()

        # Create, modify, and place image capture button and line-edit.
        self.WCB = QPushButton("Image Capture")
        self.WCB.setStyleSheet("background-color: lightgrey")
        layout.addWidget(win, 0, 0, 1, 2)
        layout.addWidget(self.WCB, 1, 0, 1, 2)

        self.cameraWindow.setLayout(layout)

        return self.cameraWindow

    def _tabular_window(self) -> QWidget:
        """Create tabular window.

        Parameters
        ----------
        None

        Returns
        -------
        MyTableWidget(QWidget)
            Object representing the tabular widget.
        """
        self.tab = MyTableWidget(self)
        return self.tab

    def _sample_window(self) -> QWidget:
        """Create sample window.

        Parameters
        ----------
        None

        Returns
        -------
        QWidget
            Window representing the sample interactive widgets.
        """
        window = QWidget()
        layout = QGridLayout()

        sampleLab = QLabel("<b><u>Sample Stage</u></b>")
        sampleLab.setFont(QFont("Times", 9))
        layout.addWidget(sampleLab, 0, 0, 1, 12)

        # Set column labels.
        layout.addWidget(QLabel("<b>Axis</b>"), 1, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 1, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 1, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 1, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 1, 6, 1, 3)
        layout.addWidget(QLabel("<b>Limits</b>"), 1, 9, 1, 4)
        layout.addWidget(QLabel("<b>Current Position</b>"), 1, 13, 1, 1)
        layout.addWidget(QLabel("<b>Motor Status</b>"), 1, 14, 1, 1)

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
        self.xIdleS = QLabel("IDLE")
        self.xStepS = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.xIdleS.setAlignment(Qt.AlignCenter)
        self.xStepS.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.xSN.setStyleSheet("background-color: lightgrey")
        self.xSP.setStyleSheet("background-color: lightgrey")
        self.xSMove.setStyleSheet("background-color: lightgrey")
        self.xSCn.setStyleSheet("background-color: lightgrey")
        self.xSStop.setStyleSheet("background-color: red")
        self.xSCp.setStyleSheet("background-color: lightgrey")
        self.xSSn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xSSp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xSHn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xSHp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xIdleS.setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        layout.addWidget(self.xSN, 2, 1, 1, 1)
        layout.addWidget(self.xSP, 2, 2, 1, 1)
        layout.addWidget(self.xSStep, 2, 3, 1, 1)
        layout.addWidget(self.xSAbsPos, 2, 4, 1, 1)
        layout.addWidget(self.xSMove, 2, 5, 1, 1)
        layout.addWidget(self.xSCn, 2, 6, 1, 1)
        layout.addWidget(self.xSStop, 2, 7, 1, 1)
        layout.addWidget(self.xSCp, 2, 8, 1, 1)
        layout.addWidget(self.xSSn, 2, 9, 1, 1)
        layout.addWidget(self.xSSp, 2, 10, 1, 1)
        layout.addWidget(self.xSHn, 2, 11, 1, 1)
        layout.addWidget(self.xSHp, 2, 12, 1, 1)
        layout.addWidget(self.xStepS, 2, 13, 1, 1)
        layout.addWidget(self.xIdleS, 2, 14, 1, 1)

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
        self.yIdleS = QLabel("IDLE")
        self.yStepS = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.yIdleS.setAlignment(Qt.AlignCenter)
        self.yStepS.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.ySN.setStyleSheet("background-color: lightgrey")
        self.ySP.setStyleSheet("background-color: lightgrey")
        self.ySMove.setStyleSheet("background-color: lightgrey")
        self.ySCn.setStyleSheet("background-color: lightgrey")
        self.ySStop.setStyleSheet("background-color: red")
        self.ySCp.setStyleSheet("background-color: lightgrey")
        self.ySSn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.ySSp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.ySHn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.ySHp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.yIdleS.setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Vertical:"), 3, 0, 1, 1)
        layout.addWidget(self.ySN, 3, 1, 1, 1)
        layout.addWidget(self.ySP, 3, 2, 1, 1)
        layout.addWidget(self.ySStep, 3, 3, 1, 1)
        layout.addWidget(self.ySAbsPos, 3, 4, 1, 1)
        layout.addWidget(self.ySMove, 3, 5, 1, 1)
        layout.addWidget(self.ySCn, 3, 6, 1, 1)
        layout.addWidget(self.ySStop, 3, 7, 1, 1)
        layout.addWidget(self.ySCp, 3, 8, 1, 1)
        layout.addWidget(self.ySSn, 3, 9, 1, 1)
        layout.addWidget(self.ySSp, 3, 10, 1, 1)
        layout.addWidget(self.ySHn, 3, 11, 1, 1)
        layout.addWidget(self.ySHp, 3, 12, 1, 1)
        layout.addWidget(self.yStepS, 3, 13, 1, 1)
        layout.addWidget(self.yIdleS, 3, 14, 1, 1)

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
        self.zIdleS = QLabel("IDLE")
        self.zStepS = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.zIdleS.setAlignment(Qt.AlignCenter)
        self.zStepS.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.zSN.setStyleSheet("background-color: lightgrey")
        self.zSP.setStyleSheet("background-color: lightgrey")
        self.zSMove.setStyleSheet("background-color: lightgrey")
        self.zSCn.setStyleSheet("background-color: lightgrey")
        self.zSStop.setStyleSheet("background-color: red")
        self.zSCp.setStyleSheet("background-color: lightgrey")
        self.zSSn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zSSp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zSHn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zSHp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zIdleS.setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Focus:"), 4, 0, 1, 1)
        layout.addWidget(self.zSN, 4, 1, 1, 1)
        layout.addWidget(self.zSP, 4, 2, 1, 1)
        layout.addWidget(self.zSStep, 4, 3, 1, 1)
        layout.addWidget(self.zSAbsPos, 4, 4, 1, 1)
        layout.addWidget(self.zSMove, 4, 5, 1, 1)
        layout.addWidget(self.zSCn, 4, 6, 1, 1)
        layout.addWidget(self.zSStop, 4, 7, 1, 1)
        layout.addWidget(self.zSCp, 4, 8, 1, 1)
        layout.addWidget(self.zSSn, 4, 9, 1, 1)
        layout.addWidget(self.zSSp, 4, 10, 1, 1)
        layout.addWidget(self.zSHn, 4, 11, 1, 1)
        layout.addWidget(self.zSHp, 4, 12, 1, 1)
        layout.addWidget(self.zStepS, 4, 13, 1, 1)
        layout.addWidget(self.zIdleS, 4, 14, 1, 1)

        # Set window layout.
        window.setLayout(layout)
        return window

    def _objective_window(self) -> QWidget:
        """Create objective window.

        Parameters
        ----------
        None

        Returns
        -------
        QWidget
            Window representing the objective interactive widgets.
        """
        window = QWidget()
        layout = QGridLayout()

        objectiveLab = QLabel("<b><u>Objective Stage</u></b>")
        objectiveLab.setFont(QFont("Times", 9))
        layout.addWidget(objectiveLab, 0, 0, 1, 13)

        # Set column labels.
        layout.addWidget(QLabel("<b>Axis</b>"), 1, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 1, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 1, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 1, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 1, 6, 1, 3)
        layout.addWidget(QLabel("<b>Limits</b>"), 1, 9, 1, 4)
        layout.addWidget(QLabel("<b>Current Position</b>"), 1, 13, 1, 1)
        layout.addWidget(QLabel("<b>Motor Status</b>"), 1, 14, 1, 1)

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
        self.xIdleO = QLabel("IDLE")
        self.xStepO = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.xIdleO.setAlignment(Qt.AlignCenter)
        self.xStepO.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.xON.setStyleSheet("background-color: lightgrey")
        self.xOP.setStyleSheet("background-color: lightgrey")
        self.xOMove.setStyleSheet("background-color: lightgrey")
        self.xOCn.setStyleSheet("background-color: lightgrey")
        self.xOStop.setStyleSheet("background-color: red")
        self.xOCp.setStyleSheet("background-color: lightgrey")
        self.xOSn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xOSp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xOHn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xOHp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.xIdleO.setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        layout.addWidget(self.xON, 2, 1, 1, 1)
        layout.addWidget(self.xOP, 2, 2, 1, 1)
        layout.addWidget(self.xOStep, 2, 3, 1, 1)
        layout.addWidget(self.xOAbsPos, 2, 4, 1, 1)
        layout.addWidget(self.xOMove, 2, 5, 1, 1)
        layout.addWidget(self.xOCn, 2, 6, 1, 1)
        layout.addWidget(self.xOStop, 2, 7, 1, 1)
        layout.addWidget(self.xOCp, 2, 8, 1, 1)
        layout.addWidget(self.xOSn, 2, 9, 1, 1)
        layout.addWidget(self.xOSp, 2, 10, 1, 1)
        layout.addWidget(self.xOHn, 2, 11, 1, 1)
        layout.addWidget(self.xOHp, 2, 12, 1, 1)
        layout.addWidget(self.xStepO, 2, 13, 1, 1)
        layout.addWidget(self.xIdleO, 2, 14, 1, 1)

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
        self.yIdleO = QLabel("IDLE")
        self.yStepO = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.yIdleO.setAlignment(Qt.AlignCenter)
        self.yStepO.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.yON.setStyleSheet("background-color: lightgrey")
        self.yOP.setStyleSheet("background-color: lightgrey")
        self.yOMove.setStyleSheet("background-color: lightgrey")
        self.yOCn.setStyleSheet("background-color: lightgrey")
        self.yOStop.setStyleSheet("background-color: red")
        self.yOCp.setStyleSheet("background-color: lightgrey")
        self.yOSn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.yOSp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.yOHn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.yOHp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.yIdleO.setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Vertical:"), 3, 0, 1, 1)
        layout.addWidget(self.yON, 3, 1, 1, 1)
        layout.addWidget(self.yOP, 3, 2, 1, 1)
        layout.addWidget(self.yOStep, 3, 3, 1, 1)
        layout.addWidget(self.yOAbsPos, 3, 4, 1, 1)
        layout.addWidget(self.yOMove, 3, 5, 1, 1)
        layout.addWidget(self.yOCn, 3, 6, 1, 1)
        layout.addWidget(self.yOStop, 3, 7, 1, 1)
        layout.addWidget(self.yOCp, 3, 8, 1, 1)
        layout.addWidget(self.yOSn, 3, 9, 1, 1)
        layout.addWidget(self.yOSp, 3, 10, 1, 1)
        layout.addWidget(self.yOHn, 3, 11, 1, 1)
        layout.addWidget(self.yOHp, 3, 12, 1, 1)
        layout.addWidget(self.yStepO, 3, 13, 1, 1)
        layout.addWidget(self.yIdleO, 3, 14, 1, 1)

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
        self.zIdleO = QLabel("IDLE")
        self.zStepO = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.zIdleO.setAlignment(Qt.AlignCenter)
        self.zStepO.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.zON.setStyleSheet("background-color: lightgrey")
        self.zOP.setStyleSheet("background-color: lightgrey")
        self.zOMove.setStyleSheet("background-color: lightgrey")
        self.zOCn.setStyleSheet("background-color: lightgrey")
        self.zOStop.setStyleSheet("background-color: red")
        self.zOCp.setStyleSheet("background-color: lightgrey")
        self.zOSn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zOSp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zOHn.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zOHp.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        self.zIdleO.setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Organize widgets on layout.
        layout.addWidget(QLabel("Focus:"), 4, 0, 1, 1)
        layout.addWidget(self.zON, 4, 1, 1, 1)
        layout.addWidget(self.zOP, 4, 2, 1, 1)
        layout.addWidget(self.zOStep, 4, 3, 1, 1)
        layout.addWidget(self.zOAbsPos, 4, 4, 1, 1)
        layout.addWidget(self.zOMove, 4, 5, 1, 1)
        layout.addWidget(self.zOCn, 4, 6, 1, 1)
        layout.addWidget(self.zOStop, 4, 7, 1, 1)
        layout.addWidget(self.zOCp, 4, 8, 1, 1)
        layout.addWidget(self.zOSn, 4, 9, 1, 1)
        layout.addWidget(self.zOSp, 4, 10, 1, 1)
        layout.addWidget(self.zOHn, 4, 11, 1, 1)
        layout.addWidget(self.zOHp, 4, 12, 1, 1)
        layout.addWidget(self.zStepO, 4, 13, 1, 1)
        layout.addWidget(self.zIdleO, 4, 14, 1, 1)

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
        Hard Limits tab of the table window.
    tab4 : QWidget
        Soft Limits tab of the table window.
    tab5 : QWidget
        Calibration tab of the table window.
    xIdleS : QLabel
        Idle label for the sample's x dimension.
    yIdleS : QLabel
        Idle label for the sample's y dimension.
    zIdleS : QLabel
        Idle label for the sample's z dimension.
    xStepS : QLabel
        STEPS label for the sample's x dimension.
    yStepS : QLabel
        STEPS label for the sample's y dimension.
    zStepS : QLabel
        STEPS label for the sample's z dimension.
    xIdleO : QLabel
        Idle label for the objective's x dimension.
    yIdleO : QLabel
        Idle label for the objective's y dimension.
    zIdleO : QLabel
        Idle label for the objective's z dimension.
    xStepO : QLabel
        STEPS label for the objective's x dimension.
    yStepO : QLabel
        STEPS label for the objective's y dimension.
    zStepO : QLabel
        STEPS label for the objective's z dimension.
    RDM1 : QRadioButton
        Transmission mode radio button.
    RDM2 : QRadioButton
        Reflection mode radio button.
    RDM3 : QRadioButton
        Visible Image mode radio button.
    RDM4 : QRadioButton
        Beamsplitter mode radio button.
    TMTM : QLineEdit
        Transmission mode position line edit.
    TMRM : QLineEdit
        Reflection mode position line edit.
    TMVM : QLineEdit
        Visual image mode position line edit.
    TMBM : QLineEdit
        Beamsplitter mode position line edit.
    TMTMbutton : QPushButton
        Transmission "Set Position" button.
    TMRMbutton : QPushButton
        Reflection "Set Position" button.
    TMVMbutton : QPushButton
        Visual image "Set Position" button.
    TMBMbutton : QPushButton
        Beamsplitter "Set Position" button.
    enableDisable : QPushButton
        Enable or Disable the THORLABS/mode motor.
    home : QPushButton
        Home THORLABS/mode motor.
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
    SMSL : QPushButton
        Set minimal soft limits button.
    SESL : QPushButton
        Set maximal soft limits button.
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
    valueType : QPushButton
        Toggles between actual and relative values.
    globals : QPushButton
        Display the programs global variables.

    Methods
    -------
    None
    """

    def __init__(self, parent: Any) -> None:
        """Initialize Class."""

        self.parent = parent

        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Define tab windows.
        self.tabs = QTabWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        self.tabs.resize(3000, 1000)

        # Add tabs to window layout.
        self.tabs.addTab(self.tab2, "Mode")
        self.tabs.addTab(self.tab3, "Hard Limits")
        self.tabs.addTab(self.tab4, "Soft Limits")
        self.tabs.addTab(self.tab5, "Calibration")


        # ---------------------------------------------------------------------
        #   Tab 2
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab2.layout = QGridLayout()

        self.tab2.layout.addWidget(QLabel("<b>Mode Selection</b>"), 0, 0, 1, 4)

        # Define mode select buttons.
        self.RDM1 = QRadioButton("Transmission")
        self.RDM2 = QRadioButton("Reflection")
        self.RDM3 = QRadioButton("Visible Image")
        self.RDM4 = QRadioButton("Beamsplitter")

        # Organize widgets on tab layout.
        self.tab2.layout.addWidget(self.RDM1, 1, 0, 1, 1)
        self.tab2.layout.addWidget(self.RDM2, 2, 0, 1, 1)
        self.tab2.layout.addWidget(self.RDM3, 3, 0, 1, 1)
        self.tab2.layout.addWidget(self.RDM4, 4, 0, 1, 1)

        # Set position customization widgets
        self.TMTM = QLineEdit(str(float(self.parent.macros["TRANSMISSION_POSITION"])))
        self.TMRM = QLineEdit(str(float(self.parent.macros["REFLECTION_POSITION"])))
        self.TMVM = QLineEdit(str(float(self.parent.macros["VISIBLE_IMAGE_POSITION"])))
        self.TMBM = QLineEdit(str(float(self.parent.macros["BEAMSPLITTER_POSITION"])))

        self.tab2.layout.addWidget(self.TMTM, 1, 1, 1, 1)
        self.tab2.layout.addWidget(self.TMRM, 2, 1, 1, 1)
        self.tab2.layout.addWidget(self.TMVM, 3, 1, 1, 1)
        self.tab2.layout.addWidget(self.TMBM, 4, 1, 1, 1)

        self.TMTMbutton = QPushButton("Set Position")
        self.TMRMbutton = QPushButton("Set Position")
        self.TMVMbutton = QPushButton("Set Position")
        self.TMBMbutton = QPushButton("Set Position")

        self.tab2.layout.addWidget(self.TMTMbutton, 1, 2, 1, 1)
        self.tab2.layout.addWidget(self.TMRMbutton, 2, 2, 1, 1)
        self.tab2.layout.addWidget(self.TMVMbutton, 3, 2, 1, 1)
        self.tab2.layout.addWidget(self.TMBMbutton, 4, 2, 1, 1)

        self.tab2.layout.addWidget(QLabel("<b>Motor Control</b>"), 5, 0, 1, 4)

        # THORLABS/mode motor controls.
        self.enableDisable = QPushButton("Enable")
        self.home = QPushButton("Home Motor")
        self.tab2.layout.addWidget(self.enableDisable, 6, 0, 1, 1)
        self.tab2.layout.addWidget(self.home, 6, 1, 1, 2)

        # Check mode when in homed position.
        self.RDM3.setChecked(True)

        # Set tab layout.
        self.tab2.setLayout(self.tab2.layout)

        # ---------------------------------------------------------------------
        #   Tab 3
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab3.layout = QGridLayout()

        # Define interactive sample widgets.
        xHardMin = self.parent.macros["XSMIN_HARD_LIMIT"]
        xHardMax = self.parent.macros["XSMAX_HARD_LIMIT"]
        yHardMin = self.parent.macros["YSMIN_HARD_LIMIT"]
        yHardMax = self.parent.macros["YSMAX_HARD_LIMIT"]
        zHardMin = self.parent.macros["ZSMIN_HARD_LIMIT"]
        zHardMax = self.parent.macros["ZSMAX_HARD_LIMIT"]
        self.xSMM = QLabel(f"{xHardMin} to {xHardMax}")
        self.ySMM = QLabel(f"{yHardMin} to {yHardMax}")
        self.zSMM = QLabel(f"{zHardMin} to {zHardMax}")

        # Organize sample widgets in the tab layout.
        self.tab3.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 2)
        self.tab3.layout.addWidget(QLabel("<i>Min to Max</i>"), 1, 1, 1, 1)
        self.tab3.layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("Vertical:"), 3, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("Focus:"), 4, 0, 1, 1)
        self.tab3.layout.addWidget(self.xSMM, 2, 1, 1, 1)
        self.tab3.layout.addWidget(self.ySMM, 3, 1, 1, 1)
        self.tab3.layout.addWidget(self.zSMM, 4, 1, 1, 1)

        # Define interactive objective widgets.
        xHardMin = self.parent.macros["XOMIN_HARD_LIMIT"]
        xHardMax = self.parent.macros["XOMAX_HARD_LIMIT"]
        yHardMin = self.parent.macros["YOMIN_HARD_LIMIT"]
        yHardMax = self.parent.macros["YOMAX_HARD_LIMIT"]
        zHardMin = self.parent.macros["ZOMIN_HARD_LIMIT"]
        zHardMax = self.parent.macros["ZOMAX_HARD_LIMIT"]
        self.xOMM = QLabel(f"{xHardMin} to {xHardMax}")
        self.yOMM = QLabel(f"{yHardMin} to {yHardMax}")
        self.zOMM = QLabel(f"{zHardMin} to {zHardMax}")

        # Organize objective widgets in the tab layout.
        self.tab3.layout.addWidget(QLabel("<b>Objective</b>"), 0, 2, 1, 2)
        self.tab3.layout.addWidget(QLabel("<i>Min to Max</i>"), 1, 3, 1, 1)
        self.tab3.layout.addWidget(QLabel("Horizontal:"), 2, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("Vertical:"), 3, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("Focus:"), 4, 2, 1, 1)
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
        self.xSMin = QLineEdit(
            str(float(self.parent.macros["XSMIN_SOFT_LIMIT"])))
        self.ySMin = QLineEdit(
            str(float(self.parent.macros["YSMIN_SOFT_LIMIT"])))
        self.zSMin = QLineEdit(
            str(float(self.parent.macros["ZSMIN_SOFT_LIMIT"])))
        self.xSMax = QLineEdit(
            str(float(self.parent.macros["XSMAX_SOFT_LIMIT"])))
        self.ySMax = QLineEdit(
            str(float(self.parent.macros["YSMAX_SOFT_LIMIT"])))
        self.zSMax = QLineEdit(
            str(float(self.parent.macros["ZSMAX_SOFT_LIMIT"])))

        # Organize sample widgets in the tab layout.
        self.tab4.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 3)
        self.tab4.layout.addWidget(QLabel("<i>Min</i>"), 1, 1, 1, 1)
        self.tab4.layout.addWidget(QLabel("<i>Max</i>"), 1, 2, 1, 1)
        self.tab4.layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        self.tab4.layout.addWidget(QLabel("Vertical:"), 3, 0, 1, 1)
        self.tab4.layout.addWidget(QLabel("Focus:"), 4, 0, 1, 1)
        self.tab4.layout.addWidget(self.xSMin, 2, 1, 1, 1)
        self.tab4.layout.addWidget(self.ySMin, 3, 1, 1, 1)
        self.tab4.layout.addWidget(self.zSMin, 4, 1, 1, 1)
        self.tab4.layout.addWidget(self.xSMax, 2, 2, 1, 1)
        self.tab4.layout.addWidget(self.ySMax, 3, 2, 1, 1)
        self.tab4.layout.addWidget(self.zSMax, 4, 2, 1, 1)

        # Define interactive objective widgets.
        self.xOMin = QLineEdit(
            str(float(self.parent.macros["XOMIN_SOFT_LIMIT"])))
        self.yOMin = QLineEdit(
            str(float(self.parent.macros["YOMIN_SOFT_LIMIT"])))
        self.zOMin = QLineEdit(
            str(float(self.parent.macros["ZOMIN_SOFT_LIMIT"])))
        self.xOMax = QLineEdit(
            str(float(self.parent.macros["XOMAX_SOFT_LIMIT"])))
        self.yOMax = QLineEdit(
            str(float(self.parent.macros["YOMAX_SOFT_LIMIT"])))
        self.zOMax = QLineEdit(
            str(float(self.parent.macros["ZOMAX_SOFT_LIMIT"])))

        # Organize objective widgets in the tab layout.
        self.tab4.layout.addWidget(QLabel("<b>Objective</b>"), 0, 3, 1, 3)
        self.tab4.layout.addWidget(QLabel("<i>Min</i>"), 1, 4, 1, 1)
        self.tab4.layout.addWidget(QLabel("<i>Max</i>"), 1, 5, 1, 1)
        self.tab4.layout.addWidget(QLabel("Horizontal:"), 2, 3, 1, 1)
        self.tab4.layout.addWidget(QLabel("Vertical:"), 3, 3, 1, 1)
        self.tab4.layout.addWidget(QLabel("Focus:"), 4, 3, 1, 1)
        self.tab4.layout.addWidget(self.xOMin, 2, 4, 1, 1)
        self.tab4.layout.addWidget(self.yOMin, 3, 4, 1, 1)
        self.tab4.layout.addWidget(self.zOMin, 4, 4, 1, 1)
        self.tab4.layout.addWidget(self.xOMax, 2, 5, 1, 1)
        self.tab4.layout.addWidget(self.yOMax, 3, 5, 1, 1)
        self.tab4.layout.addWidget(self.zOMax, 4, 5, 1, 1)

        # Define, style, and organize additional interactive widgets.
        self.SSL = QPushButton("Set Soft Limits")
        self.SMSL = QPushButton("Set Minimal Soft Limits")
        self.SESL = QPushButton("Set Maximal Soft Limits")
        self.SSL.setStyleSheet("background-color: lightgrey")
        self.SMSL.setStyleSheet("background-color: lightgrey")
        self.SESL.setStyleSheet("background-color: lightgrey")
        self.tab4.layout.addWidget(self.SSL, 5, 0, 1, 6)
        self.tab4.layout.addWidget(self.SMSL, 6, 0, 1, 3)
        self.tab4.layout.addWidget(self.SESL, 6, 3, 1, 3)

        # Add information labels.
        softLimLabel = QLabel("<i>The motors will move 'backlash' steps past the low limit before moving back to the lower limit.</i>")
        softLimLabel.setWordWrap(True)
        self.tab4.layout.addWidget(softLimLabel, 7, 0, 1, 6)

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
        xB = self.parent.macros["XS_BACKLASH"]
        yB = self.parent.macros["YS_BACKLASH"]
        zB = self.parent.macros["ZS_BACKLASH"]
        self.xSB = QLineEdit(str(xB))
        self.ySB = QLineEdit(str(yB))
        self.zSB = QLineEdit(str(zB))

        # Style interactive sample widgets.
        self.xSZero.setStyleSheet("background-color: lightgrey")
        self.ySZero.setStyleSheet("background-color: lightgrey")
        self.zSZero.setStyleSheet("background-color: lightgrey")

        # Organize sample widgets in the tab layout.
        self.tab5.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 3)
        self.tab5.layout.addWidget(QLabel("<i>Backlash</i>"), 1, 2, 1, 1)
        self.tab5.layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        self.tab5.layout.addWidget(QLabel("Vertical:"), 3, 0, 1, 1)
        self.tab5.layout.addWidget(QLabel("Focus:"), 4, 0, 1, 1)
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
        xB = self.parent.macros["XO_BACKLASH"]
        yB = self.parent.macros["YO_BACKLASH"]
        zB = self.parent.macros["ZO_BACKLASH"]
        self.xOB = QLineEdit(str(xB))
        self.yOB = QLineEdit(str(yB))
        self.zOB = QLineEdit(str(zB))

        # Style interactive objective widgets.
        self.xOZero.setStyleSheet("background-color: lightgrey")
        self.yOZero.setStyleSheet("background-color: lightgrey")
        self.zOZero.setStyleSheet("background-color: lightgrey")

        # Organize objective widgets in the tab layout.
        self.tab5.layout.addWidget(QLabel("<b>Objective</b>"), 0, 3, 1, 3)
        self.tab5.layout.addWidget(QLabel("<i>Backlash</i>"), 1, 5, 1, 1)
        self.tab5.layout.addWidget(QLabel("Horizontal:"), 2, 3, 1, 1)
        self.tab5.layout.addWidget(QLabel("Vertical:"), 3, 3, 1, 1)
        self.tab5.layout.addWidget(QLabel("Focus:"), 4, 3, 1, 1)
        self.tab5.layout.addWidget(self.xOZero, 2, 4, 1, 1)
        self.tab5.layout.addWidget(self.yOZero, 3, 4, 1, 1)
        self.tab5.layout.addWidget(self.zOZero, 4, 4, 1, 1)
        self.tab5.layout.addWidget(self.xOB, 2, 5, 1, 1)
        self.tab5.layout.addWidget(self.yOB, 3, 5, 1, 1)
        self.tab5.layout.addWidget(self.zOB, 4, 5, 1, 1)

        # Define, style, and organize additional interactive widgets.
        self.SBL = QPushButton("Update Backlash Values")
        self.SBL.setStyleSheet("background-color: lightgrey")
        self.tab5.layout.addWidget(self.SBL, 5, 0, 1, 3)

        # Add information labels.
        backlashLabel = QLabel(
            "<i>Backlash is applied when moving negitively. The motor will move 'backlash' steps past the target position before returning to the target position</i>")
        zeroLabel = QLabel("<i>Cannot zero when displaying actual values.</i>")
        backlashLabel.setWordWrap(True)
        zeroLabel.setWordWrap(True)
        self.tab5.layout.addWidget(backlashLabel, 6, 0, 1, 6)
        self.tab5.layout.addWidget(zeroLabel, 7, 0, 1, 4)

        self.valueType = QPushButton("Display Actual Values")
        self.valueType.setCheckable(True)
        self.valueType.setStyleSheet("background-color: lightgrey")
        self.tab5.layout.addWidget(self.valueType, 5, 3, 1, 3)

        self.globals = QPushButton("GLOBALS")
        self.globals.setStyleSheet("background-color: lightgrey")
        self.tab5.layout.addWidget(self.globals, 7, 5, 1, 1)

        # Set tab layout.
        self.tab5.setLayout(self.tab5.layout)

        # Set window layout.
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
