"""Create widgets interactive nature.

The controller module brings life to the GUI defined through the gui module by
connecting widgets up to control sequences that bring about change.
"""


# Import package dependencies.
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from epics import ca, caput, caget, PV

# Import objects for type annotations.
from typing import Any, Literal, Dict
from PyQt5.QtWidgets import QLineEdit, QFileDialog
from gui import GUI

# Import file dependencies.
from thorlabs_motor_control import changeMode
from globals import *


# Set up epics environment.
ca.find_libca()


class Controller(object):
    """Connect GUI widgets to control sequences.

    The Controller class takes interactive widgets such as QPushButton's
    QLineEdit's, etc. and allows for meaningful engagement with a user.

    Parameters
    ----------
    gui : GUI
        The GUI object with which the Controller class controls.
    modeMotor : Motor
        The initialized THORLABS motor unit controlling the microscope mode.

    Attributes
    ----------
    gui : GUI
        The GUi object with which the Controller class controls.
    modeMotor : Motor
        The initialized THORLABS motor unit controlling the microscope mode.

    Methods
    -------
    connectSignals()
        Connect the widgets to a control sequence.
    saveImage(fileName, image)
        Control sequence to capture an image of the live feed.
    modeState(mode, modeMotor)
        Control sequence to change the microscope mode.
    incPos(object, axis, direction, step)
        Control sequence to increment sample and objective stage motors.
    absMove(object, axis, pos)
        Control sequence to move the sample and objective stage motors to a set
        point.
    continuousMotion(object, axis, type)
        Control sequence for the continuous motion of the sample and objective
        stages.
    moveToPos(object, axis)
        Control sequence to move the sample and objective stages to an absolute
        position.
    updateAbsPos(object, axis, direction, step)
        Control sequence to update the absolute position line edit widget.
    updateSoftLimits(buttonID)
        Control sequence to set soft limits to the inputted soft limits.
    updateBacklash()
        Control sequence to update backlash values.
    zeroPos(object, axis)
        Control sequence to zero the current motor positions.
    setRelPos(object, axis)
        Control sequence to update the relative position global variables.
    """

    def __init__(self, gui: GUI, modeMotor: Any) -> None:
        """Initialize the Controller."""
        self.gui = gui
        self.modeMotor = modeMotor
        self.GL = globals()

        self.monitorPVs()
        self.connectSignals()
    
    def monitorPVs(self) -> None:
        """Configure and initiallize PVs.

        This method initializes the line-edits to the PV values on program
        startup. Additionally, it connects PVs that need monitoring to
        callback functions.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Set step line edits to current PV values.
        self.gui.xSStep.setText(str(caget(self.GL["XSSTEP"])))
        self.gui.ySStep.setText(str(caget(self.GL["YSSTEP"])))
        self.gui.zSStep.setText(str(caget(self.GL["ZSSTEP"])))
        self.gui.xOStep.setText(str(caget(self.GL["XOSTEP"])))
        self.gui.yOStep.setText(str(caget(self.GL["YOSTEP"])))
        self.gui.zOStep.setText(str(caget(self.GL["ZOSTEP"])))

        # Set absolute position line edits to current PV values.
        self.gui.xSAbsPos.setText(str(caget(self.GL["XSABSPOS"])))
        self.gui.ySAbsPos.setText(str(caget(self.GL["YSABSPOS"])))
        self.gui.zSAbsPos.setText(str(caget(self.GL["ZSABSPOS"])))
        self.gui.xOAbsPos.setText(str(caget(self.GL["XOABSPOS"])))
        self.gui.yOAbsPos.setText(str(caget(self.GL["YOABSPOS"])))
        self.gui.zOAbsPos.setText(str(caget(self.GL["ZOABSPOS"])))

        # Set backlash line edits to current PV values.
        self.gui.tab.xSB.setText(str(caget(self.GL["XSB"])))
        self.gui.tab.ySB.setText(str(caget(self.GL["YSB"])))
        self.gui.tab.zSB.setText(str(caget(self.GL["ZSB"])))
        self.gui.tab.xOB.setText(str(caget(self.GL["XOB"])))
        self.gui.tab.yOB.setText(str(caget(self.GL["YOB"])))
        self.gui.tab.zOB.setText(str(caget(self.GL["ZOB"])))

        self.PV_XSABSPOS = PV(pvname=self.GL["XSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_ySABSPOS = PV(pvname=self.GL["YSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zSABSPOS = PV(pvname=self.GL["ZSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_XOABSPOS = PV(pvname=self.GL["XOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_yOABSPOS = PV(pvname=self.GL["YOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zOABSPOS = PV(pvname=self.GL["ZOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)

        self.PV_XSSTATE = PV(pvname=self.GL["XSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YSSTATE = PV(pvname=self.GL["YSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZSSTATE = PV(pvname=self.GL["ZSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_XOSTATE = PV(pvname=self.GL["XOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YOSTATE = PV(pvname=self.GL["YOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZOSTATE = PV(pvname=self.GL["ZOSTATE"], auto_monitor=True, callback=self.motorStatus)

        print("-*- PVs configured and initialized. -*-")

    def connectSignals(self) -> None:
        """Connect widgets and control sequences.

        This method connects each of the widgets on the gui with a control
        sequence to update the display or interface with hardware.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Save image functionality.
        self.gui.WCB.clicked.connect(self.saveImage)

        # Mode select functionality.
        self.gui.tab.RDM1.pressed.connect(partial(self.modeState, 1,
                                                  self.modeMotor))
        self.gui.tab.RDM2.pressed.connect(partial(self.modeState, 2,
                                                  self.modeMotor))
        self.gui.tab.RDM3.pressed.connect(partial(self.modeState, 3,
                                                  self.modeMotor))
        self.gui.tab.RDM4.pressed.connect(partial(self.modeState, 4,
                                                  self.modeMotor))

        # Increment sample and objective stage functionality.
        self.gui.xSN.clicked.connect(partial(self.incPos, "S", "X", "N",
                                             self.gui.xSStep))
        self.gui.xSP.clicked.connect(partial(self.incPos, "S", "X", "P",
                                             self.gui.xSStep))
        self.gui.ySN.clicked.connect(partial(self.incPos, "S", "Y", "N",
                                             self.gui.ySStep))
        self.gui.ySP.clicked.connect(partial(self.incPos, "S", "Y", "P",
                                             self.gui.ySStep))
        self.gui.zSN.clicked.connect(partial(self.incPos, "S", "Z", "N",
                                             self.gui.zSStep))
        self.gui.zSP.clicked.connect(partial(self.incPos, "S", "Z", "P",
                                             self.gui.zSStep))
        self.gui.xON.clicked.connect(partial(self.incPos, "O", "X", "N",
                                             self.gui.xOStep))
        self.gui.xOP.clicked.connect(partial(self.incPos, "O", "X", "P",
                                             self.gui.xOStep))
        self.gui.yON.clicked.connect(partial(self.incPos, "O", "Y", "N",
                                             self.gui.yOStep))
        self.gui.yOP.clicked.connect(partial(self.incPos, "O", "Y", "P",
                                             self.gui.yOStep))
        self.gui.zON.clicked.connect(partial(self.incPos, "O", "Z", "N",
                                             self.gui.zOStep))
        self.gui.zOP.clicked.connect(partial(self.incPos, "O", "Z", "P",
                                             self.gui.zOStep))

        # Move sample and objective stage to absolute position functionality.
        self.gui.xSMove.clicked.connect(partial(self.absMove, "S", "X"))
        self.gui.ySMove.clicked.connect(partial(self.absMove, "S", "Y"))
        self.gui.zSMove.clicked.connect(partial(self.absMove, "S", "Z"))
        self.gui.xOMove.clicked.connect(partial(self.absMove, "O", "X"))
        self.gui.yOMove.clicked.connect(partial(self.absMove, "O", "Y"))
        self.gui.zOMove.clicked.connect(partial(self.absMove, "O", "Z"))

        # Continuous motion of the sample and objective stages functionality.
        self.gui.xSCn.clicked.connect(partial(self.continuousMotion, "S", "X",
                                              "CN"))
        self.gui.xSStop.clicked.connect(partial(self.continuousMotion, "S",
                                                "X", "STOP"))
        self.gui.xSCp.clicked.connect(partial(self.continuousMotion, "S", "X",
                                              "CP"))
        self.gui.ySCn.clicked.connect(partial(self.continuousMotion, "S", "Y",
                                              "CN"))
        self.gui.ySStop.clicked.connect(partial(self.continuousMotion, "S",
                                                "Y", "STOP"))
        self.gui.ySCp.clicked.connect(partial(self.continuousMotion, "S", "Y",
                                              "CP"))
        self.gui.zSCn.clicked.connect(partial(self.continuousMotion, "S", "Z",
                                              "CN"))
        self.gui.zSStop.clicked.connect(partial(self.continuousMotion, "S",
                                                "Z", "STOP"))
        self.gui.zSCp.clicked.connect(partial(self.continuousMotion, "S", "Z",
                                              "CP"))
        self.gui.xOCn.clicked.connect(partial(self.continuousMotion, "O", "X",
                                              "CN"))
        self.gui.xOStop.clicked.connect(partial(self.continuousMotion, "O",
                                                "X", "STOP"))
        self.gui.xOCp.clicked.connect(partial(self.continuousMotion, "O", "X",
                                              "CP"))
        self.gui.yOCn.clicked.connect(partial(self.continuousMotion, "O", "Y",
                                              "CN"))
        self.gui.yOStop.clicked.connect(partial(self.continuousMotion, "O",
                                                "Y", "STOP"))
        self.gui.yOCp.clicked.connect(partial(self.continuousMotion, "O", "Y",
                                              "CP"))
        self.gui.zOCn.clicked.connect(partial(self.continuousMotion, "O", "Z",
                                              "CN"))
        self.gui.zOStop.clicked.connect(partial(self.continuousMotion, "O",
                                                "Z", "STOP"))
        self.gui.zOCp.clicked.connect(partial(self.continuousMotion, "O", "Z",
                                              "CP"))

        # Updating soft limits functionality.
        self.gui.tab.SSL.clicked.connect(partial(self.updateSoftLimits, 0))
        self.gui.tab.SESL.clicked.connect(partial(self.updateSoftLimits, 1))

        # Zero'ing absolute position functionality.
        self.gui.tab.xSZero.clicked.connect(partial(self.zeroPos, "S", "X"))
        self.gui.tab.ySZero.clicked.connect(partial(self.zeroPos, "S", "Y"))
        self.gui.tab.zSZero.clicked.connect(partial(self.zeroPos, "S", "Z"))
        self.gui.tab.xOZero.clicked.connect(partial(self.zeroPos, "O", "X"))
        self.gui.tab.yOZero.clicked.connect(partial(self.zeroPos, "O", "Y"))
        self.gui.tab.zOZero.clicked.connect(partial(self.zeroPos, "O", "Z"))
        self.gui.tab.SBL.clicked.connect(self.updateBacklash)

        print("-*- Widgets connected to control sequences. -*-")

    def saveImage(self) -> None:
        """Live stream image capture.

        This method saves a capture of the current live stream to the chosen
        directory.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        path, _ = QFileDialog.getSaveFileName(self, "Save File",
                "sample_capture", "Image files (*.jpg *.jpeg *.gif *png)")
        
        plt.figure()
        plt.imshow(np.rot90(self.gui.image, 1))
        plt.savefig(path)
        
        print(f"Image capture saved to: {path}")

    def modeState(self, mode: Literal[1, 2, 3, 4], modeMotor: Any) -> None:
        """Change microscope mode.

        This method is called when selecting a mode radio button to change
        the THORLABS motor to a different mode position.

        Parameters
        ----------
        mode : {1, 2, 3, 4}
            Encoded mode to move the THORLABS motor to.
        modeMotor : Motor Type
            Motor controlling the mode stage.

        Returns
        -------
        None
        """
        changeMode(mode=mode, modeMotor=modeMotor)

        print(f"Changing mode to mode {mode}.")

    def incPos(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"],
               direction: Literal["N", "P"], step: QLineEdit) -> None:
        """Increment motor position.

        Increment the motor defined by 'object' and 'axis' in the direction
        defined by 'direction' by the amount 'step'.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample or orbjective using "S" and "O",
            respectively.
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z using "X", "Y", "Z",
            respectively.
        direction : {"N", "P"}
            Defines increment direction as either negative or positibe using
            "N" and "P", respectively.
        step : QLineEdit
            float(QLineEdit.text()) defines the stepsize to use.

        Returns
        -------
        None
        """
        caput(self.GL[f"{axis}{object}STEP"], float(step.text()))

        absPos = caget(self.GL[f"{axis}{object}ABSPOS"])
        incPos = caget(self.GL[f"{axis}{object}STEP"])

        PHL = self.GL[f"{axis}{object}MAX_HARD_LIMIT"]
        NHL = self.GL[f"{axis}{object}MIN_HARD_LIMIT"]
        PSL = self.GL[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.GL[f"{axis}{object}MIN_SOFT_LIMIT"]

        if direction == "P" and absPos + incPos > PSL:
            caput(self.GL[f"{axis}{object}ABSPOS"], PSL)
            caput(self.GL[f"{axis}{object}MOVE"], 1)
        elif direction == "P" and absPos + incPos > PHL:
            caput(self.GL[f"{axis}{object}ABSPOS"], PHL)
            caput(self.GL[f"{axis}{object}MOVE"], 1)
        elif direction == "N" and absPos - incPos < NSL:
            caput(self.GL[f"{axis}{object}ABSPOS"], NSL)
            caput(self.GL[f"{axis}{object}MOVE"], 1)
        elif direction == "N" and absPos - incPos < NHL:
            caput(self.GL[f"{axis}{object}ABSPOS"], NHL)
            caput(self.GL[f"{axis}{object}MOVE"], 1)
        else:
            caput(self.GL[f"{axis}{object}{direction}"], 1)
        
        absPos = caget(self.GL[f"{axis}{object}ABSPOS"])
        print(f"Incremental movement to {axis}{object}ABSPOS = {absPos}.")
    
    def absMove(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"]) -> None:
        """Move sample or objective motor to specified position.

        This method moves the motor defined by 'object' and 'axis' to the
        absolute position defined by 'pos'.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample or orbjective using "S" and "O",
            respectively.
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z using "X", "Y", "Z",
            respectively.

        Returns
        -------
        None
        """
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos,
                    ("S", "Y"): self.gui.ySAbsPos, ("O", "Y"): self.gui.yOAbsPos,
                    ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        absPos = float(lineEdit[(object, axis)].text())

        PHL = self.GL[f"{axis}{object}MAX_HARD_LIMIT"]
        NHL = self.GL[f"{axis}{object}MIN_HARD_LIMIT"]
        PSL = self.GL[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.GL[f"{axis}{object}MIN_SOFT_LIMIT"]

        if absPos > PSL:
            caput(self.GL[f"{axis}{object}ABSPOS"], PSL)
        elif absPos > PHL:
            caput(self.GL[f"{axis}{object}ABSPOS"], PHL)
        elif absPos < NSL:
            caput(self.GL[f"{axis}{object}ABSPOS"], NSL)
        elif absPos < NHL:
            caput(self.GL[f"{axis}{object}ABSPOS"], NHL)
        else:
            caput(self.GL[f"{axis}{object}ABSPOS"], absPos)
        
        caput(self.GL[f"{axis}{object}MOVE"], 1)

        absPos = caget(self.GL[f"{axis}{object}ABSPOS"])
        print(f"Absolute movement to {axis}{object}ABSPOS = {absPos}.")
    
    def continuousMotion(self, object: Literal["S", "O"], axis:
                         Literal["X", "Y", "Z"], type:
                         Literal["CN", "STOP", "CP"]) -> None:
        """Control continuous motion of the sample and objective stages.

        This method allows for the continuous motion functionality of the
        sample and objective stages. It will invoke continuous positive motion,
        continuous negative motion, or cease of motion (dictated by 'type') of
        the motor defined by 'object' and 'axis'.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample or orbjective using "S" and "O",
            respectively.
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z using "X", "Y", "Z",
            respectively.
            Defines the motor axis as x, y, or z using 0, 1, 2, respectively.
        type : {"CN", "STOP", "CP"}
            Defines button type as either "continuous negative", "stop", or
            "continuous positive" using "CN", "STOP" and "CP", respectively.

        Returns
        -------
        None
        """
        if type == "CN":
            caput(self.GL[f"{axis}{object}CN"], -1000000)
        elif type == "CP":
            caput(self.GL[f"{axis}{object}CP"], 1000000)
        else:
            caput(self.GL[f"{axis}{object}CN"], 0)
            caput(self.GL[f"{axis}{object}CP"], 0)
            caput(self.GL[f"{axis}{object}STOP"], 1)
            caput(self.GL[f"{axis}{object}STOP"], 0)
        
        print(f"Change continuous movement to -> {type}.")

    def updateAbsPos(self, **kwargs: Dict) -> None:
        """Update absolute value line edit.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `motorStatus`: refer to PyEpics documentation
            for a list of all possible arguments for PV callback functions.
        
        Returns
        -------
        None
        """
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos,
                    ("S", "Y"): self.gui.ySAbsPos, ("O", "Y"): self.gui.yOAbsPos,
                    ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.GL.keys())
        vals = list(self.GL.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        lineEdit[(object, axis)].setText(str(value))

        print(f"Updating absolute position line edit to {value}.")

    def updateSoftLimits(self, buttonID: Literal[0, 1]) -> None:
        """Update sample and objective soft limits.

        This method updates the programs soft limits to the inputted amounts or
        extreme limits dependent on 'buttonID'.

        Parameters
        ----------
        buttonID : {0, 1}
            Integer representing the button pressed as being either SSL or SESL
            using a 0 or 1, respectively.

        Returns
        -------
        None
        """
        if buttonID:
            # Set soft limits to hard limits.
            XSMIN_SOFT_LIMIT = self.GL["XSMIN_HARD_LIMIT"]
            XSMAX_SOFT_LIMIT = self.GL["XSMAX_HARD_LIMIT"]
            YSMIN_SOFT_LIMIT = self.GL["YSMIN_HARD_LIMIT"]
            YSMAX_SOFT_LIMIT = self.GL["YSMAX_HARD_LIMIT"]
            ZSMIN_SOFT_LIMIT = self.GL["ZSMIN_HARD_LIMIT"]
            ZSMAX_SOFT_LIMIT = self.GL["ZSMAX_HARD_LIMIT"]
            XOMIN_SOFT_LIMIT = self.GL["XOMIN_HARD_LIMIT"]
            XOMAX_SOFT_LIMIT = self.GL["XOMAX_HARD_LIMIT"]
            YOMIN_SOFT_LIMIT = self.GL["YOMIN_HARD_LIMIT"]
            YOMAX_SOFT_LIMIT = self.GL["YOMAX_HARD_LIMIT"]
            ZOMIN_SOFT_LIMIT = self.GL["ZOMIN_HARD_LIMIT"]
            ZOMAX_SOFT_LIMIT = self.GL["ZOMAX_HARD_LIMIT"]

            # Update soft limit line edits.
            self.gui.tab.xSMin.setText(str(XSMIN_SOFT_LIMIT))
            self.gui.tab.xSMax.setText(str(XSMAX_SOFT_LIMIT))
            self.gui.tab.ySMin.setText(str(YSMIN_SOFT_LIMIT))
            self.gui.tab.ySMax.setText(str(YSMAX_SOFT_LIMIT))
            self.gui.tab.zSMin.setText(str(ZSMIN_SOFT_LIMIT))
            self.gui.tab.zSMax.setText(str(ZSMAX_SOFT_LIMIT))
            self.gui.tab.xOMin.setText(str(XOMIN_SOFT_LIMIT))
            self.gui.tab.xOMax.setText(str(XOMAX_SOFT_LIMIT))
            self.gui.tab.yOMin.setText(str(YOMIN_SOFT_LIMIT))
            self.gui.tab.yOMax.setText(str(YOMAX_SOFT_LIMIT))
            self.gui.tab.zOMin.setText(str(ZOMIN_SOFT_LIMIT))
            self.gui.tab.zOMax.setText(str(ZOMAX_SOFT_LIMIT))

        else:
            # Set soft limits to inputted values
            xsmin = float(self.gui.tab.xSMin.text())
            if xsmin < self.GL["XSMIN_HARD_LIMIT"]:
                XSMIN_SOFT_LIMIT = self.GL["XSMIN_HARD_LIMIT"]
                self.gui.tab.xSMin.setText(str(XSMIN_SOFT_LIMIT))
            else:
                XSMIN_SOFT_LIMIT = xsmin

            xsmax = float(self.gui.tab.xSMax.text())
            if xsmax > self.GL["XSMAX_HARD_LIMIT"]:
                XSMAX_SOFT_LIMIT = self.GL["XSMAX_HARD_LIMIT"]
                self.gui.tab.xSMax.setText(str(XSMAX_SOFT_LIMIT))
            else:
                XSMAX_SOFT_LIMIT = xsmax
            
            ysmin = float(self.gui.tab.ySMin.text())
            if ysmin < self.GL["YSMIN_HARD_LIMIT"]:
                YSMIN_SOFT_LIMIT = self.GL["YSMIN_HARD_LIMIT"]
                self.gui.tab.ySMin.setText(str(YSMIN_SOFT_LIMIT))
            else:
                YSMIN_SOFT_LIMIT = ysmin

            ysmax = float(self.gui.tab.ySMax.text())
            if ysmax > self.GL["YSMAX_HARD_LIMIT"]:
                YSMAX_SOFT_LIMIT = self.GL["YSMAX_HARD_LIMIT"]
                self.gui.tab.ySMax.setText(str(YSMAX_SOFT_LIMIT))
            else:
                YSMAX_SOFT_LIMIT = ysmax
            
            zsmin = float(self.gui.tab.zSMin.text())
            if zsmin < self.GL["ZSMIN_HARD_LIMIT"]:
                ZSMIN_SOFT_LIMIT = self.GL["ZSMIN_HARD_LIMIT"]
                self.gui.tab.zSMin.setText(str(ZSMIN_SOFT_LIMIT))
            else:
                ZSMIN_SOFT_LIMIT = zsmin

            zsmax = float(self.gui.tab.zSMax.text())
            if zsmax > self.GL["ZSMAX_HARD_LIMIT"]:
                ZSMAX_SOFT_LIMIT = self.GL["ZSMAX_HARD_LIMIT"]
                self.gui.tab.zSMax.setText(str(ZSMAX_SOFT_LIMIT))
            else:
                ZSMAX_SOFT_LIMIT = zsmax
            
            xomin = float(self.gui.tab.xOMin.text())
            if xomin < self.GL["XOMIN_HARD_LIMIT"]:
                XOMIN_SOFT_LIMIT = self.GL["XOMIN_HARD_LIMIT"]
                self.gui.tab.xOMin.setText(str(XOMIN_SOFT_LIMIT))
            else:
                XOMIN_SOFT_LIMIT = xomin

            xomax = float(self.gui.tab.xOMax.text())
            if xomax > self.GL["XOMAX_HARD_LIMIT"]:
                XOMAX_SOFT_LIMIT = self.GL["XOMAX_HARD_LIMIT"]
                self.gui.tab.xOMax.setText(str(XOMAX_SOFT_LIMIT))
            else:
                XOMAX_SOFT_LIMIT = xomax
            
            yomin = float(self.gui.tab.yOMin.text())
            if yomin < self.GL["YOMIN_HARD_LIMIT"]:
                YOMIN_SOFT_LIMIT = self.GL["YOMIN_HARD_LIMIT"]
                self.gui.tab.yOMin.setText(str(YOMIN_SOFT_LIMIT))
            else:
                YOMIN_SOFT_LIMIT = yomin

            yomax = float(self.gui.tab.yOMax.text())
            if yomax > self.GL["YOMAX_HARD_LIMIT"]:
                YOMAX_SOFT_LIMIT = self.GL["YOMAX_HARD_LIMIT"]
                self.gui.tab.yOMax.setText(str(YOMAX_SOFT_LIMIT))
            else:
                YOMAX_SOFT_LIMIT = yomax
            
            zomin = float(self.gui.tab.zOMin.text())
            if zomin < self.GL["ZOMIN_HARD_LIMIT"]:
                ZOMIN_SOFT_LIMIT = self.GL["ZOMIN_HARD_LIMIT"]
                self.gui.tab.zOMin.setText(str(ZOMIN_SOFT_LIMIT))
            else:
                ZOMIN_SOFT_LIMIT = zomin

            zomax = float(self.gui.tab.zOMax.text())
            if zomax > self.GL["ZOMAX_HARD_LIMIT"]:
                ZOMAX_SOFT_LIMIT = self.GL["ZOMAX_HARD_LIMIT"]
                self.gui.tab.zOMax.setText(str(ZOMAX_SOFT_LIMIT))
            else:
                ZOMAX_SOFT_LIMIT = zomax
            
        print(f"Updating soft limits, buttonID={buttonID}.")

    def updateBacklash(self) -> None:
        """Update backlash variables.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Set global backlash variables.
        caput(self.GL["XSB"], float(self.gui.tab.xSB.text()))
        caput(self.GL["YSB"], float(self.gui.tab.ySB.text()))
        caput(self.GL["ZSB"], float(self.gui.tab.zSB.text()))
        caput(self.GL["XOB"], float(self.gui.tab.xOB.text()))
        caput(self.GL["YOB"], float(self.gui.tab.yOB.text()))
        caput(self.GL["ZOB"], float(self.gui.tab.zOB.text()))

        print("Updating backlash values.")

    def zeroPos(self, object: Literal["S", "O"], axis:
                Literal["X", "Y", "Z"]) -> None:
        """Zero sample or objective axis position.

        This method zeros the absolute position line edit of the motor defined
        by 'object' and 'axis'.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample or orbjective using "S" and "O",
            respectively.
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z using "X", "Y", "Z",
            respectively.

        Returns
        -------
        None

        Notes
        -----
        The base position deifnes the actual motor position whereas the
        relative position defines the position displayed. Internal workings use
        base position but external workings use relative position.
        """
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos,
                    ("S", "Y"): self.gui.ySAbsPos, ("O", "Y"): self.gui.yOAbsPos,
                    ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        # Update the base and relative positions.
        self.GL[f"{axis}{object}_BASE_POSITION"] += self.GL[f"{axis}{object}_RELATIVE_POSITION"]
        self.GL[f"{axis}{object}_RELATIVE_POSITION"] = 0

        # Update absolute position line edit widget to 0.
        lineEdit[(object, axis)].setText("0")

        print(f"Zero'ing the {axis}{object}ABSPOS line edit.")

    def motorStatus(self, **kwargs: Dict) -> None:
        """Check and set motor status indicators.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `motorStatus`: refer to PyEpics documentation
            for a list of all possible arguments for PV callback functions.
        
        Returns
        -------
        None
        """
        motionLabels = {("S", "X", 0): self.gui.tab.xIdleS, ("S", "X", 1): self.gui.tab.xStopS,
                        ("S", "Y", 0): self.gui.tab.yIdleS, ("S", "Y", 1): self.gui.tab.yStopS,
                        ("S", "Z", 0): self.gui.tab.zIdleS, ("S", "Z", 1): self.gui.tab.zStopS,
                        ("O", "X", 0): self.gui.tab.xIdleO, ("O", "X", 1): self.gui.tab.xStopO,
                        ("O", "Y", 0): self.gui.tab.yIdleO, ("O", "Y", 1): self.gui.tab.yStopO,
                        ("O", "Z", 0): self.gui.tab.zIdleO, ("O", "Z", 1): self.gui.tab.zStopO}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.GL.keys())
        vals = list(self.GL.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        if value == 1:
            motionLabels[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
            motionLabels[(object, axis, 1)].setStyleSheet("background-color: #49eb34; border: 1px solid black;")
        elif value == 0:
            motionLabels[(object, axis, 0)].setStyleSheet("background-color: #49eb34; border: 1px solid black;")
            motionLabels[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        print("Checkiing motor status.")

