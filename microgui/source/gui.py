"""Main GUI display.

This module contains the `GUI` and `MyTableWidget` class' responsible for
creating the main user interface with the FAR-IR Horizontal Microscope.
"""


from flir_camera_control import get_image
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QRectF, QTimer, Qt
from PyQt5.QtWidgets import (
    QButtonGroup, QComboBox, QDockWidget, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QScrollBar, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget, QFileDialog
)
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime


class GUI(QMainWindow):
    """Main GUI window.

    The `GUI` class creates the main gui window which allows users to monitor
    and control the main functionality of the microscope.

    Parameters
    ----------
    data : dict
        Dictionary of raw configuration variable data.
    macros : dict
        Dictionary of macro variables (planar version of the `data` attribute).
    savedPos : dict
        Dictionary of saved positions.

    Attributes
    ----------
    data : dict
        Dictionary containing initialization data.
    macros : dict
        Dictionary containing macro variables.
    tab : MyTableWidget object
        The tabular display located on the main GUI window.
    xSN, ySN, zSN : QPushButton
        Negative incrment button for the sample's x, y, and z dimensions.
    xSP, ySP, zSP : QPushButton
        Positive incrment button for the sample's x, y, and z dimensions.
    xSStep, ySStep, zSStep : QLineEdit
        Step size line edit for the sample's x, y, and z dimensions.
    xSAbsPos, ySAbsPos, zSAbsPos : QLineEdit
        Absolute position line edit for the sample's x, y, and z dimensions.
    xSMove, ySMove, zSMove : QPushButton
        Move to absolute position button for the sample's x, y, and z
        dimensions.
    xSCn, ySCn, zSCn : QPushButton
        Continuous negative motion buttonfor the sample's x, y, and z
        dimensions.
    xSStop, ySStop, zSStop : QPushButton
        Stop continuous motion button for the sample's x, y, and z dimensions.
    xSCp, ySCp, zSCp : QPushButton
        Continuous positive motion buttonfor the sample's x, y, and z
        dimensions.
    xSSn, ySSn, zSSn : QLineEdit
        Negative soft limit label for the sample's x, y, and z dimensions.
    xSSp, ySSp, zSSp : QLineEdit
        Positive soft limit label for the sample's x, y, and z dimensions.
    xSHn, ySHn, zSHn : QLineEdit
        Negative hard limit label for the sample's x, y, and z dimensions.
    xSHn, ySHn, zSHn : QLineEdit
        Positive hard limit label for the sample's x, y, and z dimensions.
    xStepS, yStepS, zStepS : QLabel
        STEPS label for the sample's x, y, and z dimensions.
    xIdleS, yIdleS, zIdleS : QLabel
        Motor status label for the sample's x, y, and z dimensions.
    xON, yON, zON : QPushButton
        Negative incrment button for the objective's x, y, and z dimensions.
    xOP, yOP, zOP : QPushButton
        Positive incrment button for the objective's x, y, and z dimensions.
    xOStep, yOStep, zOStep : QLineEdit
        Step size line edit for the objective's x, y, and z dimensions.
    xOAbsPos, yOAbsPos, zOAbsPos : QLineEdit
        Absolute position line edit for the objective's x, y, and z dimensions.
    xOMove, yOMove, zOMove : QPushButton
        Move to absolute position button for the objective's x, y, and z
        dimensions.
    xOCn, yOCn, zOCn : QPushButton
        Continuous negative motion buttonfor the objective's x, y, and z
        dimensions.
    xOStop, yOStop, zOStop : QPushButton
        Stop continuous motion button for the objective's x, y, and z
        dimensions.
    xOCp, yOCp, zOCp : QPushButton
        Continuous positive motion buttonfor the objective's x, y, and z
        dimensions.
    xOSn, yOSn, zOSn : QLineEdit
        Negative soft limit label for the objective's x, y, and z dimensions.
    xOSp, yOSp, zOSp : QLineEdit
        Positive soft limit label for the objective's x, y, and z dimensions.
    xOHn, yOHn, zOHn : QLineEdit
        Negative hard limit label for the objective's x, y, and z dimensions.
    xOHn, yOHn, zOHn : QLineEdit
        Positive hard limit label for the objective's x, y, and z dimensions.
    xStepO, yStepO, zStepO : QLabel
        STEPS label for the objective's x, y, and z dimensions.
    xIdleO, yIdleO, zIdleO : QLabel
        Motor status label for the objective's x, y, and z dimensions.
    textWindow : QTextBrowser
        Text browser to display Terminal output.
    savePos : QPushButton
        Save current position push button.
    loadPos : QPushButton
        Load selected position push button.
    deletePos : QPushButton
        Delete selected position push button.
    clearPos : QPushButton
        Clear all saved positions push button.
    posSelect : QComboBox
        Combo box to select a saved position.
    posLabel : QLineEdit
        Text box to insert the label for a position to save.
    loadConfig : QPushButton
        Load a new configuration button.
    saveConfig : QPushButton
        Save current configuration button.
    positionUnits : QPushButton
        Control to shange the current position between steps and microns.

    Methods
    -------
    diagram_window()
        Return the diagram window.
    tabular_window()
        Return the table window.
    sample_window()
        Return the sample window.
    objective_window()
        Return the objective window.
    base_window()
        Return the base window.
    """

    def __init__(self, data: dict, macros: dict, savedPos: dict) -> None:
        """Initialize the GUI.
        
        Notes
        -----
        This method initializes the user interface by instantiating important
        attributes, configuring the main window, and calling helper functions
        to create individual windows.
        """

        super().__init__()

        self.data = data
        self.macros = macros
        self.savedPos = savedPos

        # Set MicroGUI logo.
        self.setWindowIcon(QIcon("figures/MicroGUI_logo.png"))

        # Define main GUI window.
        self.setWindowTitle("Horizontal Microscope Control")
        self.setFixedWidth(1500)
        self.setFixedHeight(750)

        # Add sub-windows to main window layout.
        self.layout = QGridLayout()
        self.layout.addWidget(self.diagram_window(), 0, 0, 2, 5)
        self.layout.addWidget(CameraWindow(), 0, 5, 2, 5)
        self.layout.addWidget(self.tabular_window(), 0, 10, 2, 5)
        self.layout.addWidget(self.sample_window(), 2, 0, 1, 15)
        self.layout.addWidget(self.objective_window(), 3, 0, 1, 15)
        self.layout.addWidget(self.base_window(), 4, 0, 3, 15)

        # Set main window layout.
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

        self.show()

    def diagram_window(self) -> QLabel:
        """Return the diagram window.

        This method returns a label with the diagram display to allow users to
        understand motor motion and button correspondance.

        Returns
        -------
        QLabel
            Window representing the diagram display.
        """

        window = QLabel()
        image = QPixmap("figures/diagram.jpg")
        image = image.scaled(350, 350, Qt.KeepAspectRatio)
        window.setPixmap(QPixmap(image))

        return window

    def tabular_window(self) -> QWidget:
        """Return the table window.

        This method returns the tab window for the gui configuration controls.

        Returns
        -------
        MyTableWidget(QWidget)
            Object representing the tabular widget.
        """

        self.tab = MyTableWidget(self)
        return self.tab

    def sample_window(self) -> QWidget:
        """Return the sample window.

        This method returns the controls and motor status indicators for the
        sample stage.

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

        # Define widget style sheets.
        button_style_grey = "background-color: lightgrey"
        button_style_red = "background-color: red"
        label_style_grey = "background-color: lightgrey; border: 1px solid black;"

        # Set column labels.
        layout.addWidget(QLabel("<b>Axis</b>"), 1, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 1, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 1, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 1, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 1, 6, 1, 3)
        layout.addWidget(QLabel("<b>Soft Limits</b>"), 1, 9, 1, 2)
        layout.addWidget(QLabel("<b>Hard Limits</b>"), 1, 11, 1, 2)
        layout.addWidget(QLabel("<b>Current Position</b>"), 1, 13, 1, 1)
        layout.addWidget(QLabel("<b>Motor Status</b>"), 1, 14, 1, 1)

        # ---------------------------------------------------------------------
        #   X Sample Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.xSN = QPushButton("In")
        self.xSP = QPushButton("Out")
        self.xSStep = QLineEdit("0")
        self.xSAbsPos = QLineEdit("0")
        self.xSMove = QPushButton("MOVE")
        self.xSCn = QPushButton("In")
        self.xSStop = QPushButton("STOP")
        self.xSCp = QPushButton("Out")
        self.xSSn = QLabel("In")
        self.xSSp = QLabel("Out")
        self.xSHn = QLabel("In")
        self.xSHp = QLabel("Out")
        self.xIdleS = QLabel("IDLE")
        self.xStepS = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.xIdleS.setAlignment(Qt.AlignCenter)
        self.xStepS.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.xSN.setStyleSheet(button_style_grey)
        self.xSP.setStyleSheet(button_style_grey)
        self.xSMove.setStyleSheet(button_style_grey)
        self.xSCn.setStyleSheet(button_style_grey)
        self.xSStop.setStyleSheet(button_style_red)
        self.xSCp.setStyleSheet(button_style_grey)
        self.xSSn.setStyleSheet(label_style_grey)
        self.xSSp.setStyleSheet(label_style_grey)
        self.xSHn.setStyleSheet(label_style_grey)
        self.xSHp.setStyleSheet(label_style_grey)
        self.xIdleS.setStyleSheet(label_style_grey)

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
        self.ySN = QPushButton("Up")
        self.ySP = QPushButton("Down")
        self.ySStep = QLineEdit("0")
        self.ySAbsPos = QLineEdit("0")
        self.ySMove = QPushButton("MOVE")
        self.ySCn = QPushButton("Up")
        self.ySStop = QPushButton("STOP")
        self.ySCp = QPushButton("Down")
        self.ySSn = QLabel("Up")
        self.ySSp = QLabel("Down")
        self.ySHn = QLabel("Up")
        self.ySHp = QLabel("Down")
        self.yIdleS = QLabel("IDLE")
        self.yStepS = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.yIdleS.setAlignment(Qt.AlignCenter)
        self.yStepS.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.ySN.setStyleSheet(button_style_grey)
        self.ySP.setStyleSheet(button_style_grey)
        self.ySMove.setStyleSheet(button_style_grey)
        self.ySCn.setStyleSheet(button_style_grey)
        self.ySStop.setStyleSheet(button_style_red)
        self.ySCp.setStyleSheet(button_style_grey)
        self.ySSn.setStyleSheet(label_style_grey)
        self.ySSp.setStyleSheet(label_style_grey)
        self.ySHn.setStyleSheet(label_style_grey)
        self.ySHp.setStyleSheet(label_style_grey)
        self.yIdleS.setStyleSheet(label_style_grey)

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
        self.zSN = QPushButton("Upstream")
        self.zSP = QPushButton("Downstream")
        self.zSStep = QLineEdit("0")
        self.zSAbsPos = QLineEdit("0")
        self.zSMove = QPushButton("MOVE")
        self.zSCn = QPushButton("Upstream")
        self.zSStop = QPushButton("STOP")
        self.zSCp = QPushButton("Downstream")
        self.zSSn = QLabel("Upstream  ")
        self.zSSp = QLabel("Downstream")
        self.zSHn = QLabel("Upstream  ")
        self.zSHp = QLabel("Downstream")
        self.zIdleS = QLabel("IDLE")
        self.zStepS = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.zIdleS.setAlignment(Qt.AlignCenter)
        self.zStepS.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.zSN.setStyleSheet(button_style_grey)
        self.zSP.setStyleSheet(button_style_grey)
        self.zSMove.setStyleSheet(button_style_grey)
        self.zSCn.setStyleSheet(button_style_grey)
        self.zSStop.setStyleSheet(button_style_red)
        self.zSCp.setStyleSheet(button_style_grey)
        self.zSSn.setStyleSheet(label_style_grey)
        self.zSSp.setStyleSheet(label_style_grey)
        self.zSHn.setStyleSheet(label_style_grey)
        self.zSHp.setStyleSheet(label_style_grey)
        self.zIdleS.setStyleSheet(label_style_grey)

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

    def objective_window(self) -> QWidget:
        """Return the objective window.

        This method returns the controls and motor status indicators for the
        objective stage.

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

        # Define widget style sheets.
        button_style_grey = "background-color: lightgrey"
        button_style_red = "background-color: red"
        label_style_grey = "background-color: lightgrey; border: 1px solid black;"

        # Set column labels.
        layout.addWidget(QLabel("<b>Axis</b>"), 1, 0, 1, 1)
        layout.addWidget(QLabel("<b>Increment Position</b>"), 1, 1, 1, 2)
        layout.addWidget(QLabel("<b>Step Size</b>"), 1, 3, 1, 1)
        layout.addWidget(QLabel("<b>Absolute Position</b>"), 1, 4, 1, 1)
        layout.addWidget(QLabel("<b>Continual Motion</b>"), 1, 6, 1, 3)
        layout.addWidget(QLabel("<b>Soft Limits</b>"), 1, 9, 1, 2)
        layout.addWidget(QLabel("<b>Hard Limits</b>"), 1, 11, 1, 2)
        layout.addWidget(QLabel("<b>Current Position</b>"), 1, 13, 1, 1)
        layout.addWidget(QLabel("<b>Motor Status</b>"), 1, 14, 1, 1)

        # ----------------------------------------------------------------------
        #   X Objective Axis
        # ---------------------------------------------------------------------

        # Create interactive widgets.
        self.xON = QPushButton("In")
        self.xOP = QPushButton("Out")
        self.xOStep = QLineEdit("0")
        self.xOAbsPos = QLineEdit("0")
        self.xOMove = QPushButton("MOVE")
        self.xOCn = QPushButton("In")
        self.xOStop = QPushButton("STOP")
        self.xOCp = QPushButton("Out")
        self.xOSn = QLabel("In")
        self.xOSp = QLabel("Out")
        self.xOHn = QLabel("In")
        self.xOHp = QLabel("Out")
        self.xIdleO = QLabel("IDLE")
        self.xStepO = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.xIdleO.setAlignment(Qt.AlignCenter)
        self.xStepO.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.xON.setStyleSheet(button_style_grey)
        self.xOP.setStyleSheet(button_style_grey)
        self.xOMove.setStyleSheet(button_style_grey)
        self.xOCn.setStyleSheet(button_style_grey)
        self.xOStop.setStyleSheet(button_style_red)
        self.xOCp.setStyleSheet(button_style_grey)
        self.xOSn.setStyleSheet(label_style_grey)
        self.xOSp.setStyleSheet(label_style_grey)
        self.xOHn.setStyleSheet(label_style_grey)
        self.xOHp.setStyleSheet(label_style_grey)
        self.xIdleO.setStyleSheet(label_style_grey)

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
        self.yON = QPushButton("Up")
        self.yOP = QPushButton("Down")
        self.yOStep = QLineEdit("0")
        self.yOAbsPos = QLineEdit("0")
        self.yOMove = QPushButton("MOVE")
        self.yOCn = QPushButton("Up")
        self.yOStop = QPushButton("STOP")
        self.yOCp = QPushButton("Down")
        self.yOSn = QLabel("Up")
        self.yOSp = QLabel("Down")
        self.yOHn = QLabel("Up")
        self.yOHp = QLabel("Down")
        self.yIdleO = QLabel("IDLE")
        self.yStepO = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.yIdleO.setAlignment(Qt.AlignCenter)
        self.yStepO.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.yON.setStyleSheet(button_style_grey)
        self.yOP.setStyleSheet(button_style_grey)
        self.yOMove.setStyleSheet(button_style_grey)
        self.yOCn.setStyleSheet(button_style_grey)
        self.yOStop.setStyleSheet(button_style_red)
        self.yOCp.setStyleSheet(button_style_grey)
        self.yOSn.setStyleSheet(label_style_grey)
        self.yOSp.setStyleSheet(label_style_grey)
        self.yOHn.setStyleSheet(label_style_grey)
        self.yOHp.setStyleSheet(label_style_grey)
        self.yIdleO.setStyleSheet(label_style_grey)

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
        self.zON = QPushButton("Upstream")
        self.zOP = QPushButton("Downstream")
        self.zOStep = QLineEdit("0")
        self.zOAbsPos = QLineEdit("0")
        self.zOMove = QPushButton("MOVE")
        self.zOCn = QPushButton("Upstream")
        self.zOStop = QPushButton("STOP")
        self.zOCp = QPushButton("Downstream")
        self.zOSn = QLabel("Upstream  ")
        self.zOSp = QLabel("Downstream")
        self.zOHn = QLabel("Upstream  ")
        self.zOHp = QLabel("Downstream")
        self.zIdleO = QLabel("IDLE")
        self.zStepO = QLabel("<b>STEPS</b>")

        # Set label alignment.
        self.zIdleO.setAlignment(Qt.AlignCenter)
        self.zStepO.setAlignment(Qt.AlignCenter)

        # Style interactive widgets.
        self.zON.setStyleSheet(button_style_grey)
        self.zOP.setStyleSheet(button_style_grey)
        self.zOMove.setStyleSheet(button_style_grey)
        self.zOCn.setStyleSheet(button_style_grey)
        self.zOStop.setStyleSheet(button_style_red)
        self.zOCp.setStyleSheet(button_style_grey)
        self.zOSn.setStyleSheet(label_style_grey)
        self.zOSp.setStyleSheet(label_style_grey)
        self.zOHn.setStyleSheet(label_style_grey)
        self.zOHp.setStyleSheet(label_style_grey)
        self.zIdleO.setStyleSheet(label_style_grey)

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

    def base_window(self) -> QTextBrowser:
        """Return the base window.

        This method returns the user interface's base window containing the
        program status window, position save controls, configuration file
        controls, and current position unit controls.

        Returns
        -------
        QWidget
            Window representing the objective interactive widgets.
        """

        # Initialize the text browser window.
        self.textWindow = QTextBrowser()
        self.textWindow.setAcceptRichText(True)
        self.textWindow.setOpenExternalLinks(True)
        self.textWindow.setVerticalScrollBar(QScrollBar())

        # Save and load position functionality.
        self.savePos = QPushButton("Save Position")
        self.loadPos = QPushButton("Load Position")
        self.deletePos = QPushButton("Delete Position")
        self.clearPos = QPushButton("Clear All Positions")
        self.posSelect = QComboBox()
        self.posLabel = QLineEdit("Position Label")

        # Add items to the saved positions drop down menu.
        self.posSelect.addItem("--None--")
        for key in self.savedPos.keys():
            self.posSelect.addItem(key)

        # Set button style sheets.
        self.savePos.setStyleSheet("background-color: lightgrey")
        self.loadPos.setStyleSheet("background-color: lightgrey")
        self.deletePos.setStyleSheet("background-color: lightgrey")
        self.clearPos.setStyleSheet("background-color: lightgrey")

        # Set the save and load layout.
        self.posWindow = QWidget()
        layout = QGridLayout()
        layout.addWidget(QLabel("<b>Save and Load Position</b>"), 0, 0, 1, 5)
        layout.addWidget(self.posSelect, 1, 0, 1, 2)
        layout.addWidget(self.loadPos, 2, 0, 1, 1)
        layout.addWidget(self.deletePos, 2, 1, 1, 1)
        layout.addWidget(self.posLabel, 1, 2, 1, 1)
        layout.addWidget(self.savePos, 1, 3, 1, 1)
        layout.addWidget(self.clearPos, 2, 2, 1, 2)
        self.posWindow.setLayout(layout)

        # Progran-configuration functionality.
        self.configWindow = QWidget()
        self.loadConfig = QPushButton("Load Config")
        self.saveConfig = QPushButton("Save Config")
        self.loadConfig.setStyleSheet("background-color: lightgrey")
        self.saveConfig.setStyleSheet("background-color: lightgrey")

        # Set the program configuration layout.
        self.configWindow = QWidget()
        layout = QGridLayout()
        layout.addWidget(QLabel("<b>Program Configuration</b>"), 0, 0, 1, 2)
        layout.addWidget(self.loadConfig, 1, 0, 1, 2)
        layout.addWidget(self.saveConfig, 2, 0, 1, 2)
        self.configWindow.setLayout(layout)

        # Unit conversion functionality.
        self.positionUnits = QPushButton("Microns")
        self.positionUnits.setStyleSheet("background-color: lightgrey")
        self.positionUnits.setCheckable(True)

        # Set units window layout.
        self.unitsWindow = QWidget()
        layout = QGridLayout()
        layout.addWidget(QLabel("<b>Current Position Units</b>"), 0, 0, 1, 1)
        layout.addWidget(self.positionUnits, 1, 0, 2, 1)
        self.unitsWindow.setLayout(layout)

        # Create base window.
        self.baseWindow = QWidget()
        layout = QGridLayout()
        layout.addWidget(self.textWindow, 0, 0, 3, 5)
        layout.addWidget(self.posWindow, 0, 5, 3, 5)
        layout.addWidget(self.configWindow, 0, 10, 3, 2)
        layout.addWidget(self.unitsWindow, 0, 12, 3, 2)
        self.baseWindow.setLayout(layout)

        return self.baseWindow


