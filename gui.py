"""Horizontal IR Microscope main GUI file.

Notes
-----
This top level module initiates the GUI for the Far-IR Horizontal Microscope.
"""

"""GUI visual file.

Notes
-----
This module contains the GUI, ImageView, and MyTableWidget classes which
combine to form the GUI visual for the FAR-IR Horizontal Microscope.

Class's
-------
GUI : Object used to create the main GUI interface.
    cameraWindow : Window containing camera feed and interface.
    img : Live feed image.
    updateTime : PyQtGraph ImageItem object.
    fps : Dynamically changing FPS.
    image : Current displayed image.
    WCB : Image capture button.
    SIFN : Saved image file name line edit widget.
    tab : MyTableWidget object.
    xSN : Sample x incremental negative button.
    xSP : Sample x incremental positive button.
    xSStep : Sample x step size line edit.
    xSAbsPos : Sample x absolute position button.
    xSCn : Sample x continuous negative button.
    xSStop : Sample x stop button.
    xSCp : Sample x continuous button.
    xSSn : Sample x soft negative limit label.
    xSSp : Sample x soft positive limit label.
    xSHn : Sample x hard negative limit label.
    xSHp : Sample x hard positive limit label.
    ySN : Sample y incremental negative button.
    ySP : Sample y incremental positive button.
    ySStep : Sample y step size line edit.
    ySAbsPos : Sample y absolute position button.
    ySCn : Sample y continuous negative button.
    ySStop : Sample y stop button.
    ySCp : Sample y continuous button.
    ySSn : Sample y soft negative limit label.
    ySSp : Sample y soft positive limit label.
    ySHn : Sample y hard negative limit label.
    ySHp : Sample y hard positive limit label.
    zSN : Sample z incremental negative button.
    zSP : Sample z incremental positive button.
    zSStep : Sample z step size line edit.
    zSAbsPos : Sample z absolute position button.
    zSCn : Sample z continuous negative button.
    zSStop : Sample z stop button.
    zSCp : Sample z continuous button.
    zSSn : Sample z soft negative limit label.
    zSSp : Sample z soft positive limit label.
    zSHn : Sample z hard negative limit label.
    zSHp : Sample z hard positive limit label.
    xON : Objective x incremental negative button.
    xOP : Objective x incremental positive button.
    xOStep : Objective x step size line edit.
    xOAbsPos : Objective x absolute position button.
    xOCn : Objective x continuous negative button.
    xOStop : Objective x stop button.
    xOCp : Objective x continuous button.
    xOSn : Objective x soft negative limit label.
    xOSp : Objective x soft positive limit label.
    xOHn : Objective x hard negative limit label.
    xOHp : Objective x hard positive limit label.
    yON : Objective y incremental negative button.
    yOP : Objective y incremental positive button.
    yOStep : Objective y step size line edit.
    yOAbsPos : Objective y absolute position button.
    yOCn : Objective y continuous negative button.
    yOStop : Objective y stop button.
    yOCp : Objective y continuous button.
    yOSn : Objective y soft negative limit label.
    yOSp : Objective y soft positive limit label.
    yOHn : Objective y hard negative limit label.
    yOHp : Objective y hard positive limit label.
    zON : Objective z incremental negative button.
    zOP : Objective z incremental positive button.
    zOStep : Objective z step size line edit.
    zOAbsPos : Objective z absolute position button.
    zOCn : Objective z continuous negative button.
    zOStop : Objective z stop button.
    zOCp : Objective z continuous button.
    zOSn : Objective z soft negative limit label.
    zOSp : Objective z soft positive limit label.
    zOHn : Objective z hard negative limit label.
    zOHp : Objective z hard positive limit label.

ImageView: Defines PyQtGraph ImageView object for live feed.

MyTableWidget: Defines the GUI table.
    tabs : QTable Widget.
    tab1 : Tab 1 QWidget.
    tab2 : Tab 2 QWidget.
    tab3 : Tab 3 QWidget.
    tab4 : Tab 4 QWidget.
    tab5 : Tab 5 QWidget.
    xIdleS : Sample x idle label.
    yIdleS : Sample y idle label.
    zIdleS : Sample z idle label.
    xStopS : Sample x stop label.
    yStopS : Sample y stop label.
    zStopS : Sample z stop label.
    xIdleO : Objective x idle label.
    yIdleO : Objective y idle label.
    zIdleO : Objective z idle label.
    xStopO : Objective x stop label.
    yStopO : Objective y stop label.
    zStopO : Objective z stop label.
    RDM1 : Transmission radio button.
    RDM2 : Reflection radio button.
    RDM3 : Visible Image radio button.
    RDM4 : Beamsplitter radio button.
    xSMM : Sample x min and max label.
    ySMM : Sample y min and max label.
    zSMM : Sample z min and max label.
    xOMM : Objective x min and max label.
    yOMM : Objective y min and max label.
    zOMM : Objective z min and max label.
    xSMin : Sample x minimum soft limit line edit.
    xSMax : Sample x maximum soft limit line edit.
    ySMin : Sample y minimum soft limit line edit.
    ySMax : Sample y maximum soft limit line edit.
    zSMin : Sample z minimum soft limit line edit.
    zSMax : Sample z maximum soft limit line edit.
    xOMin : Objective x minimum soft limit line edit.
    xOMax : Objective x maximum soft limit line edit.
    yOMin : Objective y minimum soft limit line edit.
    yOMax : Objective y maximum soft limit line edit.
    zOMin : Objective z minimum soft limit line edit.
    zOMax : Objective z maximum soft limit line edit.
    SSL : Set soft limits button.
    SSL : Set extreme soft limits button.
    xSZero : Sample x zero button.
    ySZero : Sample y zero button.
    zSZero : Sample z zero button.
    xSB : Sample x backlash line edit.
    ySB : Sample y backlash line edit.
    zSB : Sample z backlash line edit.
    xOZero : Objective x zero button.
    yOZero : Objective y zero button.
    zOZero : Objective z zero button.
    xOB : Objective x backlash line edit.
    yOB : Objective y backlash line edit.
    zOB : Objective z backlash line edit.
    SBL : Update backlash values button.
"""


