"""Create widgets interactive nature.

The controller module brings life to the GUI defined through the gui module by
connecting widgets up to control sequences that bring about change.
"""


# Import package dependencies.
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from epics import caput, caget, PV

# Import objects for type annotations.
from typing import Any, Literal
from PyQt5.QtWidgets import QLineEdit
from gui import GUI

# Import file dependencies.
from thorlabs_motor_control import changeMode
from globals import *


class Controller:
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
        print("Configuring and Initializing PVs.")

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
        self.gui.xSB.setText(str(caget(self.GL["XSB"])))
        self.gui.ySB.setText(str(caget(self.GL["YSB"])))
        self.gui.zSB.setText(str(caget(self.GL["ZSB"])))
        self.gui.xOB.setText(str(caget(self.GL["XOB"])))
        self.gui.yOB.setText(str(caget(self.GL["YOB"])))
        self.gui.zOB.setText(str(caget(self.GL["ZOB"])))

        self.PV_XSABSPOS = PV(pvname=self.gui.GL["XSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_ySABSPOS = PV(pvname=self.gui.GL["YSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zSABSPOS = PV(pvname=self.gui.GL["ZSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_XOABSPOS = PV(pvname=self.gui.GL["XOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_yOABSPOS = PV(pvname=self.gui.GL["YOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zOABSPOS = PV(pvname=self.gui.GL["ZOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)

        self.PV_XSSTATE = PV(pvname=self.gui.GL["XSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YSSTATE = PV(pvname=self.gui.GL["YSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZSSTATE = PV(pvname=self.gui.GL["ZSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_XOSTATE = PV(pvname=self.gui.GL["XOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YOSTATE = PV(pvname=self.gui.GL["YOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZOSTATE = PV(pvname=self.gui.GL["ZOSTATE"], auto_monitor=True, callback=self.motorStatus)

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
        print("Connecting widgets to control sequences.")

        # Save image functionality.
        self.gui.WCB.clicked.connect(partial(self.saveImage, self.gui.SIFN,
                                             self.gui.image))

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
        self.gui.xSMove.clicked.connect(partial(self.absMove, "S", "X",
                                                self.gui.xSAbsPos))
        self.gui.ySMove.clicked.connect(partial(self.absMove, "S", "Y",
                                                self.gui.ySAbsPos))
        self.gui.zSMove.clicked.connect(partial(self.absMove, "S", "Z",
                                                self.gui.zSAbsPos))
        self.gui.xOMove.clicked.connect(partial(self.absMove, "O", "X",
                                                self.gui.xOAbsPos))
        self.gui.yOMove.clicked.connect(partial(self.absMove, "O", "Y",
                                                self.gui.yOAbsPos))
        self.gui.zOMove.clicked.connect(partial(self.absMove, "O", "Z",
                                                self.gui.zOAbsPos))

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

    def saveImage(self, fileName: str, image: np.ndarray) -> None:
        """Live stream image capture.

        This method saves a capture of the current live stream to the current
        working directory with the filename given by "<fileName>.png".

        Parameters
        ----------
        fileName : str
            Name to save the image capture to.
        image : np.ndarray
            Numpy array representing the image data.

        Returns
        -------
        None
        """
        print("Save image to local working directory.")

        filename = fileName.text() + ".png"
        figure = plt.figure()
        plt.imshow(np.rot90(image, 1))
        figure.savefig(filename)

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
        print("Changing mode state.")

        changeMode(mode=mode, modeMotor=modeMotor)

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
        print(f"Moving to {axis}{object}ABSPOS = {absPos}")
    
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

        absPos = lineEdit[(object, axis)].text()

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
        print(f"Moving to {axis}{object}ABSPOS = {absPos}")
    
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

    def updateAbsPos(**kwargs):
        """
        """
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos,
                    ("S", "Y"): self.gui.ySAbsPos, ("O", "Y"): self.gui.yOAbsPos,
                    ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.GL.keys())
        vals = list(self.gui.GL.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        lineEdit[(object, axis)].setText(value)

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
                self.gui.tab.xSMin.setText(XSMIN_SOFT_LIMIT)
            else:
                XSMIN_SOFT_LIMIT = xsmin

            xsmax = float(self.gui.tab.xSMax.text())
            if xsmax > self.GL["XSMAX_HARD_LIMIT"]:
                XSMAX_SOFT_LIMIT = self.GL["XSMAX_HARD_LIMIT"]
                self.gui.tab.xSMax.setText(XSMAX_SOFT_LIMIT)
            else:
                XSMAX_SOFT_LIMIT = xsmax
            
            ysmin = float(self.gui.tab.ySMin.text())
            if ysmin < self.GL["YSMIN_HARD_LIMIT"]:
                YSMIN_SOFT_LIMIT = self.GL["YSMIN_HARD_LIMIT"]
                self.gui.tab.ySMin.setText(YSMIN_SOFT_LIMIT)
            else:
                YSMIN_SOFT_LIMIT = ysmin

            ysmax = float(self.gui.tab.ySMax.text())
            if ysmax > self.GL["YSMAX_HARD_LIMIT"]:
                YSMAX_SOFT_LIMIT = self.GL["YSMAX_HARD_LIMIT"]
                self.gui.tab.ySMax.setText(YSMAX_SOFT_LIMIT)
            else:
                YSMAX_SOFT_LIMIT = ysmax
            
            zsmin = float(self.gui.tab.zSMin.text())
            if zsmin < self.GL["ZSMIN_HARD_LIMIT"]:
                ZSMIN_SOFT_LIMIT = self.GL["ZSMIN_HARD_LIMIT"]
                self.gui.tab.zSMin.setText(ZSMIN_SOFT_LIMIT)
            else:
                ZSMIN_SOFT_LIMIT = zsmin

            zsmax = float(self.gui.tab.zSMax.text())
            if zsmax > self.GL["ZSMAX_HARD_LIMIT"]:
                ZSMAX_SOFT_LIMIT = self.GL["ZSMAX_HARD_LIMIT"]
                self.gui.tab.zSMax.setText(ZSMAX_SOFT_LIMIT)
            else:
                ZSMAX_SOFT_LIMIT = zsmax
            
            xomin = float(self.gui.tab.xOMin.text())
            if xomin < self.GL["XOMIN_HARD_LIMIT"]:
                XOMIN_SOFT_LIMIT = self.GL["XOMIN_HARD_LIMIT"]
                self.gui.tab.xOMin.setText(XOMIN_SOFT_LIMIT)
            else:
                XOMIN_SOFT_LIMIT = xomin

            xomax = float(self.gui.tab.xOMax.text())
            if xomax > self.GL["XOMAX_HARD_LIMIT"]:
                XOMAX_SOFT_LIMIT = self.GL["XOMAX_HARD_LIMIT"]
                self.gui.tab.xOMax.setText(XOMAX_SOFT_LIMIT)
            else:
                XOMAX_SOFT_LIMIT = xomax
            
            yomin = float(self.gui.tab.yOMin.text())
            if yomin < self.GL["YOMIN_HARD_LIMIT"]:
                YOMIN_SOFT_LIMIT = self.GL["YOMIN_HARD_LIMIT"]
                self.gui.tab.yOMin.setText(YOMIN_SOFT_LIMIT)
            else:
                YOMIN_SOFT_LIMIT = yomin

            yomax = float(self.gui.tab.yOMax.text())
            if yomax > self.GL["YOMAX_HARD_LIMIT"]:
                YOMAX_SOFT_LIMIT = self.GL["YOMAX_HARD_LIMIT"]
                self.gui.tab.yOMax.setText(YOMAX_SOFT_LIMIT)
            else:
                YOMAX_SOFT_LIMIT = yomax
            
            zomin = float(self.gui.tab.zOMin.text())
            if zomin < self.GL["ZOMIN_HARD_LIMIT"]:
                ZOMIN_SOFT_LIMIT = self.GL["ZOMIN_HARD_LIMIT"]
                self.gui.tab.zOMin.setText(ZOMIN_SOFT_LIMIT)
            else:
                ZOMIN_SOFT_LIMIT = zomin

            zomax = float(self.gui.tab.zOMax.text())
            if zomax > self.GL["ZOMAX_HARD_LIMIT"]:
                ZOMAX_SOFT_LIMIT = self.GL["ZOMAX_HARD_LIMIT"]
                self.gui.tab.zOMax.setText(ZOMAX_SOFT_LIMIT)
            else:
                ZOMAX_SOFT_LIMIT = zomax

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

    #def setRelPos(self, object: Literal["S", "O"], axis:
    #            Literal["X", "Y", "Z"]) -> None:################################################## May be redundant
    #    """Set the relative position.

    #    This method sets the relative position of the stage defined by 'object'
    #    and 'axis' to that displayed in the corresponding line edit widget.

    #    Parameters
    #    ----------
    #    object : {"S", "O"}
    #        Defines the stage as either sample or orbjective using "S" and "O",
    #        respectively.
    #    axis : {"X", "Y", "Z"}
    #        Defines the motor axis as x, y, or z using "X", "Y", "Z",
    #        respectively.

    #    Returns
    #    -------
    #    None
    #    """
    #    lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos,
    #                ("S", "Y"): self.gui.ySAbsPos, ("O", "Y"): self.gui.yOAbsPos,
    #                ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        # Set relative position global variable.
    #    self.GL[f"{axis}{object}_RELATIVE_POSITION"] = float(lineEdit[(object, axis)].text())

    #    pvName = self.GL[f"{axis}{object}ABSPOS"]
    #    movePos = self.GL[f"{axis}{object}_BASE_POSITION"] + self.GL[f"{axis}{object}_Relative_POSITION"]
    #    caput(pvName, movePos)
    
    #def checkLimits(self, object: Literal["S", "O"], axis:
    #            Literal["X", "Y", "Z"]) -> None:########################################### May be redundant
    #    """Check and set sample and objective limit labels.

    #    Parameters
    #    ----------
    #    object : {"S", "O"}
    #        Defines the stage as either sample or orbjective using "S" and "O",
    #        respectively.
    #    axis : {"X", "Y", "Z"}
    #        Defines the motor axis as x, y, or z using "X", "Y", "Z",
    #        respectively.

    #    Returns
    #    -------
    #    None
    #    """
    #    lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos,
    #                ("S", "Y"): self.gui.ySAbsPos, ("O", "Y"): self.gui.yOAbsPos,
    #                ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}
        
    #    limitLabels = {("S", "X", 0): self.gui.xSSn, ("S", "X", 1): self.gui.xSSp,
    #                   ("S", "X", 2): self.gui.xSHn, ("S", "X", 3): self.gui.xSHp,
    #                   ("S", "Y", 0): self.gui.ySSn, ("S", "Y", 1): self.gui.ySSp,
    #                   ("S", "Y", 2): self.gui.ySHn, ("S", "Y", 3): self.gui.ySHp,
    #                   ("S", "Z", 0): self.gui.zSSn, ("S", "Z", 1): self.gui.zSSp,
    #                   ("S", "Z", 2): self.gui.zSHn, ("S", "Z", 3): self.gui.zSHp,
    #                   ("O", "X", 0): self.gui.xSSn, ("O", "X", 1): self.gui.xSSp,
    #                   ("O", "X", 2): self.gui.xSHn, ("O", "X", 3): self.gui.xSHp,
    #                   ("O", "Y", 0): self.gui.ySSn, ("O", "Y", 1): self.gui.ySSp,
    #                   ("O", "Y", 2): self.gui.ySHn, ("O", "Y", 3): self.gui.ySHp,
    #                   ("O", "Z", 0): self.gui.zSSn, ("O", "Z", 1): self.gui.zSSp,
    #                   ("O", "Z", 2): self.gui.zSHn, ("O", "Z", 3): self.gui.zSHp}
        
    #    minSoftLim = self.GL[f"{axis}{object}MIN_SOFT_LIMIT"]
    #    maxSoftLim = self.GL[f"{axis}{object}MAX_SOFT_LIMIT"]
    #    minHardLim = self.GL[f"{axis}{object}MIN_HARD_LIMIT"]
    #    maxHardLim = self.GL[f"{axis}{object}MAX_HARD_LIMIT"]

    #    newPos = float(lineEdit[(object, axis)].text())

    #    if newPos < minSoftLim:
    #        limitLabels[(object, axis, 0)].setStyleSheet("background-color: green; border: 1px solid black;")
    #        limitLabels[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
    #    elif maxSoftLim < newPos:
    #        limitLabels[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
    #        limitLabels[(object, axis, 1)].setStyleSheet("background-color: green; border: 1px solid black;")
    #    else:
    #        limitLabels[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
    #        limitLabels[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

    #    if newPos < minHardLim:
    #        limitLabels[(object, axis, 3)].setStyleSheet("background-color: green; border: 1px solid black;")
    #        limitLabels[(object, axis, 4)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
    #    elif maxHardLim < newPos:
    #        limitLabels[(object, axis, 3)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
    #        limitLabels[(object, axis, 4)].setStyleSheet("background-color: green; border: 1px solid black;")
    #    else:
    #        limitLabels[(object, axis, 3)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
    #        limitLabels[(object, axis, 4)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

    def motorStatus(**kwargs):
        """
        """
        motionLabels = {("S", "X", 0): self.gui.xIdleS, ("S", "X", 1): self.gui.xStopS,
                        ("S", "Y", 0): self.gui.yIdleS, ("S", "Y", 1): self.gui.yStopS,
                        ("S", "Z", 0): self.gui.zIdleS, ("S", "Z", 1): self.gui.zStopS,
                        ("O", "X", 0): self.gui.xIdleO, ("O", "X", 1): self.gui.xStopO,
                        ("O", "Y", 0): self.gui.yIdleO, ("O", "Y", 1): self.gui.yStopO,
                        ("O", "Z", 0): self.gui.zIdleO, ("O", "Z", 1): self.gui.zStopO}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.GL.keys())
        vals = list(self.gui.GL.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        if value == 1:
            motionLabels[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
            motionLabels[(object, axis, 1)].setStyleSheet("background-color: green; border: 1px solid black;")
        elif value == 0:
            motionLabels[(object, axis, 0)].setStyleSheet("background-color: green; border: 1px solid black;")
            motionLabels[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")