class CameraWindow(QMainWindow):
    """Generate detachable camera window.

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
    SHC : QPushButton
        Show Cross Hairs toggle push button.

    Methods
    -------
    camera_window()
        Create live feed window.
    save_image()
        Live stream image capture.
    """

    def __init__(self):
        """Initialize camera window.
        
        This method initializes the camera window by configuring the main
        winodw and connecting controls to control sequences.
        """

        super().__init__()

        # Organize window.
        dock = QDockWidget("Live Stream", self)
        dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        dock.setFeatures(dock.DockWidgetFloatable)
        dock.setWidget(self.camera_window())
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

        # Save image functionality.
        self.WCB.clicked.connect(self.save_image)

    def camera_window(self) -> QWidget:
        """Create live feed window.

        Returns
        -------
        QWidget
            Window representing the live feed and interactive widgets.
        
        Notes
        -----
        This method creates the live feed by repeatedly calling for an image
        from the camera. It takes the received Numpy array and displays it on
        a matplotlib plot. This is a very poor way of displaying a video and
        should be looked into improving as it may significantly reduce the
        latency of the program.
        """

        def updateData() -> None:
            """Update live feed display.

            This method updates the live feed display by calling for a new
            image and plotting the returned Numpy array on a matplotlib plot.

            Notes
            -----
            The red cross hair is added by changing the central five rows and
            columns of pixels in the image to red (RGB=[225, 0, 0]).
            """

            # Get new image.
            self.image = np.copy(np.rot90(get_image()))
            height = self.image.shape[0]
            width = self.image.shape[1]

            # Generate cross hairs
            if self.SCH.isChecked():
                length = int(0.1 * min(height, width))
                xLine = np.full((5, 2 * length, 3), [225, 0, 0])
                yLine = np.full((length * 2, 5, 3), [225, 0, 0])
                self.image[height // 2 - 2:height // 2 + 3,
                           width // 2 - length:width // 2 + length] = xLine
                self.image[height // 2 - length:height // 2 +
                           length:, width // 2 - 2:width // 2 + 3] = yLine

            # Update image.
            self.img.setImage(np.fliplr(np.rot90(self.image, 2)))
            QTimer.singleShot(75, updateData)

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

        layout = QGridLayout()

        # Create, modify, and place image buttons.
        self.WCB = QPushButton("Image Capture")
        self.SCH = QPushButton("Show Cross Hairs")
        self.WCB.setStyleSheet("background-color: lightgrey")
        self.SCH.setStyleSheet("background-color: lightgrey")
        self.SCH.setCheckable(True)
        layout.addWidget(win, 0, 0, 1, 2)
        layout.addWidget(self.WCB, 1, 0, 1, 1)
        layout.addWidget(self.SCH, 1, 1, 1, 1)

        self.cameraWindow.setLayout(layout)

        updateData()

        return self.cameraWindow

    def save_image(self) -> None:
        """Live stream image capture.

        This method saves a capture of the current live stream to the chosen
        directory.

        Notes
        -----
        The image will be saved as the Numpy array shown on the matplotlib
        plot. Thus, if the cross hairs button is turned on, the cross hairs
        will also be saved in the image.
        """

        params = {"parent": self,
                  "caption": "Save File",
                  "directory": "../figures",
                  "filter": "Image files (*.jpg *.jpeg)"}
        path, _ = QFileDialog.getSaveFileName(**params)

        plt.figure()
        plt.imshow(np.rot90(self.image, 3))
        plt.axis("off")
        plt.savefig(path, dpi=500, bbox_inches="tight")


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
    tab2 : QWidget
        Mode tab of the table window.
    tab3 : QWidget
        Hard Limits tab of the table window.
    tab4 : QWidget
        Soft Limits tab of the table window.
    tab5 : QWidget
        Zero tab of the table window.
    tab6 : QWidget
        Backlash tab of the table window.
    RDM1 : QRadioButton
        Transmission mode radio button.
    RDM2 : QRadioButton
        Reflection mode radio button.
    RDM3 : QRadioButton
        Visible Image mode radio button.
    RDM4 : QRadioButton
        Beamsplitter mode radio button.
    group : QButtonGroup
        Mode select button group.
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
    xSMM, ySMM, zSMM : QLabel
        Minimum and maximum label for the sample's x, y, and z dimensions.
    xOMM, yOMM, zOMM : QLabel
        Minimum and maximum label for the objective's x, y, and z dimensions.
    xSMin, xSMax, ySMin : QLineEdit
        Soft limit minimum for the sample's x, y, and z dimensions.
    ySMax, zSMin, zSMax : QLineEdit
        Soft limit maximum for the sample's x, y, and z dimensions.
    xOMin, yOMin, zOMin : QLineEdit
        Soft limit minimum for the objective's x, y, and z dimensions.
    xOMax, yOMax, zOMax : QLineEdit
        Soft limit maximum for the objective's x, y, and z dimensions.
    SSL : QPushButton
        Set soft limits button.
    SMSL : QPushButton
        Set minimal soft limits button.
    SESL : QPushButton
        Set maximal soft limits button.
    xSOffset, ySOffset, zSOffset : QLabel
        Current offset label for the sample's x, y, and z dimensions.
    xSZero, ySZero, zSZero : QPushButton
        Button to zero the sample's x, y, and z dimensions.
    xSActual, ySActual, zSActual : QPushButton
        B, dimensions.
    xOOffset, yOOffset, zOOffset : QLabel
        Current offset label for the objective's x, y, and z dimensions.
    xOZero, yOZero, zOZero : QPushButton
        Button to zero the objective's x, y, and z dimensions.
    xOActual, yOActual, zOActual : QPushButton
        Button to display actual values for the objective's x, y, and z
        dimensions.
    zeroAll : QPushButton
        Button to zero all stages.
    allActual : QPushButton
        Button to change all displays to actual values.
    xSB, ySB, zSB : QLineEdit
        Backlash input for the sample's x, y, and z dimensions.
    xOB, yOB, zOB : QLineEdit
        Backlash input for the objective's x, y, and z dimensions.
    SBL : QPushButton
        Update all backlash values button.
    """

    def __init__(self, parent: Any) -> None:
        """Initialize table.
        
        This method creates the main user interfaces tab window by setting the
        tabs and adding then to the main tab window. Then for each tab, the
        program creates the neccessary widgets and organizes them on the tabs
        layout.
        """

        self.parent = parent

        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Define tab windows.
        self.tabs = QTabWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()

        self.tabs.resize(3000, 1000)

        # Add tabs to window layout.
        self.tabs.addTab(self.tab2, "Mode")
        self.tabs.addTab(self.tab3, "Hard Limits")
        self.tabs.addTab(self.tab4, "Soft Limits")
        self.tabs.addTab(self.tab5, "Zero")
        self.tabs.addTab(self.tab6, "Backlash")

        # Define helpr function to get macro values as strings.
        def macro_str(label: str) -> str:
            return str(float(self.parent.macros[label]))

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

        # Group buttons together.
        self.group = QButtonGroup()
        self.group.addButton(self.RDM1)
        self.group.addButton(self.RDM2)
        self.group.addButton(self.RDM3)
        self.group.addButton(self.RDM4)

        # Organize widgets on tab layout.
        self.tab2.layout.addWidget(self.RDM1, 1, 0, 1, 1)
        self.tab2.layout.addWidget(self.RDM2, 2, 0, 1, 1)
        self.tab2.layout.addWidget(self.RDM3, 3, 0, 1, 1)
        self.tab2.layout.addWidget(self.RDM4, 4, 0, 1, 1)

        # Set position customization widgets
        self.TMTM = QLineEdit(macro_str("TRANSMISSION_POSITION"))
        self.TMRM = QLineEdit(macro_str("REFLECTION_POSITION"))
        self.TMVM = QLineEdit(macro_str("VISIBLE_IMAGE_POSITION"))
        self.TMBM = QLineEdit(macro_str("BEAMSPLITTER_POSITION"))

        # Add position widgets to the tab layout.
        self.tab2.layout.addWidget(self.TMTM, 1, 1, 1, 1)
        self.tab2.layout.addWidget(self.TMRM, 2, 1, 1, 1)
        self.tab2.layout.addWidget(self.TMVM, 3, 1, 1, 1)
        self.tab2.layout.addWidget(self.TMBM, 4, 1, 1, 1)

        # Define set position buttons.
        self.TMTMbutton = QPushButton("Set Position")
        self.TMRMbutton = QPushButton("Set Position")
        self.TMVMbutton = QPushButton("Set Position")
        self.TMBMbutton = QPushButton("Set Position")

        # Add set position buttons to the tab layout.
        self.tab2.layout.addWidget(self.TMTMbutton, 1, 2, 1, 1)
        self.tab2.layout.addWidget(self.TMRMbutton, 2, 2, 1, 1)
        self.tab2.layout.addWidget(self.TMVMbutton, 3, 2, 1, 1)
        self.tab2.layout.addWidget(self.TMBMbutton, 4, 2, 1, 1)

        self.tab2.layout.addWidget(QLabel("<b>Motor Control</b>"), 5, 0, 1, 4)
        longLabel = "<i>Enable or disable the THORLABS motor and move to home position.</i>"
        self.tab2.layout.addWidget(QLabel(longLabel), 6, 0, 1, 4)

        # THORLABS/mode motor controls.
        self.enableDisable = QPushButton("Disable")
        self.home = QPushButton("Home Motor")
        self.tab2.layout.addWidget(self.enableDisable, 7, 0, 1, 1)
        self.tab2.layout.addWidget(self.home, 7, 1, 1, 2)

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
        self.tab3.layout.addWidget(QLabel("<i>In, Out</i>"), 1, 1, 1, 1)
        self.tab3.layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("<i>Up, Down</i>"), 3, 1, 1, 1)
        self.tab3.layout.addWidget(QLabel("Vertical:"), 4, 0, 1, 1)
        self.tab3.layout.addWidget(QLabel("<i>Upstream, Downstream</i>"), 5, 1, 1, 1)
        self.tab3.layout.addWidget(QLabel("Focus:"), 6, 0, 1, 1)
        self.tab3.layout.addWidget(self.xSMM, 2, 1, 1, 1)
        self.tab3.layout.addWidget(self.ySMM, 4, 1, 1, 1)
        self.tab3.layout.addWidget(self.zSMM, 6, 1, 1, 1)

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
        self.tab3.layout.addWidget(QLabel("<i>In, Out</i>"), 1, 3, 1, 1)
        self.tab3.layout.addWidget(QLabel("Horizontal:"), 2, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("<i>Up, Down</i>"), 3, 3, 1, 1)
        self.tab3.layout.addWidget(QLabel("Vertical:"), 4, 2, 1, 1)
        self.tab3.layout.addWidget(QLabel("<i>Upstream, Downstream</i>"), 5, 3, 1, 1)
        self.tab3.layout.addWidget(QLabel("Focus:"), 6, 2, 1, 1)
        self.tab3.layout.addWidget(self.xOMM, 2, 3, 1, 1)
        self.tab3.layout.addWidget(self.yOMM, 4, 3, 1, 1)
        self.tab3.layout.addWidget(self.zOMM, 6, 3, 1, 1)

        # Set tab layout.
        self.tab3.setLayout(self.tab3.layout)

        # ---------------------------------------------------------------------
        #   Tab 4
        # ---------------------------------------------------------------------

        # Define tab layout.
        self.tab4.layout = QGridLayout()

        # Define interactive sample widgets.
        self.xSMin = QLineEdit(macro_str("XSMIN_SOFT_LIMIT"))
        self.ySMin = QLineEdit(macro_str("YSMIN_SOFT_LIMIT"))
        self.zSMin = QLineEdit(macro_str("ZSMIN_SOFT_LIMIT"))
        self.xSMax = QLineEdit(macro_str("XSMAX_SOFT_LIMIT"))
        self.ySMax = QLineEdit(macro_str("YSMAX_SOFT_LIMIT"))
        self.zSMax = QLineEdit(macro_str("ZSMAX_SOFT_LIMIT"))

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
        longLabel = "<i>The motors will move 'backlash' steps past the low limit before moving back to the lower limit.</i>"
        softLimLabel = QLabel(longLabel)
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
        self.xSOffset = QLabel("Offset")
        self.ySOffset = QLabel("Offset")
        self.zSOffset = QLabel("Offset")
        self.xSZero = QPushButton("ZERO")
        self.ySZero = QPushButton("ZERO")
        self.zSZero = QPushButton("ZERO")
        self.xSActual = QPushButton("Actual")
        self.ySActual = QPushButton("Actual")
        self.zSActual = QPushButton("Actual")

        # Style interactive sample widgets.
        self.xSZero.setStyleSheet("background-color: lightgrey")
        self.ySZero.setStyleSheet("background-color: lightgrey")
        self.zSZero.setStyleSheet("background-color: lightgrey")
        self.xSActual.setStyleSheet("background-color: lightgrey")
        self.ySActual.setStyleSheet("background-color: lightgrey")
        self.zSActual.setStyleSheet("background-color: lightgrey")

        # Organize sample widgets in the tab layout.
        self.tab5.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 3)
        self.tab5.layout.addWidget(QLabel("<i>Offset<i>"), 1, 1, 1, 1)
        self.tab5.layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        self.tab5.layout.addWidget(QLabel("Vertical:"), 3, 0, 1, 1)
        self.tab5.layout.addWidget(QLabel("Focus:"), 4, 0, 1, 1)
        self.tab5.layout.addWidget(self.xSOffset, 2, 1, 1, 1)
        self.tab5.layout.addWidget(self.ySOffset, 3, 1, 1, 1)
        self.tab5.layout.addWidget(self.zSOffset, 4, 1, 1, 1)
        self.tab5.layout.addWidget(self.xSZero, 2, 2, 1, 1)
        self.tab5.layout.addWidget(self.ySZero, 3, 2, 1, 1)
        self.tab5.layout.addWidget(self.zSZero, 4, 2, 1, 1)
        self.tab5.layout.addWidget(self.xSActual, 2, 3, 1, 1)
        self.tab5.layout.addWidget(self.ySActual, 3, 3, 1, 1)
        self.tab5.layout.addWidget(self.zSActual, 4, 3, 1, 1)

        # Define interactive objective widgets.
        self.xOOffset = QLabel("Offset")
        self.yOOffset = QLabel("Offset")
        self.zOOffset = QLabel("Offset")
        self.xOZero = QPushButton("ZERO")
        self.yOZero = QPushButton("ZERO")
        self.zOZero = QPushButton("ZERO")
        self.xOActual = QPushButton("Actual")
        self.yOActual = QPushButton("Actual")
        self.zOActual = QPushButton("Actual")

        # Style interactive sample widgets.
        self.xOZero.setStyleSheet("background-color: lightgrey")
        self.yOZero.setStyleSheet("background-color: lightgrey")
        self.zOZero.setStyleSheet("background-color: lightgrey")
        self.xOActual.setStyleSheet("background-color: lightgrey")
        self.yOActual.setStyleSheet("background-color: lightgrey")
        self.zOActual.setStyleSheet("background-color: lightgrey")

        # Organize sample widgets in the tab layout.
        self.tab5.layout.addWidget(QLabel("<b>Objective</b>"), 0, 4, 1, 3)
        self.tab5.layout.addWidget(QLabel("<i>Offset<i>"), 1, 5, 1, 1)
        self.tab5.layout.addWidget(QLabel("Horizontal:"), 2, 4, 1, 1)
        self.tab5.layout.addWidget(QLabel("Vertical:"), 3, 4, 1, 1)
        self.tab5.layout.addWidget(QLabel("Focus:"), 4, 4, 1, 1)
        self.tab5.layout.addWidget(self.xOOffset, 2, 5, 1, 1)
        self.tab5.layout.addWidget(self.yOOffset, 3, 5, 1, 1)
        self.tab5.layout.addWidget(self.zOOffset, 4, 5, 1, 1)
        self.tab5.layout.addWidget(self.xOZero, 2, 6, 1, 1)
        self.tab5.layout.addWidget(self.yOZero, 3, 6, 1, 1)
        self.tab5.layout.addWidget(self.zOZero, 4, 6, 1, 1)
        self.tab5.layout.addWidget(self.xOActual, 2, 7, 1, 1)
        self.tab5.layout.addWidget(self.yOActual, 3, 7, 1, 1)
        self.tab5.layout.addWidget(self.zOActual, 4, 7, 1, 1)

        self.zeroAll = QPushButton("Zero All Stages")
        self.zeroAll.setStyleSheet("background-color: lightgrey")
        self.tab5.layout.addWidget(self.zeroAll, 5, 0, 1, 4)

        self.allActual = QPushButton("Display All Actual Values")
        self.allActual.setStyleSheet("background-color: lightgrey")
        self.tab5.layout.addWidget(self.allActual, 5, 4, 1, 4)

        # Add information labels.
        zeroLabel = QLabel("<i>Cannot zero when displaying actual values.</i>")
        zeroLabel.setWordWrap(True)
        self.tab5.layout.addWidget(zeroLabel, 7, 0, 1, 4)

        # Set tab layout.
        self.tab5.setLayout(self.tab5.layout)

        # ---------------------------------------------------------------------
        #   Tab 6
        # ---------------------------------------------------------------------

        self.tab6.layout = QGridLayout()

        # Define interactive sample widgets.
        self.xSB = QLineEdit(macro_str("XS_BACKLASH"))
        self.ySB = QLineEdit(macro_str("YS_BACKLASH"))
        self.zSB = QLineEdit(macro_str("ZS_BACKLASH"))

        # Organize sample widgets in the tab layout.
        self.tab6.layout.addWidget(QLabel("<b>Sample</b>"), 0, 0, 1, 3)
        self.tab6.layout.addWidget(QLabel("<i>Backlash</i>"), 1, 1, 1, 1)
        self.tab6.layout.addWidget(QLabel("Horizontal:"), 2, 0, 1, 1)
        self.tab6.layout.addWidget(QLabel("Vertical:"), 3, 0, 1, 1)
        self.tab6.layout.addWidget(QLabel("Focus:"), 4, 0, 1, 1)
        self.tab6.layout.addWidget(self.xSB, 2, 1, 1, 1)
        self.tab6.layout.addWidget(self.ySB, 3, 1, 1, 1)
        self.tab6.layout.addWidget(self.zSB, 4, 1, 1, 1)

        # Define interactive objective widgets.
        self.xOB = QLineEdit(macro_str("XO_BACKLASH"))
        self.yOB = QLineEdit(macro_str("YO_BACKLASH"))
        self.zOB = QLineEdit(macro_str("ZO_BACKLASH"))

        # Organize objective widgets in the tab layout.
        self.tab6.layout.addWidget(QLabel("<b>Objective</b>"), 0, 2, 1, 3)
        self.tab6.layout.addWidget(QLabel("<i>Backlash</i>"), 1, 3, 1, 1)
        self.tab6.layout.addWidget(QLabel("Horizontal:"), 2, 2, 1, 1)
        self.tab6.layout.addWidget(QLabel("Vertical:"), 3, 2, 1, 1)
        self.tab6.layout.addWidget(QLabel("Focus:"), 4, 2, 1, 1)
        self.tab6.layout.addWidget(self.xOB, 2, 3, 1, 1)
        self.tab6.layout.addWidget(self.yOB, 3, 3, 1, 1)
        self.tab6.layout.addWidget(self.zOB, 4, 3, 1, 1)

        # Define, style, and organize additional interactive widgets.
        self.SBL = QPushButton("Update Backlash Values")
        self.SBL.setStyleSheet("background-color: lightgrey")
        self.tab6.layout.addWidget(self.SBL, 5, 0, 1, 4)

        # Add information labels.
        longLabel = "<i>Backlash is applied when moving negitively. The motor will move 'backlash' steps past the target position before returning to the target position</i>"
        backlashLabel = QLabel(longLabel)
        backlashLabel.setWordWrap(True)
        self.tab6.layout.addWidget(backlashLabel, 6, 0, 1, 4)

        self.tab6.setLayout(self.tab6.layout)

        # Set window layout.
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