from PyQt5.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QWidget,\
                            QLabel, QPushButton, QLineEdit, QRadioButton,\
                            QTabWidget
from PyQt5.QtGui import QPixmap
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from PyQt5.QtCore import QRectF, QTimer
from typing import Any, Dict
from flir_camera_control import getTestImage
from globals import *


class GUI(QMainWindow):
    """Object used to create the main GUI interface."""

    def __init__(self) -> None:
        """Initialize the GUI."""

        super().__init__()

        self.setWindowTitle("Horizontal Microscope Control")
        self.setFixedWidth(1300)
        self.setFixedHeight(525)

        # Create main display.
        self.layout = QGridLayout()
        self.layout.addWidget(self.getDiagramWindow(), 0, 0, 2, 1)
        self.layout.addWidget(self.getCameraWindow(), 0, 1, 2, 1)
        self.layout.addWidget(self.getTabularWindow(), 0, 2, 2, 1)
        self.layout.addWidget(self.getSampleWindow(), 2, 0, 1, 3)
        self.layout.addWidget(self.getObjectiveWindow(), 3, 0, 1, 3)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

        self.show()

    def getDiagramWindow(self) -> QLabel:
        """
        Generate diagram window.

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
        """
        Generate camera window.

        Parameters
        ----------
        None

        Returns
        -------
        window : QWidget
            Window representing the live feed and interactive widgets.
        """
        def updateData() -> None:
            """
            GUpdate live feed.

            Parameters
            ----------
            None

            Returns
            -------
            None
            """
            self.image = getTestImage()
            height = self.image.shape[0]
            width = self.image.shape[1]

            # Generate cross hairs
            xLine = np.full((3, width, 3), [225, 0, 0])
            self.image[height // 2 - 1 : height // 2 + 2, :] = xLine
            yLine = np.full((height, 3, 3), [225, 0, 0])
            self.image[:, width // 2 - 1 : width // 2 + 2] = yLine

            self.img.setImage(self.image)
            QTimer.singleShot(1, updateData)

            now = ptime.time()
            fps2 = 1.0 / (now - self.updateTime)
            self.updateTime = now
            self.fps = self.fps * 0.9 + fps2 * 0.1
        
        self.cameraWindow = QWidget()
        pg.setConfigOptions(antialias=True)

        win = pg.GraphicsLayoutWidget()
        self.img = pg.ImageItem(border='w')

        view = win.addViewBox()
        view.setAspectLocked(True)
        view.addItem(self.img)
        view.setRange(QRectF(0, 0, 400, 200))

        self.updateTime = ptime.time()
        self.fps = 0

        updateData()

        layout = QGridLayout()

        self.WCB = QPushButton("Image Capture")
        self.SIFN = QLineEdit("File Name")

        self.WCB.setStyleSheet("background-color: lightgrey")

        layout.addWidget(win, 0, 0, 1, 2)
        layout.addWidget(self.WCB, 1, 0, 1, 1)
        layout.addWidget(self.SIFN, 1, 1, 1, 1)

        self.cameraWindow.setLayout(layout)

        return self.cameraWindow

    def getTabularWindow(self) -> QWidget:
        """
        Generates tabular window.

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
        """
        Generate sample window.

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

        layout.addWidget(QLabel("<b>Axis</b>"), 0, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 0, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 0, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 0, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 0, 6, 1, 3)
        layout.addWidget(QLabel("<b>Limits</b>"), 0, 9, 1, 4)

        # ---------------------------------------------------------------------
        #   X Sample Axis
        # ---------------------------------------------------------------------

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

        window.setLayout(layout)
        return window

    def getObjectiveWindow(self) -> QWidget:
        """
        Generate objective window.

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

        layout.addWidget(QLabel("<b>Axis</b>"), 0, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 0, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 0, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 0, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 0, 6, 1, 3)
        layout.addWidget(QLabel("<b>Limits</b>"), 0, 9, 1, 4)

        # ----------------------------------------------------------------------
        #   X Objective Axis
        # ---------------------------------------------------------------------

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

        window.setLayout(layout)
        return window


