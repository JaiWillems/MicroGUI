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
        GL = globals()

        # Set step line edits to current PV values.
        self.gui.xSStep.setText(str(caget(GL["XSSTEP"])))
        self.gui.ySStep.setText(str(caget(GL["YSSTEP"])))
        self.gui.zSStep.setText(str(caget(GL["ZSSTEP"])))
        self.gui.xOStep.setText(str(caget(GL["XOSTEP"])))
        self.gui.yOStep.setText(str(caget(GL["YOSTEP"])))
        self.gui.zOStep.setText(str(caget(GL["ZOSTEP"])))

        # Set absolute position line edits to current PV values.
        self.gui.xSAbsPos.setText(str(caget(GL["XSABSPOS"])))
        self.gui.ySAbsPos.setText(str(caget(GL["YSABSPOS"])))
        self.gui.zSAbsPos.setText(str(caget(GL["ZSABSPOS"])))
        self.gui.xOAbsPos.setText(str(caget(GL["XOABSPOS"])))
        self.gui.yOAbsPos.setText(str(caget(GL["YOABSPOS"])))
        self.gui.zOAbsPos.setText(str(caget(GL["ZOABSPOS"])))

        # Set backlash line edits to current PV values.
        self.gui.tab.xSB.setText(str(caget(GL["XSB"])))
        self.gui.tab.ySB.setText(str(caget(GL["YSB"])))
        self.gui.tab.zSB.setText(str(caget(GL["ZSB"])))
        self.gui.tab.xOB.setText(str(caget(GL["XOB"])))
        self.gui.tab.yOB.setText(str(caget(GL["YOB"])))
        self.gui.tab.zOB.setText(str(caget(GL["ZOB"])))

        # Set relative position global variables to current motor position.
        GL["XS_RELATIVE_POSITION"] = caget(GL["XSABSPOS"])
        GL["YS_RELATIVE_POSITION"] = caget(GL["YSABSPOS"])
        GL["ZS_RELATIVE_POSITION"] = caget(GL["ZSABSPOS"])
        GL["XO_RELATIVE_POSITION"] = caget(GL["XOABSPOS"])
        GL["YO_RELATIVE_POSITION"] = caget(GL["YOABSPOS"])
        GL["ZO_RELATIVE_POSITION"] = caget(GL["ZOABSPOS"])

        self.PV_XSABSPOS = PV(
            pvname=GL["XSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_ySABSPOS = PV(
            pvname=GL["YSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zSABSPOS = PV(
            pvname=GL["ZSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_XOABSPOS = PV(
            pvname=GL["XOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_yOABSPOS = PV(
            pvname=GL["YOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zOABSPOS = PV(
            pvname=GL["ZOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)

        self.PV_XSSTATE = PV(
            pvname=GL["XSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YSSTATE = PV(
            pvname=GL["YSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZSSTATE = PV(
            pvname=GL["ZSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_XOSTATE = PV(
            pvname=GL["XOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YOSTATE = PV(
            pvname=GL["YOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZOSTATE = PV(
            pvname=GL["ZOSTATE"], auto_monitor=True, callback=self.motorStatus)

        self.PV_XSHN = PV(
            pvname=GL["XSHN"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_XSHP = PV(
            pvname=GL["XSHP"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_YSHN = PV(
            pvname=GL["YSHN"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_YSHP = PV(
            pvname=GL["YSHP"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_ZSHN = PV(
            pvname=GL["ZSHN"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_ZSHP = PV(
            pvname=GL["ZSHP"], auto_monitor=True, callback=self.setHardLimitInd)

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
        self.gui.tab.RDM1.pressed.connect(
            partial(self.modeState, 1, self.modeMotor))
        self.gui.tab.RDM2.pressed.connect(
            partial(self.modeState, 2, self.modeMotor))
        self.gui.tab.RDM3.pressed.connect(
            partial(self.modeState, 3, self.modeMotor))
        self.gui.tab.RDM4.pressed.connect(
            partial(self.modeState, 4, self.modeMotor))

        # Increment sample and objective stage functionality.
        self.gui.xSN.clicked.connect(
            partial(self.incPos, "S", "X", "N", self.gui.xSStep))
        self.gui.xSP.clicked.connect(
            partial(self.incPos, "S", "X", "P", self.gui.xSStep))
        self.gui.ySN.clicked.connect(
            partial(self.incPos, "S", "Y", "N", self.gui.ySStep))
        self.gui.ySP.clicked.connect(
            partial(self.incPos, "S", "Y", "P", self.gui.ySStep))
        self.gui.zSN.clicked.connect(
            partial(self.incPos, "S", "Z", "N", self.gui.zSStep))
        self.gui.zSP.clicked.connect(
            partial(self.incPos, "S", "Z", "P", self.gui.zSStep))
        self.gui.xON.clicked.connect(
            partial(self.incPos, "O", "X", "N", self.gui.xOStep))
        self.gui.xOP.clicked.connect(
            partial(self.incPos, "O", "X", "P", self.gui.xOStep))
        self.gui.yON.clicked.connect(
            partial(self.incPos, "O", "Y", "N", self.gui.yOStep))
        self.gui.yOP.clicked.connect(
            partial(self.incPos, "O", "Y", "P", self.gui.yOStep))
        self.gui.zON.clicked.connect(
            partial(self.incPos, "O", "Z", "N", self.gui.zOStep))
        self.gui.zOP.clicked.connect(
            partial(self.incPos, "O", "Z", "P", self.gui.zOStep))

        # Move sample and objective stage to absolute position functionality.
        self.gui.xSMove.clicked.connect(partial(self.absMove, "S", "X"))
        self.gui.ySMove.clicked.connect(partial(self.absMove, "S", "Y"))
        self.gui.zSMove.clicked.connect(partial(self.absMove, "S", "Z"))
        self.gui.xOMove.clicked.connect(partial(self.absMove, "O", "X"))
        self.gui.yOMove.clicked.connect(partial(self.absMove, "O", "Y"))
        self.gui.zOMove.clicked.connect(partial(self.absMove, "O", "Z"))

        # Continuous motion of the sample and objective stages functionality.
        self.gui.xSCn.clicked.connect(
            partial(self.continuousMotion, "S", "X", "CN"))
        self.gui.xSStop.clicked.connect(
            partial(self.continuousMotion, "S", "X", "STOP"))
        self.gui.xSCp.clicked.connect(
            partial(self.continuousMotion, "S", "X", "CP"))
        self.gui.ySCn.clicked.connect(
            partial(self.continuousMotion, "S", "Y", "CN"))
        self.gui.ySStop.clicked.connect(
            partial(self.continuousMotion, "S", "Y", "STOP"))
        self.gui.ySCp.clicked.connect(
            partial(self.continuousMotion, "S", "Y", "CP"))
        self.gui.zSCn.clicked.connect(
            partial(self.continuousMotion, "S", "Z", "CN"))
        self.gui.zSStop.clicked.connect(
            partial(self.continuousMotion, "S", "Z", "STOP"))
        self.gui.zSCp.clicked.connect(
            partial(self.continuousMotion, "S", "Z", "CP"))
        self.gui.xOCn.clicked.connect(
            partial(self.continuousMotion, "O", "X", "CN"))
        self.gui.xOStop.clicked.connect(
            partial(self.continuousMotion, "O", "X", "STOP"))
        self.gui.xOCp.clicked.connect(
            partial(self.continuousMotion, "O", "X", "CP"))
        self.gui.yOCn.clicked.connect(
            partial(self.continuousMotion, "O", "Y", "CN"))
        self.gui.yOStop.clicked.connect(
            partial(self.continuousMotion, "O", "Y", "STOP"))
        self.gui.yOCp.clicked.connect(
            partial(self.continuousMotion, "O", "Y", "CP"))
        self.gui.zOCn.clicked.connect(
            partial(self.continuousMotion, "O", "Z", "CN"))
        self.gui.zOStop.clicked.connect(
            partial(self.continuousMotion, "O", "Z", "STOP"))
        self.gui.zOCp.clicked.connect(
            partial(self.continuousMotion, "O", "Z", "CP"))

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

        self.gui.tab.globals.clicked.connect(self.displayGlobals)

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
        path, _ = QFileDialog.getSaveFileName(
            self.gui, "Save File", "sample_capture", "Image files (*.jpg *.jpeg *.gif *png)")

        plt.figure()
        plt.imshow(np.rot90(self.gui.image, 3))
        plt.axis("off")
        plt.savefig(path, dpi=250, bbox_inches="tight")

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

    def incPos(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"], direction: Literal["N", "P"], step: QLineEdit) -> None:
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
        GL = globals()

        caput(GL[f"{axis}{object}STEP"], float(step.text()))

        absPos = GL[f"{axis}{object}_BASE_POSITION"]
        relPos = GL[f"{axis}{object}_RELATIVE_POSITION"]
        incPos = caget(GL[f"{axis}{object}STEP"])

        PSL = GL[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = GL[f"{axis}{object}MIN_SOFT_LIMIT"]

        if direction == "P" and absPos + relPos + incPos >= PSL:
            GL[f"{axis}{object}_RELATIVE_POSITION"] = PSL - absPos

            caput(GL[f"{axis}{object}ABSPOS"], PSL)
            caput(GL[f"{axis}{object}MOVE"], 1)
            caput(GL[f"{axis}{object}MOVE"], 0)
        elif direction == "N" and absPos + relPos - incPos <= NSL:
            GL[f"{axis}{object}_RELATIVE_POSITION"] = NSL - absPos

            caput(GL[f"{axis}{object}ABSPOS"], NSL)
            caput(GL[f"{axis}{object}MOVE"], 1)
            caput(GL[f"{axis}{object}MOVE"], 0)
        else:
            if direction == "P":
                GL[f"{axis}{object}_RELATIVE_POSITION"] = relPos + incPos
            else:
                GL[f"{axis}{object}_RELATIVE_POSITION"] = relPos - incPos

            caput(GL[f"{axis}{object}{direction}"], 1)

        self.setSoftLimitInd(object, axis)

        absPos = caget(GL[f"{axis}{object}ABSPOS"])
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
        GL = globals()

        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos, ("S", "Y"): self.gui.ySAbsPos,
                    ("O", "Y"): self.gui.yOAbsPos, ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        absPos = float(lineEdit[(object, axis)].text())
        basePos = GL[f"{axis}{object}_BASE_POSITION"]

        PSL = GL[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = GL[f"{axis}{object}MIN_SOFT_LIMIT"]

        if basePos + absPos >= PSL:
            GL[f"{axis}{object}_RELATIVE_POSITION"] = PSL - basePos
            caput(GL[f"{axis}{object}ABSPOS"], PSL)
        elif basePos + absPos <= NSL:
            GL[f"{axis}{object}_RELATIVE_POSITION"] = NSL - basePos
            caput(GL[f"{axis}{object}ABSPOS"], NSL)
        else:
            GL[f"{axis}{object}_RELATIVE_POSITION"] = absPos
            caput(GL[f"{axis}{object}ABSPOS"], basePos + absPos)

        caput(GL[f"{axis}{object}MOVE"], 1)
        caput(GL[f"{axis}{object}MOVE"], 0)

        self.setSoftLimitInd(object, axis)

        absPos = caget(GL[f"{axis}{object}ABSPOS"])
        print(f"Absolute movement to {axis}{object}ABSPOS = {absPos}.")

    def continuousMotion(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"], type: Literal["CN", "STOP", "CP"]) -> None:
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
            caput(GL[f"{axis}{object}CN"], GL[f"{axis}{object}MIN_SOFT_LIMIT"])
        elif type == "CP":
            caput(GL[f"{axis}{object}CP"], GL[f"{axis}{object}MAX_SOFT_LIMIT"])
        else:
            caput(GL[f"{axis}{object}CN"], 0)
            caput(GL[f"{axis}{object}CP"], 0)
            caput(GL[f"{axis}{object}STOP"], 1)
            caput(GL[f"{axis}{object}STOP"], 0)

        self.setSoftLimitInd(object, axis)

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
        GL = globals()
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos, ("S", "Y"): self.gui.ySAbsPos,
                    ("O", "Y"): self.gui.yOAbsPos, ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(GL.keys())
        vals = list(GL.values())
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
        GL = globals()

        if buttonID:
            # Set soft limits to hard limits.
            GL["XSMIN_SOFT_LIMIT"] = GL["XSMIN_HARD_LIMIT"]
            GL["XSMAX_SOFT_LIMIT"] = GL["XSMAX_HARD_LIMIT"]
            GL["YSMIN_SOFT_LIMIT"] = GL["YSMIN_HARD_LIMIT"]
            GL["YSMAX_SOFT_LIMIT"] = GL["YSMAX_HARD_LIMIT"]
            GL["ZSMIN_SOFT_LIMIT"] = GL["ZSMIN_HARD_LIMIT"]
            GL["ZSMAX_SOFT_LIMIT"] = GL["ZSMAX_HARD_LIMIT"]
            GL["XOMIN_SOFT_LIMIT"] = GL["XOMIN_HARD_LIMIT"]
            GL["XOMAX_SOFT_LIMIT"] = GL["XOMAX_HARD_LIMIT"]
            GL["YOMIN_SOFT_LIMIT"] = GL["YOMIN_HARD_LIMIT"]
            GL["YOMAX_SOFT_LIMIT"] = GL["YOMAX_HARD_LIMIT"]
            GL["ZOMIN_SOFT_LIMIT"] = GL["ZOMIN_HARD_LIMIT"]
            GL["ZOMAX_SOFT_LIMIT"] = GL["ZOMAX_HARD_LIMIT"]

            # Update soft limit line edits.
            self.gui.tab.xSMin.setText(str(GL["XSMIN_SOFT_LIMIT"]))
            self.gui.tab.xSMax.setText(str(GL["XSMAX_SOFT_LIMIT"]))
            self.gui.tab.ySMin.setText(str(GL["YSMIN_SOFT_LIMIT"]))
            self.gui.tab.ySMax.setText(str(GL["YSMAX_SOFT_LIMIT"]))
            self.gui.tab.zSMin.setText(str(GL["ZSMIN_SOFT_LIMIT"]))
            self.gui.tab.zSMax.setText(str(GL["ZSMAX_SOFT_LIMIT"]))
            self.gui.tab.xOMin.setText(str(GL["XOMIN_SOFT_LIMIT"]))
            self.gui.tab.xOMax.setText(str(GL["XOMAX_SOFT_LIMIT"]))
            self.gui.tab.yOMin.setText(str(GL["YOMIN_SOFT_LIMIT"]))
            self.gui.tab.yOMax.setText(str(GL["YOMAX_SOFT_LIMIT"]))
            self.gui.tab.zOMin.setText(str(GL["ZOMIN_SOFT_LIMIT"]))
            self.gui.tab.zOMax.setText(str(GL["ZOMAX_SOFT_LIMIT"]))

        else:
            # Set soft limits to inputted values
            xsmin = float(self.gui.tab.xSMin.text())
            if xsmin < GL["XSMIN_HARD_LIMIT"]:
                GL["XSMIN_SOFT_LIMIT"] = GL["XSMIN_HARD_LIMIT"]
                self.gui.tab.xSMin.setText(str(GL["XSMIN_SOFT_LIMIT"]))
            else:
                GL["XSMIN_SOFT_LIMIT"] = xsmin
                self.gui.tab.xSMin.setText(str(xsmin))

            xsmax = float(self.gui.tab.xSMax.text())
            if xsmax > GL["XSMAX_HARD_LIMIT"]:
                GL["XSMAX_SOFT_LIMIT"] = GL["XSMAX_HARD_LIMIT"]
                self.gui.tab.xSMax.setText(str(GL["XSMAX_SOFT_LIMIT"]))
            else:
                GL["XSMAX_SOFT_LIMIT"] = xsmax
                self.gui.tab.xSMax.setText(str(xsmax))

            ysmin = float(self.gui.tab.ySMin.text())
            if ysmin < GL["YSMIN_HARD_LIMIT"]:
                GL["YSMIN_SOFT_LIMIT"] = GL["YSMIN_HARD_LIMIT"]
                self.gui.tab.ySMin.setText(str(GL["YSMIN_SOFT_LIMIT"]))
            else:
                GL["YSMIN_SOFT_LIMIT"] = ysmin
                self.gui.tab.ySMin.setText(str(ysmin))

            ysmax = float(self.gui.tab.ySMax.text())
            if ysmax > GL["YSMAX_HARD_LIMIT"]:
                GL["YSMAX_SOFT_LIMIT"] = GL["YSMAX_HARD_LIMIT"]
                self.gui.tab.ySMax.setText(str(GL["YSMAX_SOFT_LIMIT"]))
            else:
                GL["YSMAX_SOFT_LIMIT"] = ysmax
                self.gui.tab.ySMax.setText(str(ysmax))

            zsmin = float(self.gui.tab.zSMin.text())
            if zsmin < GL["ZSMIN_HARD_LIMIT"]:
                GL["ZSMIN_SOFT_LIMIT"] = GL["ZSMIN_HARD_LIMIT"]
                self.gui.tab.zSMin.setText(str(GL["ZSMIN_SOFT_LIMIT"]))
            else:
                GL["ZSMIN_SOFT_LIMIT"] = zsmin
                self.gui.tab.zSMin.setText(str(zsmin))

            zsmax = float(self.gui.tab.zSMax.text())
            if zsmax > GL["ZSMAX_HARD_LIMIT"]:
                GL["ZSMAX_SOFT_LIMIT"] = GL["ZSMAX_HARD_LIMIT"]
                self.gui.tab.zSMax.setText(str(GL["ZSMAX_SOFT_LIMIT"]))
            else:
                GL["ZSMAX_SOFT_LIMIT"] = zsmax
                self.gui.tab.zSMax.setText(str(zsmax))

            xomin = float(self.gui.tab.xOMin.text())
            if xomin < GL["XOMIN_HARD_LIMIT"]:
                GL["XOMIN_SOFT_LIMIT"] = GL["XOMIN_HARD_LIMIT"]
                self.gui.tab.xOMin.setText(str(GL["XOMIN_SOFT_LIMIT"]))
            else:
                GL["XOMIN_SOFT_LIMIT"] = xomin
                self.gui.tab.xOMin.setText(str(xomin))

            xomax = float(self.gui.tab.xOMax.text())
            if xomax > GL["XOMAX_HARD_LIMIT"]:
                GL["XOMAX_SOFT_LIMIT"] = GL["XOMAX_HARD_LIMIT"]
                self.gui.tab.xOMax.setText(str(GL["XOMAX_SOFT_LIMIT"]))
            else:
                GL["XOMAX_SOFT_LIMIT"] = xomax
                self.gui.tab.xOMax.setText(str(xomax))

            yomin = float(self.gui.tab.yOMin.text())
            if yomin < GL["YOMIN_HARD_LIMIT"]:
                GL["YOMIN_SOFT_LIMIT"] = GL["YOMIN_HARD_LIMIT"]
                self.gui.tab.yOMin.setText(str(GL["YOMIN_SOFT_LIMIT"]))
            else:
                GL["YOMIN_SOFT_LIMIT"] = yomin
                self.gui.tab.yOMin.setText(str(yomin))

            yomax = float(self.gui.tab.yOMax.text())
            if yomax > GL["YOMAX_HARD_LIMIT"]:
                GL["YOMAX_SOFT_LIMIT"] = GL["YOMAX_HARD_LIMIT"]
                self.gui.tab.yOMax.setText(str(GL["YOMAX_SOFT_LIMIT"]))
            else:
                GL["YOMAX_SOFT_LIMIT"] = yomax
                self.gui.tab.yOMax.setText(str(yomax))

            zomin = float(self.gui.tab.zOMin.text())
            if zomin < GL["ZOMIN_HARD_LIMIT"]:
                GL["ZOMIN_SOFT_LIMIT"] = GL["ZOMIN_HARD_LIMIT"]
                self.gui.tab.zOMin.setText(str(GL["ZOMIN_SOFT_LIMIT"]))
            else:
                GL["ZOMIN_SOFT_LIMIT"] = zomin
                self.gui.tab.zOMin.setText(str(zomin))

            zomax = float(self.gui.tab.zOMax.text())
            if zomax > GL["ZOMAX_HARD_LIMIT"]:
                GL["ZOMAX_SOFT_LIMIT"] = GL["ZOMAX_HARD_LIMIT"]
                self.gui.tab.zOMax.setText(str(GL["ZOMAX_SOFT_LIMIT"]))
            else:
                GL["ZOMAX_SOFT_LIMIT"] = zomax
                self.gui.tab.zOMax.setText(str(zomax))

        print(f"Updating soft limits, buttonID={buttonID}.")
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                Min = GL[f"{axis}{object}MIN_SOFT_LIMIT"]
                Max = GL[f"{axis}{object}MAX_SOFT_LIMIT"]
                print(f"XS SL: min -> {Min}, max -> {Max}")

        self.checkMotorPos(object, axis)

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
        caput(GL["XSB"], abs(int(self.gui.tab.xSB.text())))
        caput(GL["YSB"], abs(int(self.gui.tab.ySB.text())))
        caput(GL["ZSB"], abs(int(self.gui.tab.zSB.text())))
        caput(GL["XOB"], abs(int(self.gui.tab.xOB.text())))
        caput(GL["YOB"], abs(int(self.gui.tab.yOB.text())))
        caput(GL["ZOB"], abs(int(self.gui.tab.zOB.text())))

        self.gui.tab.xSB.setText(str(caget(GL["XSB"])))
        self.gui.tab.ySB.setText(str(caget(GL["YSB"])))
        self.gui.tab.zSB.setText(str(caget(GL["ZSB"])))
        self.gui.tab.xOB.setText(str(caget(GL["XOB"])))
        self.gui.tab.yOB.setText(str(caget(GL["YOB"])))
        self.gui.tab.zOB.setText(str(caget(GL["ZOB"])))

        print("Updating backlash values.")

    def zeroPos(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"]) -> None:
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

        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos, ("S", "Y"): self.gui.ySAbsPos,
                    ("O", "Y"): self.gui.yOAbsPos, ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        # Update the base and relative positions.
        GL[f"{axis}{object}_BASE_POSITION"] += GL[f"{axis}{object}_RELATIVE_POSITION"]
        GL[f"{axis}{object}_RELATIVE_POSITION"] = 0

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
        GL = globals()
        motionLabels = {("S", "X", 0): self.gui.tab.xIdleS, ("S", "X", 1): self.gui.tab.xStopS,
                        ("S", "Y", 0): self.gui.tab.yIdleS, ("S", "Y", 1): self.gui.tab.yStopS,
                        ("S", "Z", 0): self.gui.tab.zIdleS, ("S", "Z", 1): self.gui.tab.zStopS,
                        ("O", "X", 0): self.gui.tab.xIdleO, ("O", "X", 1): self.gui.tab.xStopO,
                        ("O", "Y", 0): self.gui.tab.yIdleO, ("O", "Y", 1): self.gui.tab.yStopO,
                        ("O", "Z", 0): self.gui.tab.zIdleO, ("O", "Z", 1): self.gui.tab.zStopO}

        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos, ("S", "Y"): self.gui.ySAbsPos,
                    ("O", "Y"): self.gui.yOAbsPos, ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(GL.keys())
        vals = list(GL.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        if value == 0:
            motionLabels[(object, axis, 0)].setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
            motionLabels[(object, axis, 1)].setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")
        elif value == 0:
            motionLabels[(object, axis, 0)].setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")
            motionLabels[(object, axis, 1)].setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")

        GL[f"{axis}{object}_RELATIVE_POSITION"] = caget(
            GL[f"{axis}{object}ABSPOS"])
        lineEdit[(object, axis)].setText(
            GL[f"{axis}{object}_RELATIVE_POSITION"])

        print(
            f"Checkiing motor status, motor ident and state => {pvname}, {value}")
        relPos = GL[f"{axis}{object}_RELATIVE_POSITION"]
        print(f"Current relative position -> {relPos}")

    def checkMotorPos(self, object, axis):
        """
        """
        GL = globals()
        PSL = GL[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = GL[f"{axis}{object}MIN_SOFT_LIMIT"]

        basePos = GL[f"{axis}{object}_BASE_POSITION"]
        relPos = GL[f"{axis}{object}_RELATIVE_POSITION"]

        if basePos + relPos > PSL:
            GL[f"{axis}{object}_RELATIVE_POSITION"] = PSL - basePos
            caput(GL[f"{axis}{object}ABSPOS"], PSL)
        elif basePos + relPos < NSL:
            GL[f"{axis}{object}_RELATIVE_POSITION"] = NSL - basePos
            caput(GL[f"{axis}{object}ABSPOS"], NSL)

        caput(GL[f"{axis}{object}MOVE"], 1)
        caput(GL[f"{axis}{object}MOVE"], 0)

    def setHardLimitInd(self, **kwargs):
        """
        """
        GL = globals()

        hardLimits = {("S", "X", 0): self.gui.xSHn, ("S", "X", 1): self.gui.xSHp,
                      ("S", "Y", 0): self.gui.ySHn, ("S", "Y", 1): self.gui.ySHp,
                      ("S", "Z", 0): self.gui.zSHn, ("S", "Z", 1): self.gui.zSHp,
                      ("O", "X", 0): self.gui.xOHn, ("O", "X", 1): self.gui.xOHp,
                      ("O", "Y", 0): self.gui.yOHn, ("O", "Y", 1): self.gui.yOHp,
                      ("O", "Z", 0): self.gui.zOHn, ("O", "Z", 1): self.gui.zOHp}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(GL.keys())
        vals = list(GL.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        # Set maximum hard limit indicator.
        if GL[f"{axis}{object}MAX_HARD_LIMIT"] <= value:
            hardLimits[(object, axis, 1)].setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        else:
            hardLimits[(object, axis, 1)].setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")

        # Set minimum hard limit indicator.
        if value <= GL[f"{axis}{object}MIN_HARD_LIMIT"]:
            hardLimits[(object, axis, 0)].setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        else:
            hardLimits[(object, axis, 0)].setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")

        print("Setting hard limit indicators.")

    def setSoftLimitInd(self, object, axis):
        """
        set soft limits if scheduled to move to soft limits
        """
        GL = globals()

        softLimits = {("S", "X", 0): self.gui.xSSn, ("S", "X", 1): self.gui.xSSp,
                      ("S", "Y", 0): self.gui.ySSn, ("S", "Y", 1): self.gui.ySSp,
                      ("S", "Z", 0): self.gui.zSSn, ("S", "Z", 1): self.gui.zSSp,
                      ("O", "X", 0): self.gui.xOSn, ("O", "X", 1): self.gui.xOSp,
                      ("O", "Y", 0): self.gui.yOSn, ("O", "Y", 1): self.gui.yOSp,
                      ("O", "Z", 0): self.gui.zOSn, ("O", "Z", 1): self.gui.zOSp}

        value = caget(GL[f"{axis}{object}ABSPOS"])

        # Set maximum soft limit indicator.
        if GL[f"{axis}{object}MAX_SOFT_LIMIT"] <= value:
            softLimits[(object, axis, 1)].setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        else:
            softLimits[(object, axis, 1)].setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")

        # Set minimum soft limit indicator.
        if value <= GL[f"{axis}{object}MIN_SOFT_LIMIT"]:
            softLimits[(object, axis, 0)].setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        else:
            softLimits[(object, axis, 0)].setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")

        print("Setting soft limit indicators.")

    def displayGlobals(self):
        """     
        """
        print("-*- GLOBAL VARIABLES - START -*-")

        GL = globals()
        keys = list(GL.keys())
        for key in keys:
            print(f"{key} -> {GL[key]}")

        print("-*- GLOBAL VARIABLES - END -*-")
