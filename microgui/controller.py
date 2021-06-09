"""Create widgets interactive nature.

The controller module brings life to the GUI defined through the gui module by
connecting widgets up to control sequences that bring about change.
"""


# Import package dependencies.
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from epics import ca, caput, caget, PV
from typing import Literal, Dict, Any, Union
from PyQt5.QtWidgets import QLineEdit, QFileDialog
from thorlabs_apt import Motor

# Import file dependencies.
from thorlabs_motor_control import enable, disable, home, changeMode
from gui import GUI


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
    _initialize_GUI()
        Configure and initiallize PVs.
    _connect_signals()
        Connect the widgets to a control sequence.
    _save_image()
        Control sequence to capture an image of the live feed.
    _mode_state(mode, modeMotor)
        Control sequence to change the microscope mode.
    _mode_position(mode)
        Change Mode position settings.
    _increment(object, axis, direction, step)
        Control sequence to increment sample and objective stage motors.
    _absolute(object, axis, pos)
        Control sequence to move the sample and objective stage motors to a set
        point.
    _continuous(object, axis, type)
        Control sequence for the continuous motion of the sample and objective
        stages.
    _update_abs_pos(**kwargs)
        Control sequence to update the absolute position line edit widget.
    _offset(object, axis, invert)
        Generate offset to convert between actual and relative values.
    _update_soft_lim(buttonID)
        Control sequence to set soft limits to the inputted soft limits.
    _update_BL()
        Control sequence to update backlash values.
    _zero(object, axis)
        Control sequence to zero the current motor positions.
    _motor_status(**kwargs)
        Control sequence to check and set mode status indicators.
    _check_motor_position()
        Control sequence to move motors within soft limits.
    _hard_lim_indicators(**kwargs)
        Control sequence to set hard limit indicators.
    _soft_lim_indicators(object, axis)
        Control sequence to set doft limit indicators.
    _change_display_vals()
        Control sequence to switch displayed values between actual and relative values.
    _set_current_position(**kwargs)
        Control sequence to update current position labels.
    _print_globals()
        Control sequence to display all global variables.
    """

    def __init__(self, gui: GUI, modeMotor: Motor) -> None:
        """Initialize the Controller."""
        self.gui = gui
        self.modeMotor = modeMotor

        self._initialize_GUI()
        self._connect_signals()

    def _initialize_GUI(self) -> None:
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

        # Set absolute position PV monitoring and callback.
        self.PV_XSABSPOS = PV(pvname=self.gui.macros["XSABSPOS"], auto_monitor=True, callback=self._update_abs_pos)
        self.PV_ySABSPOS = PV(pvname=self.gui.macros["YSABSPOS"], auto_monitor=True, callback=self._update_abs_pos)
        self.PV_zSABSPOS = PV(pvname=self.gui.macros["ZSABSPOS"], auto_monitor=True, callback=self._update_abs_pos)
        self.PV_XOABSPOS = PV(pvname=self.gui.macros["XOABSPOS"], auto_monitor=True, callback=self._update_abs_pos)
        self.PV_yOABSPOS = PV(pvname=self.gui.macros["YOABSPOS"], auto_monitor=True, callback=self._update_abs_pos)
        self.PV_zOABSPOS = PV(pvname=self.gui.macros["ZOABSPOS"], auto_monitor=True, callback=self._update_abs_pos)

        # Set state PV monitoring and callback.
        self.PV_XSSTATE = PV(pvname=self.gui.macros["XSSTATE"], auto_monitor=True, callback=self._motor_status)
        self.PV_YSSTATE = PV(pvname=self.gui.macros["YSSTATE"], auto_monitor=True, callback=self._motor_status)
        self.PV_ZSSTATE = PV(pvname=self.gui.macros["ZSSTATE"], auto_monitor=True, callback=self._motor_status)
        self.PV_XOSTATE = PV(pvname=self.gui.macros["XOSTATE"], auto_monitor=True, callback=self._motor_status)
        self.PV_YOSTATE = PV(pvname=self.gui.macros["YOSTATE"], auto_monitor=True, callback=self._motor_status)
        self.PV_ZOSTATE = PV(pvname=self.gui.macros["ZOSTATE"], auto_monitor=True, callback=self._motor_status)

        # Set hard limit position PV monitoring and callback.
        self.PV_XSHN = PV(pvname=self.gui.macros["XSHN"], auto_monitor=True, callback=self._hard_lim_indicators)
        self.PV_XSHP = PV(pvname=self.gui.macros["XSHP"], auto_monitor=True, callback=self._hard_lim_indicators)
        self.PV_YSHN = PV(pvname=self.gui.macros["YSHN"], auto_monitor=True, callback=self._hard_lim_indicators)
        self.PV_YSHP = PV(pvname=self.gui.macros["YSHP"], auto_monitor=True, callback=self._hard_lim_indicators)
        self.PV_ZSHN = PV(pvname=self.gui.macros["ZSHN"], auto_monitor=True, callback=self._hard_lim_indicators)
        self.PV_ZSHP = PV(pvname=self.gui.macros["ZSHP"], auto_monitor=True, callback=self._hard_lim_indicators)

        # Set current position PV monitoring and callback.
        self.PV_XSPOS = PV(pvname=self.gui.macros["XSPOS"], auto_monitor=True, callback=self._set_current_position)
        self.PV_YSPOS = PV(pvname=self.gui.macros["YSPOS"], auto_monitor=True, callback=self._set_current_position)
        self.PV_ZSPOS = PV(pvname=self.gui.macros["ZSPOS"], auto_monitor=True, callback=self._set_current_position)
        self.PV_XOPOS = PV(pvname=self.gui.macros["XOPOS"], auto_monitor=True, callback=self._set_current_position)
        self.PV_YOPOS = PV(pvname=self.gui.macros["YOPOS"], auto_monitor=True, callback=self._set_current_position)
        self.PV_ZOPOS = PV(pvname=self.gui.macros["ZOPOS"], auto_monitor=True, callback=self._set_current_position)

        self._append_text("-*- PVs configured and initialized. -*-")

    def _connect_signals(self) -> None:
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
        self.gui.WCB.clicked.connect(self._save_image)

        # Mode select functionality.
        self.gui.tab.RDM1.pressed.connect(partial(self._mode_state, 1, self.modeMotor))
        self.gui.tab.RDM2.pressed.connect(partial(self._mode_state, 2, self.modeMotor))
        self.gui.tab.RDM3.pressed.connect(partial(self._mode_state, 3, self.modeMotor))
        self.gui.tab.RDM4.pressed.connect(partial(self._mode_state, 4, self.modeMotor))

        # THORLABS/mode motor functionality.
        self.gui.tab.enableDisable.clicked.connect(self.enableTHORLABS)
        self.gui.tab.home.clicked.connect(self.homeTHORLABS)

        # Mode position customizarion functionality.
        self.gui.tab.TMTMbutton.clicked.connect(partial(self._mode_position, 1))
        self.gui.tab.TMRMbutton.clicked.connect(partial(self._mode_position, 2))
        self.gui.tab.TMVMbutton.clicked.connect(partial(self._mode_position, 3))
        self.gui.tab.TMBMbutton.clicked.connect(partial(self._mode_position, 4))

        # Increment sample and objective stage functionality.
        self.gui.xSN.clicked.connect(partial(self._increment, "S", "X", "N", self.gui.xSStep))
        self.gui.xSP.clicked.connect(partial(self._increment, "S", "X", "P", self.gui.xSStep))
        self.gui.ySN.clicked.connect(partial(self._increment, "S", "Y", "N", self.gui.ySStep))
        self.gui.ySP.clicked.connect(partial(self._increment, "S", "Y", "P", self.gui.ySStep))
        self.gui.zSN.clicked.connect(partial(self._increment, "S", "Z", "N", self.gui.zSStep))
        self.gui.zSP.clicked.connect(partial(self._increment, "S", "Z", "P", self.gui.zSStep))
        self.gui.xON.clicked.connect(partial(self._increment, "O", "X", "N", self.gui.xOStep))
        self.gui.xOP.clicked.connect(partial(self._increment, "O", "X", "P", self.gui.xOStep))
        self.gui.yON.clicked.connect(partial(self._increment, "O", "Y", "N", self.gui.yOStep))
        self.gui.yOP.clicked.connect(partial(self._increment, "O", "Y", "P", self.gui.yOStep))
        self.gui.zON.clicked.connect(partial(self._increment, "O", "Z", "N", self.gui.zOStep))
        self.gui.zOP.clicked.connect(partial(self._increment, "O", "Z", "P", self.gui.zOStep))

        # Move sample and objective stage to absolute position functionality.
        self.gui.xSMove.clicked.connect(partial(self._absolute, "S", "X"))
        self.gui.ySMove.clicked.connect(partial(self._absolute, "S", "Y"))
        self.gui.zSMove.clicked.connect(partial(self._absolute, "S", "Z"))
        self.gui.xOMove.clicked.connect(partial(self._absolute, "O", "X"))
        self.gui.yOMove.clicked.connect(partial(self._absolute, "O", "Y"))
        self.gui.zOMove.clicked.connect(partial(self._absolute, "O", "Z"))

        # Continuous motion of the sample and objective stages functionality.
        self.gui.xSCn.clicked.connect(partial(self._continuous, "S", "X", "CN"))
        self.gui.xSStop.clicked.connect(partial(self._continuous, "S", "X", "STOP"))
        self.gui.xSCp.clicked.connect(partial(self._continuous, "S", "X", "CP"))
        self.gui.ySCn.clicked.connect(partial(self._continuous, "S", "Y", "CN"))
        self.gui.ySStop.clicked.connect(partial(self._continuous, "S", "Y", "STOP"))
        self.gui.ySCp.clicked.connect(partial(self._continuous, "S", "Y", "CP"))
        self.gui.zSCn.clicked.connect(partial(self._continuous, "S", "Z", "CN"))
        self.gui.zSStop.clicked.connect(partial(self._continuous, "S", "Z", "STOP"))
        self.gui.zSCp.clicked.connect(partial(self._continuous, "S", "Z", "CP"))
        self.gui.xOCn.clicked.connect(partial(self._continuous, "O", "X", "CN"))
        self.gui.xOStop.clicked.connect(partial(self._continuous, "O", "X", "STOP"))
        self.gui.xOCp.clicked.connect(partial(self._continuous, "O", "X", "CP"))
        self.gui.yOCn.clicked.connect(partial(self._continuous, "O", "Y", "CN"))
        self.gui.yOStop.clicked.connect(partial(self._continuous, "O", "Y", "STOP"))
        self.gui.yOCp.clicked.connect(partial(self._continuous, "O", "Y", "CP"))
        self.gui.zOCn.clicked.connect(partial(self._continuous, "O", "Z", "CN"))
        self.gui.zOStop.clicked.connect(partial(self._continuous, "O", "Z", "STOP"))
        self.gui.zOCp.clicked.connect(partial(self._continuous, "O", "Z", "CP"))

        # Updating soft limits functionality.
        self.gui.tab.SSL.clicked.connect(partial(self._update_soft_lim, 0))
        self.gui.tab.SMSL.clicked.connect(partial(self._update_soft_lim, 1))
        self.gui.tab.SESL.clicked.connect(partial(self._update_soft_lim, 2))

        # Zero'ing absolute position functionality.
        self.gui.tab.xSZero.clicked.connect(partial(self._zero, "S", "X"))
        self.gui.tab.ySZero.clicked.connect(partial(self._zero, "S", "Y"))
        self.gui.tab.zSZero.clicked.connect(partial(self._zero, "S", "Z"))
        self.gui.tab.xOZero.clicked.connect(partial(self._zero, "O", "X"))
        self.gui.tab.yOZero.clicked.connect(partial(self._zero, "O", "Y"))
        self.gui.tab.zOZero.clicked.connect(partial(self._zero, "O", "Z"))

        # Other functionality.
        self.gui.tab.SBL.clicked.connect(self._update_BL)
        self.gui.tab.valueType.clicked.connect(self._change_display_vals)
        self.gui.tab.globals.clicked.connect(self._print_globals)

        self._append_text("-*- Widgets connected to control sequences. -*-")

    def _save_image(self) -> None:
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
        path, _ = QFileDialog.getSaveFileName(self.gui, "Save File", "sample_capture", "Image files (*.jpg *.jpeg *.gif *png)")

        plt.figure()
        plt.imshow(np.rot90(self.gui.image, 3))
        plt.axis("off")
        plt.savefig(path, dpi=500, bbox_inches="tight")

        self._append_text(f"Image capture saved to: {path}")

    def _mode_state(self, mode: Literal[1, 2, 3, 4], modeMotor: Motor) -> None:
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
        modeDict = {1: "TRANSMISSION_POSITION", 2: "REFLECTION_POSITION",
                    3: "VISIBLE_IMAGE_POSITION", 4: "BEAMSPLITTER_POSITION"}
        pos = self.gui.macros[modeDict[mode]]
        changeMode(pos=pos, modeMotor=modeMotor)

        self._append_text(f"Changing mode.")

    def _mode_position(self, mode: Literal[1, 2, 3, 4]) -> None:
        """Change mode position settings.

        Parameters
        ----------
        mode : {1, 2, 3, 4}
            The mode's position to be updated.
        
        Returns
        -------
        None
        """
        if mode == 1:
            self.gui.macros["TRANSMISSION_POSITION"] = float(self.gui.tab.TMTM.text())
            self.gui.tab.TMTM.setText(str(self.gui.macros["TRANSMISSION_POSITION"]))
            if self.gui.tab.RDM1.isChecked():
                self._mode_state(1, self.modeMotor)
        elif mode == 2:
            self.gui.macros["REFLECTION_POSITION"] = float(self.gui.tab.TMRM.text())
            self.gui.tab.TMRM.setText(str(self.gui.macros["REFLECTION_POSITION"]))
            if self.gui.tab.RDM2.isChecked():
                self._mode_state(2, self.modeMotor)
        elif mode == 3:
            self.gui.macros["VISIBLE_IMAGE_POSITION"] = float(self.gui.tab.TMVM.text())
            self.gui.tab.TMVM.setText(str(self.gui.macros["VISIBLE_IMAGE_POSITION"]))
            if self.gui.tab.RDM3.isChecked():
                self._mode_state(3, self.modeMotor)
        else:
            self.gui.macros["BEAMSPLITTER_POSITION"] = float(self.gui.tab.TMBM.text())
            self.gui.tab.TMBM.setText(str(self.gui.macros["BEAMSPLITTER_POSITION"]))
            if self.gui.tab.RDM4.isChecked():
                self._mode_state(4, self.modeMotor)
    
    def enableTHORLABS(self):
        """
        """
        label = self.gui.tab.enableDisable.text()
        if label == "Enable":
            enable(self.modeMotor)
            self.gui.tab.enableDisable.setText("Disable")
        else:
            disable(self.modeMotor)
            self.gui.tab.enableDisable.setText("Enable")

    def homeTHORLABS(self):
        """
        """
        try:
            home(self.modeMotor)
            self.gui.tab.RDM1.setChecked(False)
            self.gui.tab.RDM2.setChecked(False)
            self.gui.tab.RDM3.setChecked(False)
            self.gui.tab.RDM4.setChecked(False)
        except:
            self._append_text("ERROR: Motor cannot be homed.")

    def _increment(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"], direction: Literal["N", "P"], step: QLineEdit) -> None:
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
        basePos = self.gui.macros[f"{axis}{object}_BASE_POSITION"]
        relPos = self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"]
        incPos = float(step.text())

        PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

        if direction == "P" and basePos + relPos + incPos > PSL:
            incPos = PSL - basePos - relPos
            relPos = PSL - basePos
        elif direction == "N" and basePos + relPos - incPos < NSL:
            incPos = basePos + relPos - NSL
            relPos = NSL - basePos
        else:
            if direction == "P":
                relPos = relPos + incPos
            else:
                relPos = relPos - incPos

        self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"] = relPos
        caput(self.gui.macros[f"{axis}{object}STEP"], incPos)
        caput(self.gui.macros[f"{axis}{object}{direction}"], 1)

    def _absolute(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"]) -> None:
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
        basePos = self.gui.macros[f"{axis}{object}_BASE_POSITION"]

        PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

        if basePos + absPos > PSL:
            relPos = PSL - basePos
            absPos = PSL
        elif basePos + absPos < NSL:
            relPos = NSL - basePos
            absPos = NSL
        else:
            relPos = absPos
            absPos += basePos

        self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"] = relPos
        caput(self.gui.macros[f"{axis}{object}ABSPOS"], absPos)
        caput(self.gui.macros[f"{axis}{object}MOVE"], 1)
        caput(self.gui.macros[f"{axis}{object}MOVE"], 0)

        if not self.gui.tab.valueType.isChecked():
            lineEdit[(object, axis)].setText(str(relPos))
        else:
            lineEdit[(object, axis)].setText(str(basePos + relPos))

    def _continuous(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"], type: Literal["CN", "STOP", "CP"]) -> None:
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
            caput(self.gui.macros[f"{axis}{object}CN"], self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"])
        elif type == "CP":
            caput(self.gui.macros[f"{axis}{object}CP"], self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"])
        else:
            caput(self.gui.macros[f"{axis}{object}STOP"], 1)
            caput(self.gui.macros[f"{axis}{object}STOP"], 0)

    def _update_abs_pos(self, **kwargs: Union[str, int, float]) -> None:
        """Update absolute value line edit.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `_update_abs_pos`: refer to PyEpics documentation
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

        lineEdit[(object, axis)].setText(str(value + self._offset(object, axis)))

    def _offset(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"], invert: bool = False) -> Union[int, float]:
        """Generate offset to convert between actual and relative values.

        This method is to always be ADDED (not subtracted) to a value to
        convert between relative and absolute positions.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample or orbjective using "S" and "O",
            respectively.
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z using "X", "Y", "Z",
            respectively.
        
        invert : bool, optional
            Inverts the condition on returning the base position
        
        Returns
        -------
        float
            Offset to be applied.
        """
        if not invert and self.gui.tab.valueType.isChecked():
            return float(self.gui.macros[f"{axis}{object}_BASE_POSITION"])
        elif invert and not self.gui.tab.valueType.isChecked():
            return float(self.gui.macros[f"{axis}{object}_BASE_POSITION"])
        return 0

    def _update_soft_lim(self, buttonID: Literal[0, 1]) -> None:
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

        if buttonID == 2:
            # Set soft limits to hard limits.
            self.gui.macros["XSMIN_SOFT_LIMIT"] = float(self.gui.macros["XSMIN_HARD_LIMIT"])
            self.gui.macros["XSMAX_SOFT_LIMIT"] = float(self.gui.macros["XSMAX_HARD_LIMIT"])
            self.gui.macros["YSMIN_SOFT_LIMIT"] = float(self.gui.macros["YSMIN_HARD_LIMIT"])
            self.gui.macros["YSMAX_SOFT_LIMIT"] = float(self.gui.macros["YSMAX_HARD_LIMIT"])
            self.gui.macros["ZSMIN_SOFT_LIMIT"] = float(self.gui.macros["ZSMIN_HARD_LIMIT"])
            self.gui.macros["ZSMAX_SOFT_LIMIT"] = float(self.gui.macros["ZSMAX_HARD_LIMIT"])
            self.gui.macros["XOMIN_SOFT_LIMIT"] = float(self.gui.macros["XOMIN_HARD_LIMIT"])
            self.gui.macros["XOMAX_SOFT_LIMIT"] = float(self.gui.macros["XOMAX_HARD_LIMIT"])
            self.gui.macros["YOMIN_SOFT_LIMIT"] = float(self.gui.macros["YOMIN_HARD_LIMIT"])
            self.gui.macros["YOMAX_SOFT_LIMIT"] = float(self.gui.macros["YOMAX_HARD_LIMIT"])
            self.gui.macros["ZOMIN_SOFT_LIMIT"] = float(self.gui.macros["ZOMIN_HARD_LIMIT"])
            self.gui.macros["ZOMAX_SOFT_LIMIT"] = float(self.gui.macros["ZOMAX_HARD_LIMIT"])

        elif buttonID == 1:
            # Set soft limits to hard limits.
            self.gui.macros["XSMIN_SOFT_LIMIT"] = float(0)
            self.gui.macros["XSMAX_SOFT_LIMIT"] = float(0)
            self.gui.macros["YSMIN_SOFT_LIMIT"] = float(0)
            self.gui.macros["YSMAX_SOFT_LIMIT"] = float(0)
            self.gui.macros["ZSMIN_SOFT_LIMIT"] = float(0)
            self.gui.macros["ZSMAX_SOFT_LIMIT"] = float(0)
            self.gui.macros["XOMIN_SOFT_LIMIT"] = float(0)
            self.gui.macros["XOMAX_SOFT_LIMIT"] = float(0)
            self.gui.macros["YOMIN_SOFT_LIMIT"] = float(0)
            self.gui.macros["YOMAX_SOFT_LIMIT"] = float(0)
            self.gui.macros["ZOMIN_SOFT_LIMIT"] = float(0)
            self.gui.macros["ZOMAX_SOFT_LIMIT"] = float(0)

        else:
            # Set soft limits to inputted values
            for object in ["S", "O"]:
                for axis in ["X", "Y", "Z"]:

                    offset = self._offset(object, axis, True)

                    min = float(softLimits[(object, axis, 0)].text()) + offset
                    max = float(softLimits[(object, axis, 1)].text()) + offset

                    if min < self.gui.macros[f"{axis}{object}MIN_HARD_LIMIT"]:
                        self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"] = float(self.gui.macros[f"{axis}{object}MIN_HARD_LIMIT"])
                    else:
                        self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"] = min

                    if max > self.gui.macros[f"{axis}{object}MAX_HARD_LIMIT"]:
                        self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"] = float(self.gui.macros[f"{axis}{object}MAX_HARD_LIMIT"])
                    else:
                        self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"] = max

        # Update soft limit line edits.
        self.gui.tab.xSMin.setText(str(self.gui.macros["XSMIN_SOFT_LIMIT"] - self._offset("S", "X", True)))
        self.gui.tab.xSMax.setText(str(self.gui.macros["XSMAX_SOFT_LIMIT"] - self._offset("S", "X", True)))
        self.gui.tab.ySMin.setText(str(self.gui.macros["YSMIN_SOFT_LIMIT"] - self._offset("S", "Y", True)))
        self.gui.tab.ySMax.setText(str(self.gui.macros["YSMAX_SOFT_LIMIT"] - self._offset("S", "Y", True)))
        self.gui.tab.zSMin.setText(str(self.gui.macros["ZSMIN_SOFT_LIMIT"] - self._offset("S", "Z", True)))
        self.gui.tab.zSMax.setText(str(self.gui.macros["ZSMAX_SOFT_LIMIT"] - self._offset("S", "Z", True)))
        self.gui.tab.xOMin.setText(str(self.gui.macros["XOMIN_SOFT_LIMIT"] - self._offset("O", "X", True)))
        self.gui.tab.xOMax.setText(str(self.gui.macros["XOMAX_SOFT_LIMIT"] - self._offset("O", "X", True)))
        self.gui.tab.yOMin.setText(str(self.gui.macros["YOMIN_SOFT_LIMIT"] - self._offset("O", "Y", True)))
        self.gui.tab.yOMax.setText(str(self.gui.macros["YOMAX_SOFT_LIMIT"] - self._offset("O", "Y", True)))
        self.gui.tab.zOMin.setText(str(self.gui.macros["ZOMIN_SOFT_LIMIT"] - self._offset("O", "Z", True)))
        self.gui.tab.zOMax.setText(str(self.gui.macros["ZOMAX_SOFT_LIMIT"] - self._offset("O", "Z", True)))

        # Update soft limit indicators.
        self._soft_lim_indicators("S", "X")
        self._soft_lim_indicators("S", "Y")
        self._soft_lim_indicators("S", "Z")
        self._soft_lim_indicators("O", "X")
        self._soft_lim_indicators("O", "Y")
        self._soft_lim_indicators("O", "Z")

        # Move motors to within soft limits.
        self._check_motor_position()

        self._append_text(f"Updating soft limits.")

    def _update_BL(self) -> None:
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

        # Reset backlash line edits for consistent formatting.
        self.gui.tab.xSB.setText(str(caget(self.gui.macros["XSB"])))
        self.gui.tab.ySB.setText(str(caget(self.gui.macros["YSB"])))
        self.gui.tab.zSB.setText(str(caget(self.gui.macros["ZSB"])))
        self.gui.tab.xOB.setText(str(caget(self.gui.macros["XOB"])))
        self.gui.tab.yOB.setText(str(caget(self.gui.macros["YOB"])))
        self.gui.tab.zOB.setText(str(caget(self.gui.macros["ZOB"])))

        self._append_text("Updating backlash values.")

    def _zero(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"]) -> None:
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
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos, ("S", "Y"): self.gui.ySAbsPos,
                    ("O", "Y"): self.gui.yOAbsPos, ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        # Update the base and relative positions.
        self.gui.macros[f"{axis}{object}_BASE_POSITION"] += self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"]
        self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"] = 0

        # Update absolute position line edit widget to 0.
        lineEdit[(object, axis)].setText(str(float(0)))

        self._change_display_vals()

        self._append_text(f"Zero'ing the {axis}{object}ABSPOS line edit.")

    def _motor_status(self, **kwargs: Union[str, int, float]) -> None:
        """Check and set motor status indicators.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `_motor_status`: refer to PyEpics documentation
            for a list of all possible arguments for PV callback functions.

        Returns
        -------
        None
        """
        motionLabels = {("S", "X"): self.gui.xIdleS,
                        ("S", "Y"): self.gui.yIdleS,
                        ("S", "Z"): self.gui.zIdleS,
                        ("O", "X"): self.gui.xIdleO,
                        ("O", "Y"): self.gui.yIdleO,
                        ("O", "Z"): self.gui.zIdleO}

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
            self._soft_lim_indicators(object, axis)
        elif value == 1:
            motionLabels[(object, axis)].setText("POWERING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #ff4747; border: 1px solid black;")
        elif value == 2:
            motionLabels[(object, axis)].setText("POWERED")
            motionLabels[(object, axis)].setStyleSheet("background-color: #ff4747; border: 1px solid black;")
        elif value == 3:
            motionLabels[(object, axis)].setText("RELEASING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #edde07; border: 1px solid black;")
            self._soft_lim_indicators(object, axis)
        elif value == 4:
            motionLabels[(object, axis)].setText("ACTIVE")
            motionLabels[(object, axis)].setStyleSheet("background-color: #3ac200; border: 1px solid black;")
        elif value == 5:
            motionLabels[(object, axis)].setText("APPLYING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #edde07; border: 1px solid black;")
            self._soft_lim_indicators(object, axis)
        else:
            motionLabels[(object, axis)].setText("UNPOWERING")
            motionLabels[(object, axis)].setStyleSheet("background-color: #ff4747; border: 1px solid black;")

        basePos = self.gui.macros[f"{axis}{object}_BASE_POSITION"]
        absPos = caget(self.gui.macros[f"{axis}{object}ABSPOS"])
        self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"] = absPos - basePos

        lineEdit[(object, axis)].setText(str(absPos - basePos + self._offset(object, axis)))

    def _check_motor_position(self) -> None:
        """Moves motors within soft limits.

        This method checkes each motors position. If a motor is out of the soft
        limits, it will be moved to the closes limit.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
                NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

                basePos = self.gui.macros[f"{axis}{object}_BASE_POSITION"]
                currPos = caget(self.gui.macros[f"{axis}{object}POS"])

                if currPos > PSL:
                    relPos = PSL - basePos
                    caput(self.gui.macros[f"{axis}{object}ABSPOS"], PSL)
                    caput(self.gui.macros[f"{axis}{object}MOVE"], 1)
                    caput(self.gui.macros[f"{axis}{object}MOVE"], 0)
                elif currPos < NSL:
                    relPos = NSL - basePos
                    caput(self.gui.macros[f"{axis}{object}ABSPOS"], NSL)
                    caput(self.gui.macros[f"{axis}{object}MOVE"], 1)
                    caput(self.gui.macros[f"{axis}{object}MOVE"], 0)

                self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"] = relPos

    def _hard_lim_indicators(self, **kwargs: Union[str, int, float]) -> None:
        """Set hard limit indicators.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `_hard_lim_indicators`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        
        Returns
        -------
        None
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

        self._append_text("Setting hard limit indicators.")

    def _soft_lim_indicators(self, object: Literal["S", "O"], axis: Literal["X", "Y", "Z"]) -> None:
        """Set soft limit indicators.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `_hard_lim_indicators`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        
        Returns
        -------
        None
        """
        softLimits = {("S", "X", 0): self.gui.xSSn, ("S", "X", 1): self.gui.xSSp,
                      ("S", "Y", 0): self.gui.ySSn, ("S", "Y", 1): self.gui.ySSp,
                      ("S", "Z", 0): self.gui.zSSn, ("S", "Z", 1): self.gui.zSSp,
                      ("O", "X", 0): self.gui.xOSn, ("O", "X", 1): self.gui.xOSp,
                      ("O", "Y", 0): self.gui.yOSn, ("O", "Y", 1): self.gui.yOSp,
                      ("O", "Z", 0): self.gui.zOSn, ("O", "Z", 1): self.gui.zOSp}

        value = caget(self.gui.macros[f"{axis}{object}POS"])
        minSoftLim = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]
        maxSoftLim = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]

        # Set maximum soft limit indicator.
        if maxSoftLim <= value:
            softLimits[(object, axis, 1)].setStyleSheet("background-color: #3ac200; border: 1px solid black;")
        else:
            softLimits[(object, axis, 1)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        # Set minimum soft limit indicator.
        if value <= minSoftLim:
            softLimits[(object, axis, 0)].setStyleSheet("background-color: #3ac200; border: 1px solid black;")
        else:
            softLimits[(object, axis, 0)].setStyleSheet("background-color: lightgrey; border: 1px solid black;")

        self._append_text("Setting soft limit indicators.")

    def _change_display_vals(self) -> None:
        """Switch displayed values between actual and relative values.

        This method changes all position based line edits and labels between
        actual values and relative values where relative values are taken with
        reference to the zeroed position.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        lineEdit = {("S", "X"): self.gui.xSAbsPos, ("O", "X"): self.gui.xOAbsPos,
                    ("S", "Y"): self.gui.ySAbsPos, ("O", "Y"): self.gui.yOAbsPos,
                    ("S", "Z"): self.gui.zSAbsPos, ("O", "Z"): self.gui.zOAbsPos}

        hardLimits = {("S", "X"): self.gui.tab.xSMM, ("O", "X"): self.gui.tab.xOMM,
                      ("S", "Y"): self.gui.tab.ySMM, ("O", "Y"): self.gui.tab.yOMM,
                      ("S", "Z"): self.gui.tab.zSMM, ("O", "Z"): self.gui.tab.zOMM}

        softLimits = {("S", "X", 0): self.gui.tab.xSMin, ("S", "X", 1): self.gui.tab.xSMax,
                      ("S", "Y", 0): self.gui.tab.ySMin, ("S", "Y", 1): self.gui.tab.ySMax,
                      ("S", "Z", 0): self.gui.tab.zSMin, ("S", "Z", 1): self.gui.tab.zSMax,
                      ("O", "X", 0): self.gui.tab.xOMin, ("O", "X", 1): self.gui.tab.xOMax,
                      ("O", "Y", 0): self.gui.tab.yOMin, ("O", "Y", 1): self.gui.tab.yOMax,
                      ("O", "Z", 0): self.gui.tab.zOMin, ("O", "Z", 1): self.gui.tab.zOMax}

        currentStep = {("S", "X"): self.gui.xStepS, ("O", "X"): self.gui.xStepO,
                       ("S", "Y"): self.gui.yStepS, ("O", "Y"): self.gui.yStepO,
                       ("S", "Z"): self.gui.zStepS, ("O", "Z"): self.gui.zStepO}
        
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:

                # Change absolute position line edit.
                relPos = self.gui.macros[f"{axis}{object}_RELATIVE_POSITION"]
                lineEdit[(object, axis)].setText(str(relPos + self._offset(object, axis)))

                offset = self._offset(object, axis, True)

                # Change hard limit displays.
                minLim = self.gui.macros[f"{axis}{object}MIN_HARD_LIMIT"] - offset
                maxLim = self.gui.macros[f"{axis}{object}MAX_HARD_LIMIT"] - offset
                hardLimits[(object, axis)].setText(f"{minLim} to {maxLim}")

                # Change soft limit line edits.
                minLim = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"] - offset
                maxLim = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"] - offset
                softLimits[(object, axis, 0)].setText(str(minLim))
                softLimits[(object, axis, 1)].setText(str(maxLim))

                # Change current step line edit.
                value = caget(self.gui.macros[f"{axis}{object}POS"])
                currentStep[(object, axis)].setText(f"<b>{value - offset} STEPS</b>")

    def _set_current_position(self, **kwargs: Union[str, int, float]) -> None:
        """Update current position label.

        Parameters
        ----------
        **kwargs : Dict
            Extra arguments to `_hard_lim_indicators`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        
        Returns
        -------
        None
        """
        stepLineEdit = {("S", "X"): self.gui.xStepS, ("O", "X"): self.gui.xStepO,
                        ("S", "Y"): self.gui.yStepS, ("O", "Y"): self.gui.yStepO,
                        ("S", "Z"): self.gui.zStepS, ("O", "Z"): self.gui.zStepO}

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        offset = self._offset(object, axis, True)

        stepText = f"<b>{value - offset} STEPS</b>"
        stepLineEdit[(object, axis)].setText(stepText)

    def _append_text(self, text):
        """
        """
        self.gui.textWindow.append(text)
        maxVal = self.tb.verticalScrollBar().maximum()
        self.gui.textWindow.verticalScrollBar().setValue(maxVal)

    def _print_globals(self) -> None:
        """Display all global variables.

        Parameters
        ----------
        None

        Returns
        -------
        None     
        """
        self._append_text("-*- GLOBAL VARIABLES - START -*-")

        keys = list(self.gui.macros.keys())
        for key in keys:
            self._append_text(f"{key} -> {self.gui.macros[key]}")

        self._append_text("-*- GLOBAL VARIABLES - END -*-")