class ImageView(pg.ImageView):
    """ImageView object"""

    def __init__(self, *args: tuple, **kwargs: Dict[str, any]):
        """Initialize ImageView object"""
        pg.ImageView.__init__(self, *args, **kwargs)


class MyTableWidget(QWidget):
    """
    """

    def __init__(self, parent: Any) -> None:
        """Initialize Class."""

        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()

        self.tabs.resize(3000, 1000)

        self.tabs.addTab(self.tab1, "Status")
        self.tabs.addTab(self.tab2, "Mode")
        self.tabs.addTab(self.tab3, "Specifications")
        self.tabs.addTab(self.tab4, "Limits")
        self.tabs.addTab(self.tab5, "Calibration")

        # ---------------------------------------------------------------------
        #   Tab 1
        # ---------------------------------------------------------------------

        self.tab1.layout = QGridLayout(self)

        # Sample widgets.
        self.xIdleS = QLabel("IDLE")
        self.yIdleS = QLabel("IDLE")
        self.zIdleS = QLabel("IDLE")
        self.xStopS = QLabel("In Motion")
        self.yStopS = QLabel("In Motion")
        self.zStopS = QLabel("In Motion")

        self.xIdleS.setStyleSheet("border: 1px solid black;")
        self.yIdleS.setStyleSheet("border: 1px solid black;")
        self.zIdleS.setStyleSheet("border: 1px solid black;")
        self.xStopS.setStyleSheet("border: 1px solid black;")
        self.yStopS.setStyleSheet("border: 1px solid black;")
        self.zStopS.setStyleSheet("border: 1px solid black;")

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

        # Objective widgets.
        self.xIdleO = QLabel("IDLE")
        self.yIdleO = QLabel("IDLE")
        self.zIdleS = QLabel("IDLE")
        self.xStopO = QLabel("In Motion")
        self.yStopO = QLabel("In Motion")
        self.zStopO = QLabel("In Motion")

        self.xIdleO.setStyleSheet("border: 1px solid black;")
        self.yIdleO.setStyleSheet("border: 1px solid black;")
        self.zIdleS.setStyleSheet("border: 1px solid black;")
        self.xStopO.setStyleSheet("border: 1px solid black;")
        self.yStopO.setStyleSheet("border: 1px solid black;")
        self.zStopO.setStyleSheet("border: 1px solid black;")

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

        self.tab1.setLayout(self.tab1.layout)

        # ---------------------------------------------------------------------
        #   Tab 2
        # ---------------------------------------------------------------------

        self.tab2.layout = QVBoxLayout()

        self.RDM1 = QRadioButton("Transmission")
        self.RDM2 = QRadioButton("Reflection")
        self.RDM3 = QRadioButton("Visible Image")
        self.RDM4 = QRadioButton("Beamsplitter")

        self.tab2.layout.addWidget(self.RDM1)
        self.tab2.layout.addWidget(self.RDM2)
        self.tab2.layout.addWidget(self.RDM3)
        self.tab2.layout.addWidget(self.RDM4)

        self.tab2.setLayout(self.tab2.layout)

        # ---------------------------------------------------------------------
        #   Tab 3
        # ---------------------------------------------------------------------

        self.tab3.layout = QGridLayout()

        # Sample widgets.
        self.xSMM = QLabel(f"{XSMIN_HARD_LIMIT} to {XSMAX_HARD_LIMIT}")
        self.ySMM = QLabel(f"{YSMIN_HARD_LIMIT} to {YSMAX_HARD_LIMIT}")
        self.zSMM = QLabel(f"{ZSMIN_HARD_LIMIT} to {ZSMAX_HARD_LIMIT}")

        self.tab3.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 2)
        self.tab3.layout.addWidget(QLabel("<i>Min to Max</i>"), 1, 1, 1, 1)
        self.tab3.layout.addWidget(QLabel("X:"), 2, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("Y:"), 3, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("Z:"), 4, 0, 1, 1)
        self.tab3.layout.addWidget(self.xSMM, 2, 1, 1, 1)
        self.tab3.layout.addWidget(self.ySMM, 3, 1, 1, 1)
        self.tab3.layout.addWidget(self.zSMM, 4, 1, 1, 1)

        # Objective widgets.
        self.xOMM = QLabel(f"{XOMIN_HARD_LIMIT} to {XOMAX_HARD_LIMIT}")
        self.yOMM = QLabel(f"{YOMIN_HARD_LIMIT} to {YOMAX_HARD_LIMIT}")
        self.zOMM = QLabel(f"{ZOMIN_HARD_LIMIT} to {ZOMAX_HARD_LIMIT}")

        self.tab3.layout.addWidget(QLabel("<b>Objective</b>"), 0, 2, 1, 2)
        self.tab3.layout.addWidget(QLabel("<i>Min to Max</i>"), 1, 3, 1, 1)
        self.tab3.layout.addWidget(QLabel("X:"), 2, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("Y:"), 3, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("Z:"), 4, 2, 1, 1)
        self.tab3.layout.addWidget(self.xOMM, 2, 3, 1, 1)
        self.tab3.layout.addWidget(self.yOMM, 3, 3, 1, 1)
        self.tab3.layout.addWidget(self.zOMM, 4, 3, 1, 1)

        self.tab3.setLayout(self.tab3.layout)

        # ---------------------------------------------------------------------
        #   Tab 4
        # ---------------------------------------------------------------------

        self.tab4.layout = QGridLayout()

        # Sample widgets.
        self.xSMin = QLineEdit("0")
        self.ySMin = QLineEdit("0")
        self.zSMin = QLineEdit("0")
        self.xSMax = QLineEdit("0")
        self.ySMax = QLineEdit("0")
        self.zSMax = QLineEdit("0")

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

        # Objective widgets.
        self.xOMin = QLineEdit("0")
        self.yOMin = QLineEdit("0")
        self.zOMin = QLineEdit("0")
        self.xOMax = QLineEdit("0")
        self.yOMax = QLineEdit("0")
        self.zOMax = QLineEdit("0")

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

        # Additional widgets.
        self.SSL = QPushButton("Set Soft Limits")
        self.SESL = QPushButton("Set Extreme Soft Limits")

        self.SSL.setStyleSheet("background-color: lightgrey")
        self.SESL.setStyleSheet("background-color: lightgrey")

        self.tab4.layout.addWidget(self.SSL, 5, 0, 1, 3)
        self.tab4.layout.addWidget(self.SESL, 5, 4, 1, 3)

        self.tab4.setLayout(self.tab4.layout)

        # ---------------------------------------------------------------------
        #   Tab 5
        # ---------------------------------------------------------------------

        self.tab5.layout = QGridLayout()

        # Sample widgets.
        self.xSZero = QPushButton("ZERO")
        self.ySZero = QPushButton("ZERO")
        self.zSZero = QPushButton("ZERO")
        self.xSB = QLineEdit(str(XS_BACKLASH))
        self.ySB = QLineEdit(str(YS_BACKLASH))
        self.zSB = QLineEdit(str(ZS_BACKLASH))

        self.xSZero.setStyleSheet("background-color: lightgrey")
        self.ySZero.setStyleSheet("background-color: lightgrey")
        self.zSZero.setStyleSheet("background-color: lightgrey")

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

        # Objective widgets.
        self.xOZero = QPushButton("ZERO")
        self.yOZero = QPushButton("ZERO")
        self.zOZero = QPushButton("ZERO")
        self.xOB = QLineEdit(str(XO_BACKLASH))
        self.yOB = QLineEdit(str(YO_BACKLASH))
        self.zOB = QLineEdit(str(ZO_BACKLASH))

        self.xOZero.setStyleSheet("background-color: lightgrey")
        self.yOZero.setStyleSheet("background-color: lightgrey")
        self.zOZero.setStyleSheet("background-color: lightgrey")

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

        # Other widgets.
        self.SBL = QPushButton("Update Backlash Values")
        self.SBL.setStyleSheet("background-color: lightgrey")
        self.tab5.layout.addWidget(self.SBL, 5, 0, 1, 6)

        self.tab5.setLayout(self.tab5.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
