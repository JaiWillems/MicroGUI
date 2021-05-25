"""Create widgets interactive nature.

The controller module brings life to the GUI defined through the gui module by
connecting widgets up to control sequences that bring about change.
"""


# Import package dependencies.
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from epics import caput, caget

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
        self.connectSignals()

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
        self.updateAbsPos(object, axis, direction, step)
        self.setRelPos(object, axis)
        self.moveToPos(object, axis)
        self.checkLimits(object, axis)
    
    def absMove(self, object: Literal[0, 1], axis: Literal[0, 1, 2]) -> None:
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
        self.setRelPos(object, axis)
        self.moveToPos(object, axis)
        self.checkLimits(object, axis)
    
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
        GL = globals()

        if type == "CN":
            pvName = GL[f"{axis}{object}CN"]
            caput(pvName, -1000000)
        elif type == "CP":
            pvName = GL[f"{axis}{object}CP"]
            caput(pvName, 1000000)
        else:
            pvName = GL[f"{axis}{object}STOP"]
            caput(pvName, 1)
            self.setRelPos(object, axis)
            self.checkLimits(object, axis)

    def moveToPos(self, object: Literal["S", "O"], axis:
                  Literal["X", "Y", "Z"]) -> None:
        """Move stage to given position.

        This method moves the motor defined by 'object' and 'axis' to the
        position defined by the corresponding line edit.

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
        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}
        
        currentVal = float(lineEdit[(object, axis)])

        GL = globals()
        minSoftLim = GL[f"{axis}{object}MIN_SOFT_LIMIT"]
        maxSoftLim = GL[f"{axis}{object}MAX_SOFT_LIMIT"]
        minHardLim = GL[f"{axis}{object}MIN_HARD_LIMIT"]
        maxHardLim = GL[f"{axis}{object}MAX_HARD_LIMIT"]

        if currentVal < minSoftLim:
            lineEdit[(object, axis)].setText(minSoftLim)
        elif maxSoftLim < currentVal:
            lineEdit[(object, axis)].setText(maxSoftLim)
        elif currentVal < minHardLim:
            lineEdit[(object, axis)].setText(minHardLim)
        elif maxHardLim < currentVal:
            lineEdit[(object, axis)].setText(maxHardLim)
        
        pvName = GL[f"{axis}{object}MOVE"]
        caput(pvName, 1)
        caput(pvName, 0)

    def updateAbsPos(self, object: Literal[0, 1], axis: Literal[0, 1, 2],
                     direction: Literal[0, 1], step: QLineEdit) -> None:
        """Increment absolute position line edit.

        Increment the absolute position line edit widget defined by 'object'
        and 'axis' in the direction defined by 'direction' by the amount
        'step'.

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

        Notes
        -----
        Called when the method incPos is called to ensure displays are
        accurate.
        """        
        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}

        # Define line edit values.
        currentVal = float(lineEdit[(object, axis)].text())
        stepVal = float(step.text())

        # Update appropriate line edit value.
        if direction:
            lineEdit[(object, axis)].setText(str(currentVal + stepVal))
        else:
            lineEdit[(object, axis)].setText(str(currentVal - stepVal))

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
        GL = globals()
        if buttonID:
            # Set soft limits to hard limits.
            XSMIN_SOFT_LIMIT = GL["XSMIN_HARD_LIMIT"]
            XSMAX_SOFT_LIMIT = GL["XSMAX_HARD_LIMIT"]
            YSMIN_SOFT_LIMIT = GL["YSMIN_HARD_LIMIT"]
            YSMAX_SOFT_LIMIT = GL["YSMAX_HARD_LIMIT"]
            ZSMIN_SOFT_LIMIT = GL["ZSMIN_HARD_LIMIT"]
            ZSMAX_SOFT_LIMIT = GL["ZSMAX_HARD_LIMIT"]
            XOMIN_SOFT_LIMIT = GL["XOMIN_HARD_LIMIT"]
            XOMAX_SOFT_LIMIT = GL["XOMAX_HARD_LIMIT"]
            YOMIN_SOFT_LIMIT = GL["YOMIN_HARD_LIMIT"]
            YOMAX_SOFT_LIMIT = GL["YOMAX_HARD_LIMIT"]
            ZOMIN_SOFT_LIMIT = GL["ZOMIN_HARD_LIMIT"]
            ZOMAX_SOFT_LIMIT = GL["ZOMAX_HARD_LIMIT"]

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
            if xsmin < GL["XSMIN_HARD_LIMIT"]:
                XSMIN_SOFT_LIMIT = GL["XSMIN_HARD_LIMIT"]
                self.gui.tab.xSMin.setText(XSMIN_SOFT_LIMIT)
            else:
                XSMIN_SOFT_LIMIT = xsmin

            xsmax = float(self.gui.tab.xSMax.text())
            if xsmax > GL["XSMAX_HARD_LIMIT"]:
                XSMAX_SOFT_LIMIT = GL["XSMAX_HARD_LIMIT"]
                self.gui.tab.xSMax.setText(XSMAX_SOFT_LIMIT)
            else:
                XSMAX_SOFT_LIMIT = xsmax
            
            ysmin = float(self.gui.tab.ySMin.text())
            if ysmin < GL["YSMIN_HARD_LIMIT"]:
                YSMIN_SOFT_LIMIT = GL["YSMIN_HARD_LIMIT"]
                self.gui.tab.ySMin.setText(YSMIN_SOFT_LIMIT)
            else:
                YSMIN_SOFT_LIMIT = ysmin

            ysmax = float(self.gui.tab.ySMax.text())
            if ysmax > GL["YSMAX_HARD_LIMIT"]:
                YSMAX_SOFT_LIMIT = GL["YSMAX_HARD_LIMIT"]
                self.gui.tab.ySMax.setText(YSMAX_SOFT_LIMIT)
            else:
                YSMAX_SOFT_LIMIT = ysmax
            
            zsmin = float(self.gui.tab.zSMin.text())
            if zsmin < GL["ZSMIN_HARD_LIMIT"]:
                ZSMIN_SOFT_LIMIT = GL["ZSMIN_HARD_LIMIT"]
                self.gui.tab.zSMin.setText(ZSMIN_SOFT_LIMIT)
            else:
                ZSMIN_SOFT_LIMIT = zsmin

            zsmax = float(self.gui.tab.zSMax.text())
            if zsmax > GL["ZSMAX_HARD_LIMIT"]:
                ZSMAX_SOFT_LIMIT = GL["ZSMAX_HARD_LIMIT"]
                self.gui.tab.zSMax.setText(ZSMAX_SOFT_LIMIT)
            else:
                ZSMAX_SOFT_LIMIT = zsmax
            
            xomin = float(self.gui.tab.xOMin.text())
            if xomin < GL["XOMIN_HARD_LIMIT"]:
                XOMIN_SOFT_LIMIT = GL["XOMIN_HARD_LIMIT"]
                self.gui.tab.xOMin.setText(XOMIN_SOFT_LIMIT)
            else:
                XOMIN_SOFT_LIMIT = xomin

            xomax = float(self.gui.tab.xOMax.text())
            if xomax > GL["XOMAX_HARD_LIMIT"]:
                XOMAX_SOFT_LIMIT = GL["XOMAX_HARD_LIMIT"]
                self.gui.tab.xOMax.setText(XOMAX_SOFT_LIMIT)
            else:
                XOMAX_SOFT_LIMIT = xomax
            
            yomin = float(self.gui.tab.yOMin.text())
            if yomin < GL["YOMIN_HARD_LIMIT"]:
                YOMIN_SOFT_LIMIT = GL["YOMIN_HARD_LIMIT"]
                self.gui.tab.yOMin.setText(YOMIN_SOFT_LIMIT)
            else:
                YOMIN_SOFT_LIMIT = yomin

            yomax = float(self.gui.tab.yOMax.text())
            if yomax > GL["YOMAX_HARD_LIMIT"]:
                YOMAX_SOFT_LIMIT = GL["YOMAX_HARD_LIMIT"]
                self.gui.tab.yOMax.setText(YOMAX_SOFT_LIMIT)
            else:
                YOMAX_SOFT_LIMIT = yomax
            
            zomin = float(self.gui.tab.zOMin.text())
            if zomin < GL["ZOMIN_HARD_LIMIT"]:
                ZOMIN_SOFT_LIMIT = GL["ZOMIN_HARD_LIMIT"]
                self.gui.tab.zOMin.setText(ZOMIN_SOFT_LIMIT)
            else:
                ZOMIN_SOFT_LIMIT = zomin

            zomax = float(self.gui.tab.zOMax.text())
            if zomax > GL["ZOMAX_HARD_LIMIT"]:
                ZOMAX_SOFT_LIMIT = GL["ZOMAX_HARD_LIMIT"]
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
        GL = globals()

        # Set global backlash variables.
        GL["XS_BACKLASH"] = float(self.gui.tab.xSB.text())
        GL["YS_BACKLASH"] = float(self.gui.tab.ySB.text())
        GL["ZS_BACKLASH"] = float(self.gui.tab.zSB.text())
        GL["XO_BACKLASH"] = float(self.gui.tab.xOB.text())
        GL["YO_BACKLASH"] = float(self.gui.tab.yOB.text())
        GL["ZO_BACKLASH"] = float(self.gui.tab.zOB.text())

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
        GL = globals()

        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}

        # Get global indices.
        basePosStr = f"{axis}{object}_BASE_POSITION"
        relPosStr = f"{axis}{object}_RELATIVE_POSITION"

        # Update the base and relative positions.
        GL[basePosStr] += GL[relPosStr]
        GL[relPosStr] = 0

        # Update absolute position line edit widget to 0.
        lineEdit[(object, axis)].setText("0")

    def setRelPos(self, object: Literal["S", "O"], axis:
                Literal["X", "Y", "Z"]) -> None:
        """Set the relative position.

        This method sets the relative position of the stage defined by 'object'
        and 'axis' to that displayed in the corresponding line edit widget.

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
        GL = globals()

        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}

        # Set relative position global variable.
        GL[f"{axis}{object}_RELATIVE_POSITION"] = float(lineEdit[(object, axis)].text())

        pvName = GL[f"{axis}{object}ABSPOS"]
        movePos = GL[f"{axis}{object}_BASE_POSITION"] + GL[f"{axis}{object}_Relative_POSITION"]
        caput(pvName, movePos)
    
    def checkLimits(self, object: Literal["S", "O"], axis:
                Literal["X", "Y", "Z"]) -> None:
        """Check and set sample and objective limit labels.

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
        GL = globals()

        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}
        
        limitLabels = {(0, 0, 0): self.gui.xSSn, (0, 0, 1): self.gui.xSSp,
                       (0, 0, 2): self.gui.xSHn, (0, 0, 3): self.gui.xSHp,
                       (0, 1, 0): self.gui.ySSn, (0, 1, 1): self.gui.ySSp,
                       (0, 1, 2): self.gui.ySHn, (0, 1, 3): self.gui.ySHp,
                       (0, 2, 0): self.gui.zSSn, (0, 2, 1): self.gui.zSSp,
                       (0, 2, 2): self.gui.zSHn, (0, 2, 3): self.gui.zSHp,
                       (1, 0, 0): self.gui.xSSn, (1, 0, 1): self.gui.xSSp,
                       (1, 0, 2): self.gui.xSHn, (1, 0, 3): self.gui.xSHp,
                       (1, 1, 0): self.gui.ySSn, (1, 1, 1): self.gui.ySSp,
                       (1, 1, 2): self.gui.ySHn, (1, 1, 3): self.gui.ySHp,
                       (1, 2, 0): self.gui.zSSn, (1, 2, 1): self.gui.zSSp,
                       (1, 2, 2): self.gui.zSHn, (1, 2, 3): self.gui.zSHp}
        
        minSoftLim = GL[f"{axis}{object}MIN_SOFT_LIMIT"]
        maxSoftLim = GL[f"{axis}{object}MAX_SOFT_LIMIT"]
        minHardLim = GL[f"{axis}{object}MIN_HARD_LIMIT"]
        maxHardLim = GL[f"{axis}{object}MAX_HARD_LIMIT"]

        newPos = float(lineEdit[(object, axis)].text())

        if newPos < minSoftLim:
            limitLabels[(object, axis, 0)].setStyleSheet("background-color: green; border: 1px solid black;")
            limitLabels[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        elif maxSoftLim < newPos:
            limitLabels[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
            limitLabels[(object, axis, 1)].setStyleSheet("background-color: green; border: 1px solid black;")
        else:
            limitLabels[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
            limitLabels[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        if newPos < minHardLim:
            limitLabels[(object, axis, 3)].setStyleSheet("background-color: green; border: 1px solid black;")
            limitLabels[(object, axis, 4)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        elif maxHardLim < newPos:
            limitLabels[(object, axis, 3)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
            limitLabels[(object, axis, 4)].setStyleSheet("background-color: green; border: 1px solid black;")
        else:
            limitLabels[(object, axis, 3)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
            limitLabels[(object, axis, 4)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

    def checkMotorMotion(self, object: Literal["S", "O"], axis:
                Literal["X", "Y", "Z"]) -> None:
        """Check motor motion.
        
        This method monitors the motion of the active motor and sets the sample
        and objective motor status labels.

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
        GL = globals()

        motionLabels = {(0, 0, 0): self.gui.xIdleS, (0, 0, 1): self.gui.xStopS,
                        (0, 1, 0): self.gui.yIdleS, (0, 1, 1): self.gui.yStopS,
                        (0, 2, 0): self.gui.zIdleS, (0, 2, 1): self.gui.zStopS,
                        (1, 0, 0): self.gui.xIdleO, (1, 0, 1): self.gui.xStopO,
                        (1, 1, 0): self.gui.yIdleO, (1, 1, 1): self.gui.yStopO,
                        (1, 2, 0): self.gui.zIdleO, (1, 2, 1): self.gui.zStopO}
        
        motionLabels[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
        motionLabels[(object, axis, 1)].setStyleSheet("background-color: green; border: 1px solid black;")

        pvName = GL[f"{object}{axis}STATE"]
        state = caget(pvName)
        while state == 0:#########################################################Assumed that 0 indicated motion
            state = caget(pvName)

        motionLabels[(object, axis, 0)].setStyleSheet("background-color: green; border: 1px solid black;")
        motionLabels[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

