"""Create widgets interactive nature.

The controller module brings life to the GUI defined through the gui module by
connecting widgets up to control sequences that bring about change.
"""


# Import package dependencies.
from functools import partial
from PyQt5.QtGui import QColor
from thorlabs_apt import Motor
from epics import ca, caput, PV
from typing import Literal, Any, Dict
from PyQt5.QtWidgets import QLineEdit, QFileDialog

# Import file dependencies.
from gui import GUI
from thorlabs_motor_control import enable, disable, home, changeMode
from configuration import load_config, save_config, save_pos_config

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
    PV_XSSTEP : PV
        Step PV for the sample's x dimension.
    PV_YSSTEP : PV
        Step PV for the sample's y dimension.
    PV_ZSSTEP : PV
        Step PV for the sample's z dimension.
    PV_XOSTEP : PV
        Step PV for the objective's x dimension.
    PV_YOSTEP : PV
        Step PV for the objective's y dimension.
    PV_ZOSTEP : PV
        Step PV for the objective's z dimension.
    PV_XSABSPOS : PV
        Absolute position PV for the sample's x dimension.
    PV_YSABSPOS : PV
        Absolute position PV for the sample's y dimension.
    PV_ZSABSPOS : PV
        Absolute position PV for the sample's z dimension.
    PV_XOABSPOS : PV
        Absolute position PV for the objective's x dimension.
    PV_YOABSPOS : PV
        Absolute position PV for the objective's y dimension.
    PV_ZOABSPOS : PV
        Absolute position PV for the objective's z dimension.
    PV_XSPOS : PV
        Current position PV for the sample's x dimension.
    PV_YSPOS : PV
        Current position PV for the sample's y dimension.
    PV_ZSPOS : PV
        Current position PV for the sample's z dimension.
    PV_XOPOS : PV
        Current position PV for the objective's x dimension.
    PV_YOPOS : PV
        Current position PV for the objective's y dimension.
    PV_ZOPOS : PV
        Current position PV for the objective's z dimension.
    PV_XSPOS_ABS : PV
        Absolute current position PV for the sample's x dimension.
    PV_YSPOS_ABS : PV
        Absolute current position PV for the sample's y dimension.
    PV_ZSPOS_ABS : PV
        Absolute current position PV for the sample's z dimension.
    PV_XOPOS_ABS : PV
        Absolute current position PV for the objective's x dimension.
    PV_YOPOS_ABS : PV
        Absolute current position PV for the objective's y dimension.
    PV_ZOPOS_ABS : PV
        Absolute current position PV for the objective's z dimension.
    PV_XSMOVE : PV
        Move PV of the sample's x dimension.
    PV_YSMOVE : PV
        Move PV of the sample's y dimension.
    PV_ZSMOVE : PV
        Move PV of the sample's z dimension.
    PV_XOMOVE : PV
        Move PV of the objective's x dimension.
    PV_YOMOVE : PV
        Move PV of the objective's y dimension.
    PV_ZOMOVE : PV
        Move PV of the objective's z dimension.
    PV_XSSTOP : PV
        Stop PV for the sample's x dimension.
    PV_YSSTOP : PV
        Stop PV for the sample's y dimension.
    PV_ZSSTOP : PV
        Stop PV for the sample's z dimension.
    PV_XOSTOP : PV
        Stop PV for the objective's x dimension.
    PV_YOSTOP : PV
        Stop PV for the objective's y dimension.
    PV_ZOSTOP : PV
        Stop PV for the objective's z dimension.
    PV_XSHN : PV
        Negative hard limit PV for the sample's x dimension.
    PV_XSHP : PV
        Positive hard limit PV for the sample's x dimension.
    PV_YSHN : PV
        Negative hard limit PV for the sample's y dimension.
    PV_YSHP : PV
        Positive hard limit PV for the sample's y dimension.
    PV_ZSHN : PV
        Negative hard limit PV for the sample's z dimension.
    PV_ZSHP : PV
        Positive hard limit PV for the sample's z dimension.
    PV_XOHN : PV
        Negative hard limit PV for the objective's x dimension.
    PV_XOHP : PV
        Positive hard limit PV for the objective's x dimension.
    PV_YOHN : PV
        Negative hard limit PV for the objective's y dimension.
    PV_YOHP : PV
        Positive hard limit PV for the objective's y dimension.
    PV_ZOHN : PV
        Negative hard limit PV for the objective's z dimension.
    PV_ZOHP : PV
        Positive hard limit PV for the objective's z dimension.
    PV_XSSTATE : PV
        State PV of the sample's x dimension.
    PV_YSSTATE : PV
        State PV of the sample's y dimension.
    PV_ZSSTATE : PV
        State PV of the sample's z dimension.
    PV_XOSTATE : PV
        State PV of the objective's x dimension.
    PV_YOSTATE : PV
        State PV of the objective's y dimension.
    PV_ZOSTATE : PV
        State PV of the objective's z dimension.
    PV_XSOFFSET : PV
        Offset PV for the sample's x dimension
    PV_YSOFFSET : PV
        Offset PV for the sample's y dimension
    PV_ZSOFFSET : PV
        Offset PV for the sample's z dimension
    PV_XOOFFSET : PV
        Offset PV for the objective's x dimension
    PV_YOOFFSET : PV
        Offset PV for the objective's y dimension
    PV_ZOOFFSET : PV
        Offset PV for the objective's z dimension

    Methods
    -------
    _initialize_PVs()
        Initialize GUI PVs.
    _initialize_GUI()
        Initialize GUI displays.
    _connect_signals()
        Connect the widgets to a control sequence.
    _mode_state(mode, modeMotor)
        Control sequence to change the microscope mode.
    _mode_position(mode)
        Change Mode position settings.
    _enable_thorlabs()
        Control sequence to enable the THORLABS motor.
    _home_thorlabs()
        Control sequence to home the THORLABS motor.
    _increment(object, axis, direction, step)
        Control sequence to increment sample and objective stage motors.
    _absolute(object, axis, pos)
        Control sequence to move the sample and objective stage motors to a
        set point.
    _continuous(object, axis, type)
        Control sequence for the continuous motion of the sample and objective
        stages.
    _update_abs_pos(**kwargs)
        Control sequence to update the absolute position line edit widget.
    _update_soft_lim(buttonID)
        Control sequence to set soft limits to the inputted soft limits.
    _update_BL()
        Control sequence to update backlash values.
    _motor_status(**kwargs)
        Control sequence to check and set mode status indicators.
    _check_motor_position()
        Control sequence to move motors within soft limits.
    _soft_lim_indicators(object, axis)
        Control sequence to set doft limit indicators.
    _hard_lim_indicators(**kwargs)
        Control sequence to set hard limit indicators.
    _change_display_vals()
        Callback function to switch displayed values between actual and
        relative values.
    _change_to_actual()
        Control sequence to change display values to actual.
    _change_to_relative()
        Control sequence to change display values to relative.
    _zero(object, axis)
        Control sequence to zero the current motor positions.
    _actual(object, axis)
        Control sequence to zero the current motor offset.
    _set_current_position(**kwargs)
        Control sequence to update current position labels.
    _append_text(text, color)
        Control sequence to append text to the user information display.
    _load_config()
        Control sequence to upload a new configuration.
    _save_config()
        Control sequence to save the current configuration.
    _change_units()
        Control sequence to change the `current position` display's units.
    _save_position()
        Control sequence to save the current motor positions.
    _load_position()
        Control sequence to load the selected motor position.
    _delete_position()
        Control sequence to delete the selected motor position.
    _clear_position()
        Control sequence to clear all saved motor positions.
    """

    def __init__(self, gui: GUI, modeMotor: Motor) -> None:
        """Initialize the Controller."""

        self.gui = gui
        self.modeMotor = modeMotor

        self._initialize_PVs()
        self._initialize_GUI()
        self._connect_signals()

    def _initialize_PVs(self) -> None:
        """Conigure GUI PV's."""

        # Conigure step PV.
        self.PV_XSSTEP = PV(pvname=self.gui.macros["XSSTEP"])
        self.PV_YSSTEP = PV(pvname=self.gui.macros["YSSTEP"])
        self.PV_ZSSTEP = PV(pvname=self.gui.macros["ZSSTEP"])
        self.PV_XOSTEP = PV(pvname=self.gui.macros["XOSTEP"])
        self.PV_YOSTEP = PV(pvname=self.gui.macros["YOSTEP"])
        self.PV_ZOSTEP = PV(pvname=self.gui.macros["XOSTEP"])

        # # Set absolute position PV monitoring and callback.
        # self.PV_XSABSPOS = PV(pvname=self.gui.macros["XSABSPOS"],
        #                       auto_monitor=True, callback=self._update_abs_pos)
        # self.PV_YSABSPOS = PV(pvname=self.gui.macros["YSABSPOS"],
        #                       auto_monitor=True, callback=self._update_abs_pos)
        # self.PV_ZSABSPOS = PV(pvname=self.gui.macros["ZSABSPOS"],
        #                       auto_monitor=True, callback=self._update_abs_pos)
        # self.PV_XOABSPOS = PV(pvname=self.gui.macros["XOABSPOS"],
        #                       auto_monitor=True, callback=self._update_abs_pos)
        # self.PV_YOABSPOS = PV(pvname=self.gui.macros["YOABSPOS"],
        #                       auto_monitor=True, callback=self._update_abs_pos)
        # self.PV_ZOABSPOS = PV(pvname=self.gui.macros["ZOABSPOS"],
        #                       auto_monitor=True, callback=self._update_abs_pos)

        # Set current position PV monitoring and callback.
        self.PV_XSPOS = PV(pvname=self.gui.macros["XSPOS"], auto_monitor=True,
                           callback=self._set_current_position)
        self.PV_YSPOS = PV(pvname=self.gui.macros["YSPOS"], auto_monitor=True,
                           callback=self._set_current_position)
        self.PV_ZSPOS = PV(pvname=self.gui.macros["ZSPOS"], auto_monitor=True,
                           callback=self._set_current_position)
        self.PV_XOPOS = PV(pvname=self.gui.macros["XOPOS"], auto_monitor=True,
                           callback=self._set_current_position)
        self.PV_YOPOS = PV(pvname=self.gui.macros["YOPOS"], auto_monitor=True,
                           callback=self._set_current_position)
        self.PV_ZOPOS = PV(pvname=self.gui.macros["ZOPOS"], auto_monitor=True,
                           callback=self._set_current_position)

        # Initialize current absolute position PV's.
        self.PV_XSPOS_ABS = PV(pvname=self.gui.macros["XSPOS_ABS"])
        self.PV_YSPOS_ABS = PV(pvname=self.gui.macros["YSPOS_ABS"])
        self.PV_ZSPOS_ABS = PV(pvname=self.gui.macros["ZSPOS_ABS"])
        self.PV_XOPOS_ABS = PV(pvname=self.gui.macros["XOPOS_ABS"])
        self.PV_YOPOS_ABS = PV(pvname=self.gui.macros["YOPOS_ABS"])
        self.PV_ZOPOS_ABS = PV(pvname=self.gui.macros["ZOPOS_ABS"])

        # Initialize move PV's.
        self.PV_XSMOVE = PV(pvname=self.gui.macros["XSMOVE"])
        self.PV_YSMOVE = PV(pvname=self.gui.macros["YSMOVE"])
        self.PV_ZSMOVE = PV(pvname=self.gui.macros["ZSMOVE"])
        self.PV_XOMOVE = PV(pvname=self.gui.macros["XOMOVE"])
        self.PV_YOMOVE = PV(pvname=self.gui.macros["YOMOVE"])
        self.PV_ZOMOVE = PV(pvname=self.gui.macros["ZOMOVE"])

        # Configure emergency stop PVs.
        self.PV_XSSTOP = PV(pvname=self.gui.macros["XSSTOP"])
        self.PV_YSSTOP = PV(pvname=self.gui.macros["YSSTOP"])
        self.PV_ZSSTOP = PV(pvname=self.gui.macros["ZSSTOP"])
        self.PV_XOSTOP = PV(pvname=self.gui.macros["XOSTOP"])
        self.PV_YOSTOP = PV(pvname=self.gui.macros["YOSTOP"])
        self.PV_ZOSTOP = PV(pvname=self.gui.macros["ZOSTOP"])

        # Set hard limit position PV monitoring and callback.
        self.PV_XSHN = PV(pvname=self.gui.macros["XSHN"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_XSHP = PV(pvname=self.gui.macros["XSHP"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_YSHN = PV(pvname=self.gui.macros["YSHN"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_YSHP = PV(pvname=self.gui.macros["YSHP"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_ZSHN = PV(pvname=self.gui.macros["ZSHN"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_ZSHP = PV(pvname=self.gui.macros["ZSHP"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_XOHN = PV(pvname=self.gui.macros["XOHN"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_XOHP = PV(pvname=self.gui.macros["XOHP"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_YOHN = PV(pvname=self.gui.macros["YOHN"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_YOHP = PV(pvname=self.gui.macros["YOHP"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_ZOHN = PV(pvname=self.gui.macros["ZOHN"], auto_monitor=True,
                          callback=self._hard_lim_indicators)
        self.PV_ZOHP = PV(pvname=self.gui.macros["ZOHP"], auto_monitor=True,
                          callback=self._hard_lim_indicators)

        # Set state PV monitoring and callback.
        self.PV_XSSTATE = PV(pvname=self.gui.macros["XSSTATE"],
                             auto_monitor=True, callback=self._motor_status)
        self.PV_YSSTATE = PV(pvname=self.gui.macros["YSSTATE"],
                             auto_monitor=True, callback=self._motor_status)
        self.PV_ZSSTATE = PV(pvname=self.gui.macros["ZSSTATE"],
                             auto_monitor=True, callback=self._motor_status)
        self.PV_XOSTATE = PV(pvname=self.gui.macros["XOSTATE"],
                             auto_monitor=True, callback=self._motor_status)
        self.PV_YOSTATE = PV(pvname=self.gui.macros["YOSTATE"],
                             auto_monitor=True, callback=self._motor_status)
        self.PV_ZOSTATE = PV(pvname=self.gui.macros["ZOSTATE"],
                             auto_monitor=True, callback=self._motor_status)

        # Initialize offset PV monitoring and callback.
        self.PV_XSOFFSET = PV(pvname=self.gui.macros["XSOFFSET"],
                              auto_monitor=True,
                              callback=self._change_display_vals)
        self.PV_YSOFFSET = PV(pvname=self.gui.macros["YSOFFSET"],
                              auto_monitor=True,
                              callback=self._change_display_vals)
        self.PV_ZSOFFSET = PV(pvname=self.gui.macros["ZSOFFSET"],
                              auto_monitor=True,
                              callback=self._change_display_vals)
        self.PV_XOOFFSET = PV(pvname=self.gui.macros["XOOFFSET"],
                              auto_monitor=True,
                              callback=self._change_display_vals)
        self.PV_YOOFFSET = PV(pvname=self.gui.macros["YOOFFSET"],
                              auto_monitor=True,
                              callback=self._change_display_vals)
        self.PV_ZOOFFSET = PV(pvname=self.gui.macros["ZOOFFSET"],
                              auto_monitor=True,
                              callback=self._change_display_vals)

        # Intialize backlash PV's.
        self.PV_XSB = PV(self.gui.macros["XSB"])
        self.PV_YSB = PV(self.gui.macros["YSB"])
        self.PV_ZSB = PV(self.gui.macros["ZSB"])
        self.PV_XOB = PV(self.gui.macros["XOB"])
        self.PV_YOB = PV(self.gui.macros["YOB"])
        self.PV_ZOB = PV(self.gui.macros["ZOB"])

        self._append_text("PVs configured and initialized.")

    def _initialize_GUI(self) -> None:
        """Configure GUI displays."""

        # Set THORLABS motor position line edits.
        self.gui.tab.TMTM.setText(
            str(float(self.gui.macros["TRANSMISSION_POSITION"])))
        self.gui.tab.TMRM.setText(
            str(float(self.gui.macros["REFLECTION_POSITION"])))
        self.gui.tab.TMVM.setText(
            str(float(self.gui.macros["VISIBLE_IMAGE_POSITION"])))
        self.gui.tab.TMBM.setText(
            str(float(self.gui.macros["BEAMSPLITTER_POSITION"])))

        # Set soft limit line edits.
        self.gui.tab.xSMin.setText(
            str(float(self.gui.macros["XSMIN_SOFT_LIMIT"])))
        self.gui.tab.xSMax.setText(
            str(float(self.gui.macros["XSMAX_SOFT_LIMIT"])))
        self.gui.tab.ySMin.setText(
            str(float(self.gui.macros["YSMIN_SOFT_LIMIT"])))
        self.gui.tab.ySMax.setText(
            str(float(self.gui.macros["YSMAX_SOFT_LIMIT"])))
        self.gui.tab.zSMin.setText(
            str(float(self.gui.macros["ZSMIN_SOFT_LIMIT"])))
        self.gui.tab.zSMax.setText(
            str(float(self.gui.macros["ZSMAX_SOFT_LIMIT"])))
        self.gui.tab.xOMin.setText(
            str(float(self.gui.macros["XOMIN_SOFT_LIMIT"])))
        self.gui.tab.xOMax.setText(
            str(float(self.gui.macros["XOMAX_SOFT_LIMIT"])))
        self.gui.tab.yOMin.setText(
            str(float(self.gui.macros["YOMIN_SOFT_LIMIT"])))
        self.gui.tab.yOMax.setText(
            str(float(self.gui.macros["YOMAX_SOFT_LIMIT"])))
        self.gui.tab.zOMin.setText(
            str(float(self.gui.macros["ZOMIN_SOFT_LIMIT"])))
        self.gui.tab.zOMax.setText(
            str(float(self.gui.macros["ZOMAX_SOFT_LIMIT"])))

        # Set all offset PV's to the saved offsets.
        self.PV_XSOFFSET.put(self.gui.macros["XS_OFFSET"])
        self.PV_YSOFFSET.put(self.gui.macros["YS_OFFSET"])
        self.PV_ZSOFFSET.put(self.gui.macros["ZS_OFFSET"])
        self.PV_XOOFFSET.put(self.gui.macros["XO_OFFSET"])
        self.PV_YOOFFSET.put(self.gui.macros["YO_OFFSET"])
        self.PV_ZOOFFSET.put(self.gui.macros["ZO_OFFSET"])

        # Set offset line edits to current PV values.
        self.gui.tab.xSOffset.setText(str(float(self.gui.macros["XS_OFFSET"])))
        self.gui.tab.ySOffset.setText(str(float(self.gui.macros["YS_OFFSET"])))
        self.gui.tab.zSOffset.setText(str(float(self.gui.macros["ZS_OFFSET"])))
        self.gui.tab.xOOffset.setText(str(float(self.gui.macros["XO_OFFSET"])))
        self.gui.tab.yOOffset.setText(str(float(self.gui.macros["YO_OFFSET"])))
        self.gui.tab.zOOffset.setText(str(float(self.gui.macros["ZO_OFFSET"])))

        # Set backlash PV values.
        self.PV_XSB.put(self.gui.macros["XS_BACKLASH"])
        self.PV_YSB.put(self.gui.macros["YS_BACKLASH"])
        self.PV_ZSB.put(self.gui.macros["ZS_BACKLASH"])
        self.PV_XOB.put(self.gui.macros["XO_BACKLASH"])
        self.PV_YOB.put(self.gui.macros["YO_BACKLASH"])
        self.PV_ZOB.put(self.gui.macros["ZO_BACKLASH"])

        # Set backlash line edits to current PV values.
        self.gui.tab.xSB.setText(str(float(self.gui.macros["XS_BACKLASH"])))
        self.gui.tab.ySB.setText(str(float(self.gui.macros["YS_BACKLASH"])))
        self.gui.tab.zSB.setText(str(float(self.gui.macros["ZS_BACKLASH"])))
        self.gui.tab.xOB.setText(str(float(self.gui.macros["XO_BACKLASH"])))
        self.gui.tab.yOB.setText(str(float(self.gui.macros["YO_BACKLASH"])))
        self.gui.tab.zOB.setText(str(float(self.gui.macros["ZO_BACKLASH"])))

        # Set step line edits to current PV values.
        self.gui.xSStep.setText(str(float(self.PV_XSSTEP.get())))
        self.gui.ySStep.setText(str(float(self.PV_YSSTEP.get())))
        self.gui.zSStep.setText(str(float(self.PV_ZSSTEP.get())))
        self.gui.xOStep.setText(str(float(self.PV_XOSTEP.get())))
        self.gui.yOStep.setText(str(float(self.PV_YOSTEP.get())))
        self.gui.zOStep.setText(str(float(self.PV_ZOSTEP.get())))

        # Make the absolute display align with the current position display.
        self.PV_XSABSPOS.put(self.PV_XSPOS.get())
        self.PV_YSABSPOS.put(self.PV_YSPOS.get())
        self.PV_ZSABSPOS.put(self.PV_ZSPOS.get())
        self.PV_XOABSPOS.put(self.PV_XOPOS.get())
        self.PV_YOABSPOS.put(self.PV_YOPOS.get())
        self.PV_ZOABSPOS.put(self.PV_ZOPOS.get())

        # Set absolute position line edits to current PV values.
        self.gui.xSAbsPos.setText(str(self.PV_XSABSPOS.get()))
        self.gui.ySAbsPos.setText(str(self.PV_YSABSPOS.get()))
        self.gui.zSAbsPos.setText(str(self.PV_ZSABSPOS.get()))
        self.gui.xOAbsPos.setText(str(self.PV_XOABSPOS.get()))
        self.gui.yOAbsPos.setText(str(self.PV_YOABSPOS.get()))
        self.gui.zOAbsPos.setText(str(self.PV_ZOABSPOS.get()))

        # Enable Thorlabs motor.
        enable(self.modeMotor)

        # Set soft limit indicators.
        self._soft_lim_indicators()

        self._append_text("Display values and macros initialized.")

    def _connect_signals(self) -> None:
        """Connect widgets and control sequences.

        This method connects each of the widgets on the gui with a control
        sequence to update the display or interface with hardware.
        """

        # Mode select functionality.
        self.gui.tab.RDM1.pressed.connect(partial(self._mode_state,
                                                  "TRANSMISSION_POSITION",
                                                  self.modeMotor))
        self.gui.tab.RDM2.pressed.connect(partial(self._mode_state,
                                                  "REFLECTION_POSITION",
                                                  self.modeMotor))
        self.gui.tab.RDM3.pressed.connect(partial(self._mode_state,
                                                  "VISIBLE_IMAGE_POSITION",
                                                  self.modeMotor))
        self.gui.tab.RDM4.pressed.connect(partial(self._mode_state,
                                                  "BEAMSPLITTER_POSITION",
                                                  self.modeMotor))

        # THORLABS/mode motor functionality.
        self.gui.tab.enableDisable.clicked.connect(self._enable_thorlabs)
        self.gui.tab.home.clicked.connect(self._home_thorlabs)

        # Mode position customizarion functionality.
        self.gui.tab.TMTMbutton.clicked.connect(
            partial(self._mode_position, "TRANSMISSION_POSITION"))
        self.gui.tab.TMRMbutton.clicked.connect(
            partial(self._mode_position, "REFLECTION_POSITION"))
        self.gui.tab.TMVMbutton.clicked.connect(
            partial(self._mode_position, "VISIBLE_IMAGE_POSITION"))
        self.gui.tab.TMBMbutton.clicked.connect(
            partial(self._mode_position, "BEAMSPLITTER_POSITION"))

        # Increment sample and objective stage functionality.
        self.gui.xSN.clicked.connect(
            partial(self._increment, "S", "X", "N", self.gui.xSStep))
        self.gui.xSP.clicked.connect(
            partial(self._increment, "S", "X", "P", self.gui.xSStep))
        self.gui.ySN.clicked.connect(
            partial(self._increment, "S", "Y", "N", self.gui.ySStep))
        self.gui.ySP.clicked.connect(
            partial(self._increment, "S", "Y", "P", self.gui.ySStep))
        self.gui.zSN.clicked.connect(
            partial(self._increment, "S", "Z", "N", self.gui.zSStep))
        self.gui.zSP.clicked.connect(
            partial(self._increment, "S", "Z", "P", self.gui.zSStep))
        self.gui.xON.clicked.connect(
            partial(self._increment, "O", "X", "N", self.gui.xOStep))
        self.gui.xOP.clicked.connect(
            partial(self._increment, "O", "X", "P", self.gui.xOStep))
        self.gui.yON.clicked.connect(
            partial(self._increment, "O", "Y", "N", self.gui.yOStep))
        self.gui.yOP.clicked.connect(
            partial(self._increment, "O", "Y", "P", self.gui.yOStep))
        self.gui.zON.clicked.connect(
            partial(self._increment, "O", "Z", "N", self.gui.zOStep))
        self.gui.zOP.clicked.connect(
            partial(self._increment, "O", "Z", "P", self.gui.zOStep))

        # Move sample and objective stage to absolute position functionality.
        self.gui.xSMove.clicked.connect(partial(self._absolute, "S", "X"))
        self.gui.ySMove.clicked.connect(partial(self._absolute, "S", "Y"))
        self.gui.zSMove.clicked.connect(partial(self._absolute, "S", "Z"))
        self.gui.xOMove.clicked.connect(partial(self._absolute, "O", "X"))
        self.gui.yOMove.clicked.connect(partial(self._absolute, "O", "Y"))
        self.gui.zOMove.clicked.connect(partial(self._absolute, "O", "Z"))

        # Continuous motion of the sample and objective stages functionality.
        self.gui.xSCn.clicked.connect(
            partial(self._continuous, "S", "X", "CN"))
        self.gui.xSStop.clicked.connect(
            partial(self._continuous, "S", "X", "STOP"))
        self.gui.xSCp.clicked.connect(
            partial(self._continuous, "S", "X", "CP"))
        self.gui.ySCn.clicked.connect(
            partial(self._continuous, "S", "Y", "CN"))
        self.gui.ySStop.clicked.connect(
            partial(self._continuous, "S", "Y", "STOP"))
        self.gui.ySCp.clicked.connect(
            partial(self._continuous, "S", "Y", "CP"))
        self.gui.zSCn.clicked.connect(
            partial(self._continuous, "S", "Z", "CN"))
        self.gui.zSStop.clicked.connect(
            partial(self._continuous, "S", "Z", "STOP"))
        self.gui.zSCp.clicked.connect(
            partial(self._continuous, "S", "Z", "CP"))
        self.gui.xOCn.clicked.connect(
            partial(self._continuous, "O", "X", "CN"))
        self.gui.xOStop.clicked.connect(
            partial(self._continuous, "O", "X", "STOP"))
        self.gui.xOCp.clicked.connect(
            partial(self._continuous, "O", "X", "CP"))
        self.gui.yOCn.clicked.connect(
            partial(self._continuous, "O", "Y", "CN"))
        self.gui.yOStop.clicked.connect(
            partial(self._continuous, "O", "Y", "STOP"))
        self.gui.yOCp.clicked.connect(
            partial(self._continuous, "O", "Y", "CP"))
        self.gui.zOCn.clicked.connect(
            partial(self._continuous, "O", "Z", "CN"))
        self.gui.zOStop.clicked.connect(
            partial(self._continuous, "O", "Z", "STOP"))
        self.gui.zOCp.clicked.connect(
            partial(self._continuous, "O", "Z", "CP"))

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

        # Zero'ing absolute position functionality.
        self.gui.tab.xSActual.clicked.connect(partial(self._actual, "S", "X"))
        self.gui.tab.ySActual.clicked.connect(partial(self._actual, "S", "Y"))
        self.gui.tab.zSActual.clicked.connect(partial(self._actual, "S", "Z"))
        self.gui.tab.xOActual.clicked.connect(partial(self._actual, "O", "X"))
        self.gui.tab.yOActual.clicked.connect(partial(self._actual, "O", "Y"))
        self.gui.tab.zOActual.clicked.connect(partial(self._actual, "O", "Z"))

        # Other functionality.
        self.gui.tab.SBL.clicked.connect(self._update_BL)
        self.gui.tab.allActual.clicked.connect(self._change_to_actual)
        self.gui.tab.zeroAll.clicked.connect(self._change_to_relative)
        self.gui.positionUnits.clicked.connect(self._change_units)

        # Load and save configuration functionality.
        self.gui.savePos.clicked.connect(self._save_position)
        self.gui.loadPos.clicked.connect(self._load_position)
        self.gui.deletePos.clicked.connect(self._delete_position)
        self.gui.clearPos.clicked.connect(self._clear_position)

        # Configuration functionality.
        self.gui.loadConfig.clicked.connect(self._load_config)
        self.gui.saveConfig.clicked.connect(self._save_config)

        self._append_text("Widgets connected to control sequences.")

    def _mode_state(self, mode: str, modeMotor: Motor) -> None:
        """Change microscope mode.

        This method is called when selecting a mode radio button to change
        the THORLABS motor to a different mode position.

        Parameters
        ----------
        mode : str
            Mode to move the THORLABS motor to.
        modeMotor : Motor Type
            Motor controlling the mode stage.
        """

        # Set move_to position based on mode.
        position = self.gui.macros[mode]
        status = changeMode(pos=position, modeMotor=modeMotor)

        if status == -1:
            self._append_text("ERROR: Can not change THORLABS motor position.",
                              QColor(255, 0, 0))
        else:
            self._append_text(f"Changing mode to {mode}.")

    def _mode_position(self, mode: str) -> None:
        """Change mode position settings.

        Parameters
        ----------
        mode : str
            The mode's position to be updated.
        """

        if mode == "TRANSMISSION_POSITION":
            pos_line_edit = self.gui.tab.TMTM
            radio_select = self.gui.tab.RDM1.isChecked()
        elif mode == "REFLECTION_POSITION":
            pos_line_edit = self.gui.tab.TMRM
            radio_select = self.gui.tab.RDM2.isChecked()
        elif mode == "VISIBLE_IMAGE_POSITION":
            pos_line_edit = self.gui.tab.TMVM
            radio_select = self.gui.tab.RDM3.isChecked()
        elif mode == "BEAMSPLITTER_POSITION":
            pos_line_edit = self.gui.tab.TMBM
            radio_select = self.gui.tab.RDM4.isChecked()
        
        self.gui.macros[mode] = float(pos_line_edit.text())
        pos_line_edit.setText(str(self.gui.macros[mode]))

        if radio_select:
            self._mode_state(mode, self.modeMotor)

        self._append_text("Setting new mode position.")

    def _enable_thorlabs(self) -> None:
        """Enable or disable the THORLABS motor."""

        label = self.gui.tab.enableDisable.text()

        if label == "Enable":
            enable(self.modeMotor)

            self.gui.tab.enableDisable.setText("Disable")
            self._append_text("THORLABS motor enabled.")
        else:
            disable(self.modeMotor)

            self.gui.tab.enableDisable.setText("Enable")
            self._append_text("THORLABS motor disabled.")

    def _home_thorlabs(self) -> None:
        """Home the THORLABS motor."""

        try:
            home(self.modeMotor)
            self.gui.tab.group.setExclusive(False)
            self.gui.tab.RDM1.setChecked(False)
            self.gui.tab.RDM2.setChecked(False)
            self.gui.tab.RDM3.setChecked(False)
            self.gui.tab.RDM4.setChecked(False)
            self.gui.tab.group.setExclusive(True)

            self._append_text("THORLABS motor homing.")
        except:
            self._append_text("ERROR: THORLABS motor cannot be homed, ensure the motor is enabled.",
                              QColor(255, 0, 0))

    def _increment(self, object: Literal["S", "O"], axis:
                   Literal["X", "Y", "Z"], direction: Literal["N", "P"], step:
                   QLineEdit) -> None:
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
        """

        absPos = self.__dict__[f"PV_{axis}{object}POS_ABS"].get()
        incPos = float(step.text())

        if incPos < 0:
            incPos = -incPos
            step.setText(str(incPos))
            self._append_text("WARNING: Step must be positive. Step sign has been changed to positive.",
                              QColor(250, 215, 0))

        PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

        if direction == "P" and absPos + incPos > PSL:
            incPos = PSL - absPos
        elif direction == "N" and absPos - incPos < NSL:
            incPos = absPos - NSL

        self.__dict__[f"PV_{axis}{object}STEP"].put(incPos)
        caput(self.gui.macros[f"{axis}{object}{direction}"], 1)

    def _absolute(self, object: Literal["S", "O"], axis:
                  Literal["X", "Y", "Z"]) -> None:
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
        """

        absPosLineEdit = self.__dict__["gui"].__dict__[f"{axis.lower()}{object}AbsPos"]
        absPos = float(absPosLineEdit.text())
        absPosLineEdit.setText(str(absPos))

        PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

        if absPos > PSL:
            absPos = PSL
        elif absPos < NSL:
            absPos = NSL

        self.__dict__[f"PV_{axis}{object}ABSPOS"].put(absPos)
        self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
        self.__dict__[f"PV_{axis}{object}MOVE"].put(0)

    def _continuous(self, object: Literal["S", "O"], axis:
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
        """

        if type == "CN":
            caput(self.gui.macros[f"{axis}{object}CN"],
                  self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"])
        elif type == "CP":
            caput(self.gui.macros[f"{axis}{object}CP"],
                  self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"])
        else:
            self.__dict__[f"PV_{axis}{object}STOP"].put(1)
            self.__dict__[f"PV_{axis}{object}STOP"].put(0)

    # def _update_abs_pos(self, **kwargs: Dict[str, Any]) -> None:
    #     """Update absolute value line edit.

    #     Parameters
    #     ----------
    #     **kwargs : dict
    #         Extra arguments to `_update_abs_pos`: refer to PyEpics
    #         documentation for a list of all possible arguments for PV callback
    #         functions.
    #     """

    #     pvname = kwargs["pvname"]
    #     value = kwargs["value"]

    #     keys = list(self.gui.macros.keys())
    #     vals = list(self.gui.macros.values())
    #     pvKey = keys[vals.index(pvname)]

    #     axis = pvKey[0]
    #     object = pvKey[1]

    #     self.__dict__["gui"].__dict__[f"{axis.lower()}{object}AbsPos"].setText(str(value))

    def _update_soft_lim(self, buttonID: Literal[0, 1]) -> None:
        """Update sample and objective soft limits.

        This method updates the programs soft limits to the inputted amounts or
        extreme limits dependent on 'buttonID'.

        Parameters
        ----------
        buttonID : {0, 1}
            Integer representing the button pressed as being either SSL or SESL
            using a 0 or 1, respectively.
        """

        if buttonID == 2:
            # Set soft limits to hard limits.
            self.gui.macros["XSMIN_SOFT_LIMIT"] = float(
                self.gui.macros["XSMIN_HARD_LIMIT"])
            self.gui.macros["XSMAX_SOFT_LIMIT"] = float(
                self.gui.macros["XSMAX_HARD_LIMIT"])
            self.gui.macros["YSMIN_SOFT_LIMIT"] = float(
                self.gui.macros["YSMIN_HARD_LIMIT"])
            self.gui.macros["YSMAX_SOFT_LIMIT"] = float(
                self.gui.macros["YSMAX_HARD_LIMIT"])
            self.gui.macros["ZSMIN_SOFT_LIMIT"] = float(
                self.gui.macros["ZSMIN_HARD_LIMIT"])
            self.gui.macros["ZSMAX_SOFT_LIMIT"] = float(
                self.gui.macros["ZSMAX_HARD_LIMIT"])
            self.gui.macros["XOMIN_SOFT_LIMIT"] = float(
                self.gui.macros["XOMIN_HARD_LIMIT"])
            self.gui.macros["XOMAX_SOFT_LIMIT"] = float(
                self.gui.macros["XOMAX_HARD_LIMIT"])
            self.gui.macros["YOMIN_SOFT_LIMIT"] = float(
                self.gui.macros["YOMIN_HARD_LIMIT"])
            self.gui.macros["YOMAX_SOFT_LIMIT"] = float(
                self.gui.macros["YOMAX_HARD_LIMIT"])
            self.gui.macros["ZOMIN_SOFT_LIMIT"] = float(
                self.gui.macros["ZOMIN_HARD_LIMIT"])
            self.gui.macros["ZOMAX_SOFT_LIMIT"] = float(
                self.gui.macros["ZOMAX_HARD_LIMIT"])

        elif buttonID == 1:
            # Set soft limits to zero.
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

                    offset = self.__dict__[f"PV_{axis}{object}OFFSET"].get()

                    tabDict = self.__dict__["gui"].__dict__["tab"].__dict__

                    min = float(tabDict[
                        f"{axis.lower()}{object}Min"].text()) - offset
                    max = float(tabDict[
                        f"{axis.lower()}{object}Max"].text()) - offset

                    if min > max:
                        self._append_text((f"WARNING: {axis}{object} soft ",
                                          "limits are invalid. Minimum ",
                                          "limits must be less then maximum ",
                                          "limits."), QColor(250, 215, 0))
                    else:
                        if min < self.gui.macros[f"{axis}{object}MIN_HARD_LIMIT"]:
                            self.gui.macros[
                                f"{axis}{object}MIN_SOFT_LIMIT"] = float(
                                    self.gui.macros[
                                        f"{axis}{object}MIN_HARD_LIMIT"])
                        else:
                            self.gui.macros[
                                f"{axis}{object}MIN_SOFT_LIMIT"] = min

                        if max > self.gui.macros[f"{axis}{object}MAX_HARD_LIMIT"]:
                            self.gui.macros[
                                f"{axis}{object}MAX_SOFT_LIMIT"] = float(
                                self.gui.macros[
                                    f"{axis}{object}MAX_HARD_LIMIT"])
                        else:
                            self.gui.macros[
                                f"{axis}{object}MAX_SOFT_LIMIT"] = max

        # Update soft limit line edits.
        self.gui.tab.xSMin.setText(str(self.gui.macros["XSMIN_SOFT_LIMIT"] +
                                       self.PV_XSOFFSET.get()))
        self.gui.tab.xSMax.setText(str(self.gui.macros["XSMAX_SOFT_LIMIT"] +
                                       self.PV_XSOFFSET.get()))
        self.gui.tab.ySMin.setText(str(self.gui.macros["YSMIN_SOFT_LIMIT"] +
                                       self.PV_YSOFFSET.get()))
        self.gui.tab.ySMax.setText(str(self.gui.macros["YSMAX_SOFT_LIMIT"] +
                                       self.PV_YSOFFSET.get()))
        self.gui.tab.zSMin.setText(str(self.gui.macros["ZSMIN_SOFT_LIMIT"] +
                                       self.PV_ZSOFFSET.get()))
        self.gui.tab.zSMax.setText(str(self.gui.macros["ZSMAX_SOFT_LIMIT"] +
                                       self.PV_ZSOFFSET.get()))
        self.gui.tab.xOMin.setText(str(self.gui.macros["XOMIN_SOFT_LIMIT"] +
                                       self.PV_XOOFFSET.get()))
        self.gui.tab.xOMax.setText(str(self.gui.macros["XOMAX_SOFT_LIMIT"] +
                                       self.PV_XOOFFSET.get()))
        self.gui.tab.yOMin.setText(str(self.gui.macros["YOMIN_SOFT_LIMIT"] +
                                       self.PV_YOOFFSET.get()))
        self.gui.tab.yOMax.setText(str(self.gui.macros["YOMAX_SOFT_LIMIT"] +
                                       self.PV_YOOFFSET.get()))
        self.gui.tab.zOMin.setText(str(self.gui.macros["ZOMIN_SOFT_LIMIT"] +
                                       self.PV_ZOOFFSET.get()))
        self.gui.tab.zOMax.setText(str(self.gui.macros["ZOMAX_SOFT_LIMIT"] +
                                       self.PV_ZOOFFSET.get()))

        # Move motors to within soft limits.
        self._check_motor_position()
        self._soft_lim_indicators()

        self._append_text("Updating soft limits.")

    def _update_BL(self) -> None:
        """Update backlash variables."""

        tabDict = self.__dict__["gui"].__dict__["tab"].__dict__

        # Set global backlash variables.
        self.gui.macros["XS_BACKLASH"] = abs(int(float(tabDict["xSB"].text())))
        self.gui.macros["YS_BACKLASH"] = abs(int(float(tabDict["ySB"].text())))
        self.gui.macros["ZS_BACKLASH"] = abs(int(float(tabDict["zSB"].text())))
        self.gui.macros["XO_BACKLASH"] = abs(int(float(tabDict["xOB"].text())))
        self.gui.macros["YO_BACKLASH"] = abs(int(float(tabDict["yOB"].text())))
        self.gui.macros["ZO_BACKLASH"] = abs(int(float(tabDict["zOB"].text())))

        # Set backlash PV's.
        self.PV_XSB.put(self.gui.macros["XS_BACKLASH"])
        self.PV_YSB.put(self.gui.macros["YS_BACKLASH"])
        self.PV_ZSB.put(self.gui.macros["ZS_BACKLASH"])
        self.PV_XOB.put(self.gui.macros["XO_BACKLASH"])
        self.PV_YOB.put(self.gui.macros["YO_BACKLASH"])
        self.PV_ZOB.put(self.gui.macros["ZO_BACKLASH"])

        # Reset backlash line edits for consistent formatting.
        self.gui.tab.xSB.setText(str(float(self.gui.macros["XS_BACKLASH"])))
        self.gui.tab.ySB.setText(str(float(self.gui.macros["YS_BACKLASH"])))
        self.gui.tab.zSB.setText(str(float(self.gui.macros["ZS_BACKLASH"])))
        self.gui.tab.xOB.setText(str(float(self.gui.macros["XO_BACKLASH"])))
        self.gui.tab.yOB.setText(str(float(self.gui.macros["YO_BACKLASH"])))
        self.gui.tab.zOB.setText(str(float(self.gui.macros["ZO_BACKLASH"])))

        self._append_text("Updating backlash values.")

    def _motor_status(self, **kwargs: Dict[str, Any]) -> None:
        """Check and set motor status indicators.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `_motor_status`: refer to PyEpics documentation
            for a list of all possible arguments for PV callback functions.
        """

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        label = self.__dict__["gui"].__dict__[f"{axis.lower()}Idle{object}"]

        if value == 0:
            label.setText("IDLE")
            label.setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")
            self._soft_lim_indicators(object, axis)
        elif value == 1:
            label.setText("POWERING")
            label.setStyleSheet(
                "background-color: #ff4747; border: 1px solid black;")
        elif value == 2:
            label.setText("POWERED")
            label.setStyleSheet(
                "background-color: #ff4747; border: 1px solid black;")
        elif value == 3:
            label.setText("RELEASING")
            label.setStyleSheet(
                "background-color: #edde07; border: 1px solid black;")
        elif value == 4:
            label.setText("ACTIVE")
            label.setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        elif value == 5:
            label.setText("APPLYING")
            label.setStyleSheet(
                "background-color: #edde07; border: 1px solid black;")
        else:
            label.setText("UNPOWERING")
            label.setStyleSheet(
                "background-color: #ff4747; border: 1px solid black;")

    def _check_motor_position(self) -> None:
        """Moves motors within soft limits.

        This method checkes each motors position. If a motor is out of the soft
        limits, it will be moved to the closes limit.
        """

        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:

                PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
                NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

                currPos = self.__dict__[f"PV_{axis}{object}POS_ABS"].get()

                if currPos >= PSL:
                    self.__dict__[f"PV_{axis}{object}ABSPOS"].put(PSL)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(0)
                elif currPos <= NSL:
                    self.__dict__[f"PV_{axis}{object}ABSPOS"].put(NSL)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(0)

    def _soft_lim_indicators(self, object: Literal["S", "O"], axis:
                             Literal["X", "Y", "Z"]) -> None:
        """Set soft limit indicators.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample or orbjective using "S" and "O",
            respectively.
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z using "X", "Y", "Z",
            respectively.
        """

        value = self.__dict__[f"PV_{axis}{object}POS"].get()

        negLim = self.__dict__["gui"].__dict__[f"{axis.lower()}{object}Sn"]
        posLim = self.__dict__["gui"].__dict__[f"{axis.lower()}{object}Sp"]

        minSoftLim = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]
        maxSoftLim = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]

        # Set maximum soft limit indicator.
        if maxSoftLim <= value:
            posLim.setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        else:
            posLim.setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")

        # Set minimum soft limit indicator.
        if value <= minSoftLim:
            negLim.setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        else:
            negLim.setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")

    def _hard_lim_indicators(self, **kwargs: Dict[str, Any]) -> None:
        """Set hard limit indicators.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `_hard_lim_indicators`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        """

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]
        direction = pvKey[3]

        label = self.__dict__["gui"].__dict__[
            f"{axis.lower()}{object}H{direction.lower()}"]

        if value > 0:
            label.setStyleSheet(
                "background-color: #3ac200; border: 1px solid black;")
        else:
            label.setStyleSheet(
                "background-color: lightgrey; border: 1px solid black;")

    def _change_display_vals(self, **kwargs: Dict[str, Any]) -> None:
        """Switch displayed values between actual and relative values.

        This method changes all position based line edits and labels between
        actual values and relative values where relative values are taken with
        reference to the zeroed position.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `_change_display_vals`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        """

        pvname = kwargs["pvname"]
        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]
        axis = pvKey[0]
        object = pvKey[1]

        guiDict = self.__dict__["gui"].__dict__

        absPos = guiDict[f"{axis.lower()}{object}AbsPos"]
        hardLims = guiDict["tab"].__dict__[f"{axis.lower()}{object}MM"]
        minSoftLim = guiDict["tab"].__dict__[f"{axis.lower()}{object}Min"]
        maxSoftLim = guiDict["tab"].__dict__[f"{axis.lower()}{object}Max"]
        offsetLabel = guiDict["tab"].__dict__[f"{axis.lower()}{object}Offset"]

        offset = self.__dict__[f"PV_{axis}{object}OFFSET"].get()
        currAbsPos = self.__dict__[f"PV_{axis}{object}POS_ABS"].get()

        self.__dict__[f"PV_{axis}{object}ABSPOS"].put(currAbsPos)
        absPos.setText(str(currAbsPos + offset))

        minLim = self.gui.macros[f"{axis}{object}MIN_HARD_LIMIT"] + offset
        maxLim = self.gui.macros[f"{axis}{object}MAX_HARD_LIMIT"] + offset
        hardLims.setText(f"{minLim} to {maxLim}")

        minLim = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"] + offset
        maxLim = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"] + offset
        minSoftLim.setText(str(minLim))
        maxSoftLim.setText(str(maxLim))

        offsetLabel.setText(str(offset))

    def _change_to_actual(self) -> None:
        """Change display values to actual.

        This method sets all offsets to zero.
        """

        self.PV_XSOFFSET.put(0)
        self.PV_YSOFFSET.put(0)
        self.PV_ZSOFFSET.put(0)
        self.PV_XOOFFSET.put(0)
        self.PV_YOOFFSET.put(0)
        self.PV_ZOOFFSET.put(0)

        self.gui.macros["XS_OFFSET"] = 0
        self.gui.macros["YS_OFFSET"] = 0
        self.gui.macros["ZS_OFFSET"] = 0
        self.gui.macros["XO_OFFSET"] = 0
        self.gui.macros["YO_OFFSET"] = 0
        self.gui.macros["ZO_OFFSET"] = 0

    def _change_to_relative(self) -> None:
        """Change display values to relative.

        This method zeros all motor stages.
        """

        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                caput(self.gui.macros[f"{axis}{object}ZERO"], 1)
                caput(self.gui.macros[f"{axis}{object}ZERO"], 0)

                self.gui.macros[f"{axis}{object}_OFFSET"] = self.__dict__[
                    f"PV_{axis}{object}OFFSET"].get()

    def _zero(self, object: Literal["S", "O"], axis:
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

        Notes
        -----
        Inputed values are relative if `offset!=0` and are absolute if
        `offset==0`. A relative value can be attained by adding the offset
        value to the corresponding absolute value.
        """

        caput(self.gui.macros[f"{axis}{object}ZERO"], 1)
        caput(self.gui.macros[f"{axis}{object}ZERO"], 0)

        self.gui.macros[f"{axis}{object}_OFFSET"] = self.__dict__[
            f"PV_{axis}{object}OFFSET"].get()

        self._append_text(f"Zero'ing the {axis}{object}ABSPOS line edit.")

    def _actual(self, object: Literal["S", "O"], axis:
                Literal["X", "Y", "Z"]) -> None:
        """Convert to relative the sample or objective axis position.

        This method converts motor's position defined by 'object' and 'axis' to
        relative positions.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample or orbjective using "S" and "O",
            respectively.
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z using "X", "Y", "Z",
            respectively.
        """

        self.__dict__[f"PV_{axis}{object}OFFSET"].put(0)
        self.gui.macros[f"{axis}{object}_OFFSET"] = 0

    def _set_current_position(self, **kwargs: Dict[str, Any]) -> None:
        """Update current position label.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `_hard_lim_indicators`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        """

        pvname = kwargs["pvname"]
        value = kwargs["value"]

        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        axis = pvKey[0]
        object = pvKey[1]

        if self.gui.positionUnits.isChecked():
            factor = self.gui.macros[f"{axis}{object}_STEP2MICRON"]
            stepText = f"<b>{round(factor * value, 1)} MICRONS</b>"
        else:
            stepText = f"<b>{round(value, 1)} STEPS</b>"

        stepLineEdit = self.__dict__["gui"].__dict__[
            f"{axis.lower()}Step{object}"]
        stepLineEdit.setText(stepText)

    def _append_text(self, text: str, color: QColor=QColor(0, 0, 0)) -> None:
        """Append text to console window.

        This method adds `text` of color `color` to the main GUI console
        window.

        Parameters
        ----------
        text : str
            String of text to be appended to the console window.
        color : QColor, optional
            RGB color specification for the appended text.
        """

        self.gui.textWindow.setTextColor(color)
        self.gui.textWindow.append(text)
        maxVal = self.gui.textWindow.verticalScrollBar().maximum()
        self.gui.textWindow.verticalScrollBar().setValue(maxVal)

    def _load_config(self) -> None:
        """Load new configuration"""

        self._append_text("Loading new program configuration.")
        path, _ = QFileDialog.getOpenFileName(parent=self.gui,
                                              caption="Open File",
                                              directory="../configuration files",
                                              filter="configuration files (*.json)")
        data, macros = load_config(path)
        self.gui.data = data
        self.gui.macros = macros
        self._initialize_GUI()

    def _save_config(self) -> None:
        """Save current configuration."""

        path, _ = QFileDialog.getSaveFileName(parent=self.gui,
                                              caption="Save File",
                                              directory="../configuration files",
                                              filter="configuration files (*.json)")
        save_config(path, self.gui.data, self.gui.macros)

        self._append_text(f"Configuration saved to {path}")

    def _change_units(self) -> None:
        """Changes the current position's display units."""

        for object in ["O", "S"]:
            for axis in ["X", "Y", "Z"]:

                value = self.__dict__[f"PV_{axis}{object}POS"].get()

                if self.gui.positionUnits.isChecked():
                    factor = self.gui.macros[f"{axis}{object}_STEP2MICRON"]
                    stepText = f"<b>{round(factor * value, 1)} MICRONS</b>"
                else:
                    stepText = f"<b>{round(value, 1)} STEPS</b>"

                stepLineEdit = self.__dict__["gui"].__dict__[
                    f"{axis.lower()}Step{object}"]
                stepLineEdit.setText(stepText)

    def _save_position(self):
        """Save the current position to the program."""

        label = self.gui.posLabel.text()
        position = {}
        position["XS"] = self.PV_XSPOS_ABS.get()
        position["YS"] = self.PV_YSPOS_ABS.get()
        position["ZS"] = self.PV_ZSPOS_ABS.get()
        position["XO"] = self.PV_XOPOS_ABS.get()
        position["YO"] = self.PV_YOPOS_ABS.get()
        position["ZO"] = self.PV_ZOPOS_ABS.get()

        if self.gui.posSelect.findText(label) == -1:

            self.gui.savedPos[label] = position
            self.gui.posSelect.insertItem(1, label)
            save_pos_config(path="saved_positions.json",
                            data=self.gui.savedPos)

            self._append_text(f"Position saved: {label}")

        else:
            self._append_text(("ERROR: Position label already exists, change ",
                              "the position label and try again."),
                              QColor(255, 0, 0))

    def _load_position(self):
        """Load the selected position to the program."""

        label = self.gui.posSelect.currentText()

        if label != "--None--":

            position = self.gui.savedPos[label]

            for object in ["S", "O"]:
                for axis in ["X", "Y", "Z"]:

                    absPos = position[f"{axis}{object}"]

                    PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
                    NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

                    if absPos > PSL or absPos < NSL:
                        self._append_text(("ERROR: Position falls outside of ",
                                          "soft limits."), QColor(255, 0, 0))
                    else:
                        offset = self.__dict__[
                            f"PV_{axis}{object}OFFSET"].get()
                        self.__dict__[
                            f"PV_{axis}{object}ABSPOS"].put(absPos + offset)
                        self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
                        self.__dict__[f"PV_{axis}{object}MOVE"].put(0)

            self._append_text(f"Position loaded: {label}")

    def _delete_position(self):
        """Delete the selected position from the program."""

        label = self.gui.posSelect.currentText()
        index = self.gui.posSelect.currentIndex()

        if index != 0:
            self.gui.posSelect.removeItem(index)
            del self.gui.savedPos[label]
            save_pos_config(path="saved_positions.json",
                            data=self.gui.savedPos)
            self._append_text(f"Position deleted: {label}")

    def _clear_position(self):
        """Clear all saved positions from the program."""

        for key in self.gui.savedPos.keys():
            index = self.gui.posSelect.findText(key)
            self.gui.posSelect.removeItem(index)

        save_pos_config(path="saved_positions.json", data=self.gui.savedPos)
        self._append_text("All positions cleared.")
