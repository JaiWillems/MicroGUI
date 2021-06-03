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

        # Set step line edits to current PV values.
        self.gui.xSStep.setText(str(caget(self.gui.macros["XSSTEP"])))
        self.gui.ySStep.setText(str(caget(self.gui.macros["YSSTEP"])))
        self.gui.zSStep.setText(str(caget(self.gui.macros["ZSSTEP"])))
        self.gui.xOStep.setText(str(caget(self.gui.macros["XOSTEP"])))
        self.gui.yOStep.setText(str(caget(self.gui.macros["YOSTEP"])))
        self.gui.zOStep.setText(str(caget(self.gui.macros["ZOSTEP"])))

        # Set absolute position line edits to current PV values.
        self.gui.xSAbsPos.setText(str(caget(self.gui.macros["XSABSPOS"])))
        self.gui.ySAbsPos.setText(str(caget(self.gui.macros["YSABSPOS"])))
        self.gui.zSAbsPos.setText(str(caget(self.gui.macros["ZSABSPOS"])))
        self.gui.xOAbsPos.setText(str(caget(self.gui.macros["XOABSPOS"])))
        self.gui.yOAbsPos.setText(str(caget(self.gui.macros["YOABSPOS"])))
        self.gui.zOAbsPos.setText(str(caget(self.gui.macros["ZOABSPOS"])))

        # Set backlash line edits to current PV values.
        self.gui.tab.xSB.setText(str(caget(self.gui.macros["XSB"])))
        self.gui.tab.ySB.setText(str(caget(self.gui.macros["YSB"])))
        self.gui.tab.zSB.setText(str(caget(self.gui.macros["ZSB"])))
        self.gui.tab.xOB.setText(str(caget(self.gui.macros["XOB"])))
        self.gui.tab.yOB.setText(str(caget(self.gui.macros["YOB"])))
        self.gui.tab.zOB.setText(str(caget(self.gui.macros["ZOB"])))

        # Set relative position global variables to current motor position.
        self.gui.macros["XS_RELATIVE_POSITION"] = caget(self.gui.macros["XSABSPOS"])
        self.gui.macros["YS_RELATIVE_POSITION"] = caget(self.gui.macros["YSABSPOS"])
        self.gui.macros["ZS_RELATIVE_POSITION"] = caget(self.gui.macros["ZSABSPOS"])
        self.gui.macros["XO_RELATIVE_POSITION"] = caget(self.gui.macros["XOABSPOS"])
        self.gui.macros["YO_RELATIVE_POSITION"] = caget(self.gui.macros["YOABSPOS"])
        self.gui.macros["ZO_RELATIVE_POSITION"] = caget(self.gui.macros["ZOABSPOS"])

        self.PV_XSABSPOS = PV(pvname=self.gui.macros["XSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_ySABSPOS = PV(pvname=self.gui.macros["YSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zSABSPOS = PV(pvname=self.gui.macros["ZSABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_XOABSPOS = PV(pvname=self.gui.macros["XOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_yOABSPOS = PV(pvname=self.gui.macros["YOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)
        self.PV_zOABSPOS = PV(pvname=self.gui.macros["ZOABSPOS"], auto_monitor=True, callback=self.updateAbsPos)

        self.PV_XSSTATE = PV(pvname=self.gui.macros["XSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YSSTATE = PV(pvname=self.gui.macros["YSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZSSTATE = PV(pvname=self.gui.macros["ZSSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_XOSTATE = PV(pvname=self.gui.macros["XOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_YOSTATE = PV(pvname=self.gui.macros["YOSTATE"], auto_monitor=True, callback=self.motorStatus)
        self.PV_ZOSTATE = PV(pvname=self.gui.macros["ZOSTATE"], auto_monitor=True, callback=self.motorStatus)

        self.PV_XSHN = PV(pvname=self.gui.macros["XSHN"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_XSHP = PV(pvname=self.gui.macros["XSHP"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_YSHN = PV(pvname=self.gui.macros["YSHN"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_YSHP = PV(pvname=self.gui.macros["YSHP"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_ZSHN = PV(pvname=self.gui.macros["ZSHN"], auto_monitor=True, callback=self.setHardLimitInd)
        self.PV_ZSHP = PV(pvname=self.gui.macros["ZSHP"], auto_monitor=True, callback=self.setHardLimitInd)

        self.PV_XSPOS = PV(pvname=self.gui.macros["XSPOS"], auto_monitor=True, callback=self.updateSteps)
        self.PV_YSPOS = PV(pvname=self.gui.macros["YSPOS"], auto_monitor=True, callback=self.updateSteps)
        self.PV_ZSPOS = PV(pvname=self.gui.macros["ZSPOS"], auto_monitor=True, callback=self.updateSteps)
        self.PV_XOPOS = PV(pvname=self.gui.macros["XOPOS"], auto_monitor=True, callback=self.updateSteps)
        self.PV_YOPOS = PV(pvname=self.gui.macros["YOPOS"], auto_monitor=True, callback=self.updateSteps)
        self.PV_ZOPOS = PV(pvname=self.gui.macros["ZOPOS"], auto_monitor=True, callback=self.updateSteps)

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
        self.gui.tab.RDM1.pressed.connect(partial(self.modeState, 1, self.modeMotor))
        self.gui.tab.RDM2.pressed.connect(partial(self.modeState, 2, self.modeMotor))
        self.gui.tab.RDM3.pressed.connect(partial(self.modeState, 3, self.modeMotor))
        self.gui.tab.RDM4.pressed.connect(partial(self.modeState, 4, self.modeMotor))

        # Mode position customizarion functionality.
        self.gui.tab.TMTMbutton.clicked.connect(partial(self.modePos, 1))
        self.gui.tab.TMRMbutton.clicked.connect(partial(self.modePos, 2))
        self.gui.tab.TMVMbutton.clicked.connect(partial(self.modePos, 3))
        self.gui.tab.TMBMbutton.clicked.connect(partial(self.modePos, 4))

        # Increment sample and objective stage functionality.
        self.gui.xSN.clicked.connect(partial(self.incPos, "S", "X", "N", self.gui.xSStep))
        self.gui.xSP.clicked.connect(partial(self.incPos, "S", "X", "P", self.gui.xSStep))
        self.gui.ySN.clicked.connect(partial(self.incPos, "S", "Y", "N", self.gui.ySStep))
        self.gui.ySP.clicked.connect(partial(self.incPos, "S", "Y", "P", self.gui.ySStep))
        self.gui.zSN.clicked.connect(partial(self.incPos, "S", "Z", "N", self.gui.zSStep))
        self.gui.zSP.clicked.connect(partial(self.incPos, "S", "Z", "P", self.gui.zSStep))
        self.gui.xON.clicked.connect(partial(self.incPos, "O", "X", "N", self.gui.xOStep))
        self.gui.xOP.clicked.connect(partial(self.incPos, "O", "X", "P", self.gui.xOStep))
        self.gui.yON.clicked.connect(partial(self.incPos, "O", "Y", "N", self.gui.yOStep))
        self.gui.yOP.clicked.connect(partial(self.incPos, "O", "Y", "P", self.gui.yOStep))
        self.gui.zON.clicked.connect(partial(self.incPos, "O", "Z", "N", self.gui.zOStep))
        self.gui.zOP.clicked.connect(partial(self.incPos, "O", "Z", "P", self.gui.zOStep))

        # Move sample and objective stage to absolute position functionality.
        self.gui.xSMove.clicked.connect(partial(self.absMove, "S", "X"))
        self.gui.ySMove.clicked.connect(partial(self.absMove, "S", "Y"))
        self.gui.zSMove.clicked.connect(partial(self.absMove, "S", "Z"))
        self.gui.xOMove.clicked.connect(partial(self.absMove, "O", "X"))
        self.gui.yOMove.clicked.connect(partial(self.absMove, "O", "Y"))
        self.gui.zOMove.clicked.connect(partial(self.absMove, "O", "Z"))

        # Continuous motion of the sample and objective stages functionality.
        self.gui.xSCn.clicked.connect(partial(self.continuousMotion, "S", "X", "CN"))
        self.gui.xSStop.clicked.connect(partial(self.continuousMotion, "S", "X", "STOP"))
        self.gui.xSCp.clicked.connect(partial(self.continuousMotion, "S", "X", "CP"))
        self.gui.ySCn.clicked.connect(partial(self.continuousMotion, "S", "Y", "CN"))
        self.gui.ySStop.clicked.connect(partial(self.continuousMotion, "S", "Y", "STOP"))
        self.gui.ySCp.clicked.connect(partial(self.continuousMotion, "S", "Y", "CP"))
        self.gui.zSCn.clicked.connect(partial(self.continuousMotion, "S", "Z", "CN"))
        self.gui.zSStop.clicked.connect(partial(self.continuousMotion, "S", "Z", "STOP"))
        self.gui.zSCp.clicked.connect(partial(self.continuousMotion, "S", "Z", "CP"))
        self.gui.xOCn.clicked.connect(partial(self.continuousMotion, "O", "X", "CN"))
        self.gui.xOStop.clicked.connect(partial(self.continuousMotion, "O", "X", "STOP"))
        self.gui.xOCp.clicked.connect(partial(self.continuousMotion, "O", "X", "CP"))
        self.gui.yOCn.clicked.connect(partial(self.continuousMotion, "O", "Y", "CN"))
        self.gui.yOStop.clicked.connect(partial(self.continuousMotion, "O", "Y", "STOP"))
        self.gui.yOCp.clicked.connect(partial(self.continuousMotion, "O", "Y", "CP"))
        self.gui.zOCn.clicked.connect(partial(self.continuousMotion, "O", "Z", "CN"))
        self.gui.zOStop.clicked.connect(partial(self.continuousMotion, "O", "Z", "STOP"))
        self.gui.zOCp.clicked.connect(partial(self.continuousMotion, "O", "Z", "CP"))

        # Updating soft limits functionality.
        self.gui.tab.SSL.clicked.connect(partial(self.updateSoftLimits, 0))
        self.gui.tab.SMSL.clicked.connect(partial(self.updateSoftLimits, 1))
        self.gui.tab.SESL.clicked.connect(partial(self.updateSoftLimits, 2))

        # Zero'ing absolute position functionality.
        self.gui.tab.xSZero.clicked.connect(partial(self.zeroPos, "S", "X"))
        self.gui.tab.ySZero.clicked.connect(partial(self.zeroPos, "S", "Y"))
        self.gui.tab.zSZero.clicked.connect(partial(self.zeroPos, "S", "Z"))
        self.gui.tab.xOZero.clicked.connect(partial(self.zeroPos, "O", "X"))
        self.gui.tab.yOZero.clicked.connect(partial(self.zeroPos, "O", "Y"))
        self.gui.tab.zOZero.clicked.connect(partial(self.zeroPos, "O", "Z"))

        self.gui.tab.SBL.clicked.connect(self.updateBacklash)

        self.gui.tab.valueType.clicked.connect(self.changeValues)

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
        plt.savefig(path, dpi=500, bbox_inches="tight")

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
        # Set move_to position based on mode.
        if mode == 1:
            pos = self.gui.macros["TRANSMISSION_POSITION"]
        elif mode == 2:
            pos = self.gui.macros["REFLECTION_POSITION"]
        elif mode == 3:
            pos = self.gui.macros["VISIBLE_IMAGE_POSITION"]
        else:
            pos = self.gui.macros["BEAMSPLITTER_POSITION"]

        changeMode(pos=pos, modeMotor=modeMotor)

        print(f"Changing mode to mode {mode}.")

    def modePos(self, mode):
        """
        """
        if mode == 1:
            self.gui.macros["TRANSMISSION_POSITION"] = float(
                self.gui.tab.TMTM.text())
            if self.gui.tab.RDM1.isChecked():
                self.modeState(1, self.modeMotor)
        elif mode == 2:
            self.gui.macros["REFLECTION_POSITION"] = float(
                self.gui.tab.TMRM.text())
            if self.gui.tab.RDM2.isChecked():
                self.modeState(2, self.modeMotor)
        elif mode == 3:
            self.gui.macros["VISUAL_IMAGE_POSITION"] = float(
                self.gui.tab.TMVM.text())
            if self.gui.tab.RDM3.isChecked():
                self.modeState(3, self.modeMotor)
        else:
            self.gui.macros["BEAMSPLITTER_POSITION"] = float(
                self.gui.tab.TMBM.text())
            if self.gui.tab.RDM4.isChecked():
                self.modeState(4, self.modeMotor)

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
        caput(self.gui.macros[f"{axis}{object}STEP"], float(step.text()))
        caput(self.gui.macros[f"{axis}{object}{direction}"], 1)
        caput(self.gui.macros[f"{axis}{object}{direction}"], 0)

        # -Simulation----------------------------------------------------------
        absPos = caget(self.gui.macros[f"{axis}{object}ABSPOS"])
        print(f"Incremental movement to {axis}{object}ABSPOS = {absPos}.")
        # ---------------------------------------------------------------------

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
        caput(self.gui.macros[f"{axis}{object}ABSPOS"], absPos)

        caput(self.gui.macros[f"{axis}{object}MOVE"], 1)
        caput(self.gui.macros[f"{axis}{object}MOVE"], 0)

        # -Simulation----------------------------------------------------------
        absPos = caget(self.gui.macros[f"{axis}{object}ABSPOS"])
        print(f"Absolute movement to {axis}{object}ABSPOS = {absPos}.")
        # ---------------------------------------------------------------------

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
        if type == "CN":
            caput(self.gui.macros[f"{axis}{object}CN"], -1000000)
        elif type == "CP":
            caput(self.gui.macros[f"{axis}{object}CP"], 1000000)
        else:
            caput(self.gui.macros[f"{axis}{object}STOP"], 1)
            caput(self.gui.macros[f"{axis}{object}STOP"], 0)

        # -Simulation----------------------------------------------------------
        print(f"Change continuous movement to -> {type}.")
        # ---------------------------------------------------------------------

    def updateAbsPos(self, **kwargs: Dict) -> None:
        """Update absolute value line edit.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `updateAbsPos`: refer to PyEpics documentation
            for a list of all possible arguments for PV callback functions.

        Returns
        -------
        None
        """
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos, ("S", "Y"): self.gui.ySAbsPos,
                    ("O", "Y"): self.gui.yOAbsPos, ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        lineEdit[(object, axis)].setText(str(value + self.offset(object, axis)))

        # -Simulation----------------------------------------------------------
        print(f"Updating absolute position line edit to relative position: {value + self.offset(object, axis)}.")
        # ---------------------------------------------------------------------

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
        softLimits = {("S", "X", 0): self.gui.tab.xSMin, ("S", "X", 1): self.gui.tab.xSMax,
                      ("S", "Y", 0): self.gui.tab.ySMin, ("S", "Y", 1): self.gui.tab.ySMax,
                      ("S", "Z", 0): self.gui.tab.zSMin, ("S", "Z", 1): self.gui.tab.zSMax,
                      ("O", "X", 0): self.gui.tab.xOMin, ("O", "X", 1): self.gui.tab.xOMax,
                      ("O", "Y", 0): self.gui.tab.yOMin, ("O", "Y", 1): self.gui.tab.yOMax,
                      ("O", "Z", 0): self.gui.tab.zOMin, ("O", "Z", 1): self.gui.tab.zOMax}

        # Set soft limits to inputted values
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:

                min = float(softLimits[(object, axis, 0)].text())
                max = float(softLimits[(object, axis, 1)].text())

                caput(self.gui.macros[f"{axis}{object}SN"], min)
                caput(self.gui.macros[f"{axis}{object}SP"], max)

        self.checkMotorPos()

        # -Simulation----------------------------------------------------------
        print(f"Updating soft limits, buttonID={buttonID}.")
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                Min = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]
                Max = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
                print(f"XS SL: min -> {Min}, max -> {Max}")
        # ---------------------------------------------------------------------

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
        caput(self.gui.macros["XSB"], abs(int(float(self.gui.tab.xSB.text()))))
        caput(self.gui.macros["YSB"], abs(int(float(self.gui.tab.ySB.text()))))
        caput(self.gui.macros["ZSB"], abs(int(float(self.gui.tab.zSB.text()))))
        caput(self.gui.macros["XOB"], abs(int(float(self.gui.tab.xOB.text()))))
        caput(self.gui.macros["YOB"], abs(int(float(self.gui.tab.yOB.text()))))
        caput(self.gui.macros["ZOB"], abs(int(float(self.gui.tab.zOB.text()))))

        self.gui.tab.xSB.setText(str(caget(self.gui.macros["XSB"])))
        self.gui.tab.ySB.setText(str(caget(self.gui.macros["YSB"])))
        self.gui.tab.zSB.setText(str(caget(self.gui.macros["ZSB"])))
        self.gui.tab.xOB.setText(str(caget(self.gui.macros["XOB"])))
        self.gui.tab.yOB.setText(str(caget(self.gui.macros["YOB"])))
        self.gui.tab.zOB.setText(str(caget(self.gui.macros["ZOB"])))

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
        caput(self.gui.macros[f"{axis}{object}ZERO"], 1)        
        caput(self.gui.macros[f"{axis}{object}ZERO"], 0)

        # -Simulation----------------------------------------------------------
        print(f"Zero'ing the {axis}{object}ABSPOS line edit.")
        # ---------------------------------------------------------------------

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
        motionLabels = {("S", "X"): self.gui.tab.xIdleS,
                        ("S", "Y"): self.gui.tab.yIdleS,
                        ("S", "Z"): self.gui.tab.zIdleS,
                        ("O", "X"): self.gui.tab.xIdleO,
                        ("O", "Y"): self.gui.tab.yIdleO,
                        ("O", "Z"): self.gui.tab.zIdleO}

        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos, ("S", "Y"): self.gui.ySAbsPos,
                    ("O", "Y"): self.gui.yOAbsPos, ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        if value == 0:
            motionLabels[(object, axis)].setText("IDLE")
            motionLabels[(object, axis)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")
            self.setSoftLimitInd(object, axis)
        elif value == 1:
            motionLabels[(object, axis)].setText("POWERING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #edde07; border: 1px solid black;")
            self.setSoftLimitInd(object, axis)
        elif value == 2:
            motionLabels[(object, axis)].setText("POWERED")
            motionLabels[(object, axis)].setStyleSheet("background-color: #edde07; border: 1px solid black;")
            self.setSoftLimitInd(object, axis)
        elif value == 3:
            motionLabels[(object, axis)].setText("RELEASING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #ff4747; border: 1px solid black;")
            self.setSoftLimitInd(object, axis)
        elif value == 4:
            motionLabels[(object, axis)].setText("ACTIVE")
            motionLabels[(object, axis)].setStyleSheet("background-color: #3ac200; border: 1px solid black;")
        elif value == 5:
            motionLabels[(object, axis)].setText("APPLYING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #ff4747; border: 1px solid black;")
            self.setSoftLimitInd(object, axis)
        else:
            motionLabels[(object, axis)].setText("UNPOWERING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #edde07; border: 1px solid black;")
            self.setSoftLimitInd(object, axis)

        # -Simulation----------------------------------------------------------
        print(f"Checking motor status, motor identity: {pvname}, state: {value}")
        # ---------------------------------------------------------------------

    def setHardLimitInd(self, **kwargs):
        """
        """
        hardLimits = {("S", "X", "N"): self.gui.xSHn, ("S", "X", "P"): self.gui.xSHp,
                      ("S", "Y", "N"): self.gui.ySHn, ("S", "Y", "P"): self.gui.ySHp,
                      ("S", "Z", "N"): self.gui.zSHn, ("S", "Z", "P"): self.gui.zSHp,
                      ("O", "X", "N"): self.gui.xOHn, ("O", "X", "P"): self.gui.xOHp,
                      ("O", "Y", "N"): self.gui.yOHn, ("O", "Y", "P"): self.gui.yOHp,
                      ("O", "Z", "N"): self.gui.zOHn, ("O", "Z", "P"): self.gui.zOHp}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]
        direction = pvKey[3]

        if value > 0:
            hardLimits[(object, axis, direction)].setStyleSheet("background-color: #3ac200; border: 1px solid black;")
        else:
            hardLimits[(object, axis, direction)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # -Simulation----------------------------------------------------------
        print("Setting hard limit indicators.")
        # ---------------------------------------------------------------------

    def setSoftLimitInd(self, object, axis):
        """Set soft limit indicators.


        set soft limits if scheduled to move to soft limits
        """
        softLimits = {("S", "X", 0): self.gui.xSSn, ("S", "X", 1): self.gui.xSSp,
                      ("S", "Y", 0): self.gui.ySSn, ("S", "Y", 1): self.gui.ySSp,
                      ("S", "Z", 0): self.gui.zSSn, ("S", "Z", 1): self.gui.zSSp,
                      ("O", "X", 0): self.gui.xOSn, ("O", "X", 1): self.gui.xOSp,
                      ("O", "Y", 0): self.gui.yOSn, ("O", "Y", 1): self.gui.yOSp,
                      ("O", "Z", 0): self.gui.zOSn, ("O", "Z", 1): self.gui.zOSp}

        value = caget(self.gui.macros[f"{axis}{object}POS"])
        minSoftLim = caget(self.gui.macros[f"{axis}{object}SN"])
        maxSoftLim = caget(self.gui.macros[f"{axis}{object}SP"])

        # Set maximum soft limit indicator.
        if value != 0 and value <= minSoftLim:
            softLimits[(object, axis, 1)].setStyleSheet("background-color: #3ac200; border: 1px solid black;")
        else:
            softLimits[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Set minimum soft limit indicator.
        if value != 0 and value >= maxSoftLim:
            softLimits[(object, axis, 0)].setStyleSheet("background-color: #3ac200; border: 1px solid black;")
        else:
            softLimits[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # -Simulation----------------------------------------------------------
        print("Setting soft limit indicators.")
        # ---------------------------------------------------------------------

    def updateSteps(self, **kwargs):
        """
        """
        stepLineEdit = {("S", "X"): self.gui.tab.xStepS, ("O", "X"): self.gui.tab.xStepO,
                        ("S", "Y"): self.gui.tab.yStepS, ("O", "Y"): self.gui.tab.yStepO,
                        ("S", "Z"): self.gui.tab.zStepS, ("O", "Z"): self.gui.tab.zStepO}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        stepText = f"<b>{value} STEPS</b>"
        stepLineEdit[(object, axis)].setText(stepText)

    def displayGlobals(self):
        """Print out all global variables.

        Parameters
        ----------
        None

        Returns
        -------
        None     
        """
        print("-*- GLOBAL VARIABLES - START -*-")

        keys = list(self.gui.macros.keys())
        for key in keys:
            print(f"{key} -> {self.gui.macros[key]}")

        print("-*- GLOBAL VARIABLES - END -*-")
