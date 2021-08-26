"""Create widgets' interactive nature.

This module contains the `Controller` class to bring life to the GUI defined
in the `GUI` class by connecting widgets up to control sequences that bring
about change.
"""


from configuration import load_config, save_config, save_pos_config
from epics import ca, caput, PV
from gui import GUI
from functools import partial
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFileDialog, QLineEdit
from thorlabs_apt import Motor
from thorlabs_motor_control import changeMode, disable, enable, home
from typing import Any, Dict, Literal

# Set up epics environment.
ca.find_libca()


class Controller(object):
    """Connect widgets to control sequences.

    The `Controller` class connects the widgets defined by the `GUI` class to
    control seuqences allowing for meaningful engagement with program users.

    Parameters
    ----------
    gui : GUI
        User interface to control.
    modeMotor : Motor
        THORLABS motor unit controlling the microscope mode.

    Attributes
    ----------
    gui : GUI
        User interface to control.
    modeMotor : Motor
        THORLABS motor unit controlling the microscope mode.
    PV_SSTEP, PV_YSSTEP, PV_ZSSTEP : PV
        Step PV's for the sample's x, y, and z dimensions.
    PV_XOSTEP, PV_YOSTEP, PV_ZOSTEP : PV
        Step PV's for the objective's x, y, and z dimensions.
    PV_XSABSPOS, PV_YSABSPOS, PV_ZSABSPOS : PV
        Absolute position PV's for the sample's x, y, and z dimensions.
    PV_XOABSPOS, PV_YOABSPOS, PV_ZOABSPOS : PV
        Absolute position PV's for the objective's x, y, and z dimensions.
    PV_XSPOS, PV_YSPOS, PV_ZSPOS : PV
        Current position PV's for the sample's x, y, and z dimensions.
    PV_XOPOS, PV_YOPOS, PV_ZOPOS : PV
        Current position PV's for the objective's x, y, and z dimensions.
    PV_XSPOS_ABS, PV_YSPOS_ABS, PV_ZSPOS_ABS : PV
        Absolute current position PV's for the sample's x, y, and z dimensions.
    PV_XOPOS_ABS, PV_YOPOS_ABS, PV_ZOPOS_ABS : PV
        Absolute current position PV's for the objective's x, y, and z
        dimensions.
    PV_XSMOVE, PV_YSMOVE, PV_ZSMOVE : PV
        Move PV's of the sample's x, y, and z dimensions.
    PV_XOMOVE, PV_YOMOVE, PV_ZOMOVE : PV
        Move PV's of the objective's x, y, and z dimensions.
    PV_XSSTOP, PV_YSSTOP, PV_ZSSTOP : PV
        Stop PV's for the sample's x, y, and z dimensions.
    PV_XOSTOP, PV_YOSTOP, PV_ZOSTOP : PV
        Stop PV's for the objective's x, y, and z dimensions.
    PV_XSHN, PV_YSHN, PV_ZSHN : PV
        Negative hard limit PV's for the sample's x, y, and z dimensions.
    PV_XSHP, PV_YSHP, PV_ZSHP : PV
        Positive hard limit PV's for the sample's x, y, and z dimensions.
    PV_XOHN, PV_YOHN, PV_ZOHN: PV
        Negative hard limit PV's for the objective's x, y, and z dimensions.
    PV_XOHP, PV_YOHP, PV_ZOHP : PV
        Positive hard limit PV's for the objective's x, y, and z dimensions.
    PV_XSSTATE, PV_YSSTATE, PV_ZSSTATE : PV
        State PV's of the sample's x, y, and z dimensions.
    PV_XOSTATE, PV_YOSTATE, PV_ZOSTATE : PV
        State PV's of the objective's x, y, and z dimensions.
    PV_XSOFFSET, PV_YSOFFSET, PV_ZSOFFSET : PV
        Offset PV's for the sample's x, y, and z dimensions.
    PV_XOOFFSET, PV_YOOFFSET, PV_ZOOFFSET : PV
        Offset PV's for the objective's x, y, and z dimensions.

    Methods
    -------
    initialize_process_variables()
        Conigure user interface process variables.
    initialize_gui()
        Configure user interface display values.
    connect_signals()
        Connect widgets to control sequences.
    mode_state(mode, modeMotor)
        Change microscope mode.
    mode_position(mode)
        Update mode position.
    enable_thorlabs()
        Enable or disable the THORLABS motor.
    home_thorlabs()
        Home the THORLABS motor.
    increment(object, axis, direction, step)
        Increment motor position
    absolute(object, axis, pos)
        Move motor to an absolute position.
    continuous(object, axis, type)
        Control continuous motion of the motor.
    update_soft_lim(buttonID)
        Update sample and objective soft limits.
    update_backlash()
        Update backlash variables.
    motor_status(**kwargs)
        Set motor status indicators.
    check_motor_position()
        Assert motor positions are within soft limits.
    soft_lim_indicators(object, axis)
        Set soft limit indicators.
    hard_lim_indicators(**kwargs)
        Set hard limit indicators.
    change_display_vals()
        Toggle display values between actual and relative.
    change_to_actual()
        Change display values to actual values.
    change_to_relative()
        Change display values to relative values.
    zero(object, axis)
        Zero motor position.
    actual(object, axis)
        Un-zero motor position.
    set_current_position(**kwargs)
        Update current position label.
    append_text(text, color)
        Append text to console window.
    load_config()
        Load new configuration.
    save_config()
        Save current configuration.
    change_units()
        Changes the current position's display units.
    save_position()
        Save the current position to a configuration file.
    load_position()
        Move motors to the selected position.
    delete_position()
        Delete the selected position.
    clear_position()
        Clear all saved positions.
    """

    def __init__(self, gui: GUI, modeMotor: Motor) -> None:
        """Initialize the Controller.

        This method initializes the `Controller` class by setting two key
        attributes that will be used significantly thorughout the program in
        addition to calling several methods to set up the PV's, to initialize
        values in the GUI widgets, as well as connecting the widgets to
        control sequences.
        """

        self.gui = gui
        self.modeMotor = modeMotor

        self.initialize_process_variables()
        self.initialize_gui()
        self.connect_signals()

    def initialize_process_variables(self) -> None:
        """Conigure user interface process variables.

        This method initializes all PV's that will need to be called within the
        program ans also configures auto-monitoring and callback functions for
        certain process variables.

        Notes
        -----
        In some instances, the process variables could not be connected with
        during the program execution without initialization. Configuring
        process variables in this section improves the ability to connect with
        process variables during program execution.
        """

        mac = self.gui.macros

        # Conigure step PV.
        self.PV_XSSTEP = PV(pvname=mac["XSSTEP"])
        self.PV_YSSTEP = PV(pvname=mac["YSSTEP"])
        self.PV_ZSSTEP = PV(pvname=mac["ZSSTEP"])
        self.PV_XOSTEP = PV(pvname=mac["XOSTEP"])
        self.PV_YOSTEP = PV(pvname=mac["YOSTEP"])
        self.PV_ZOSTEP = PV(pvname=mac["XOSTEP"])

        # Set absolute position PV monitoring and callback.
        self.PV_XSABSPOS = PV(pvname=mac["XSABSPOS"])
        self.PV_YSABSPOS = PV(pvname=mac["YSABSPOS"])
        self.PV_ZSABSPOS = PV(pvname=mac["ZSABSPOS"])
        self.PV_XOABSPOS = PV(pvname=mac["XOABSPOS"])
        self.PV_YOABSPOS = PV(pvname=mac["YOABSPOS"])
        self.PV_ZOABSPOS = PV(pvname=mac["ZOABSPOS"])

        # Set current position PV monitoring and callback.
        cb = self.set_current_position
        self.PV_XSPOS = PV(pvname=mac["XSPOS"], auto_monitor=True, callback=cb)
        self.PV_YSPOS = PV(pvname=mac["YSPOS"], auto_monitor=True, callback=cb)
        self.PV_ZSPOS = PV(pvname=mac["ZSPOS"], auto_monitor=True, callback=cb)
        self.PV_XOPOS = PV(pvname=mac["XOPOS"], auto_monitor=True, callback=cb)
        self.PV_YOPOS = PV(pvname=mac["YOPOS"], auto_monitor=True, callback=cb)
        self.PV_ZOPOS = PV(pvname=mac["ZOPOS"], auto_monitor=True, callback=cb)

        # Initialize current absolute position PV's.
        self.PV_XSPOS_ABS = PV(pvname=mac["XSPOS_ABS"])
        self.PV_YSPOS_ABS = PV(pvname=mac["YSPOS_ABS"])
        self.PV_ZSPOS_ABS = PV(pvname=mac["ZSPOS_ABS"])
        self.PV_XOPOS_ABS = PV(pvname=mac["XOPOS_ABS"])
        self.PV_YOPOS_ABS = PV(pvname=mac["YOPOS_ABS"])
        self.PV_ZOPOS_ABS = PV(pvname=mac["ZOPOS_ABS"])

        # Initialize move PV's.
        self.PV_XSMOVE = PV(pvname=mac["XSMOVE"])
        self.PV_YSMOVE = PV(pvname=mac["YSMOVE"])
        self.PV_ZSMOVE = PV(pvname=mac["ZSMOVE"])
        self.PV_XOMOVE = PV(pvname=mac["XOMOVE"])
        self.PV_YOMOVE = PV(pvname=mac["YOMOVE"])
        self.PV_ZOMOVE = PV(pvname=mac["ZOMOVE"])

        # Configure emergency stop PVs.
        self.PV_XSSTOP = PV(pvname=mac["XSSTOP"])
        self.PV_YSSTOP = PV(pvname=mac["YSSTOP"])
        self.PV_ZSSTOP = PV(pvname=mac["ZSSTOP"])
        self.PV_XOSTOP = PV(pvname=mac["XOSTOP"])
        self.PV_YOSTOP = PV(pvname=mac["YOSTOP"])
        self.PV_ZOSTOP = PV(pvname=mac["ZOSTOP"])

        # Set hard limit position PV monitoring and callback.
        cb = self.hard_lim_indicators
        self.PV_XSHN = PV(pvname=mac["XSHN"], auto_monitor=True, callback=cb)
        self.PV_XSHP = PV(pvname=mac["XSHP"], auto_monitor=True, callback=cb)
        self.PV_YSHN = PV(pvname=mac["YSHN"], auto_monitor=True, callback=cb)
        self.PV_YSHP = PV(pvname=mac["YSHP"], auto_monitor=True, callback=cb)
        self.PV_ZSHN = PV(pvname=mac["ZSHN"], auto_monitor=True, callback=cb)
        self.PV_ZSHP = PV(pvname=mac["ZSHP"], auto_monitor=True, callback=cb)
        self.PV_XOHN = PV(pvname=mac["XOHN"], auto_monitor=True, callback=cb)
        self.PV_XOHP = PV(pvname=mac["XOHP"], auto_monitor=True, callback=cb)
        self.PV_YOHN = PV(pvname=mac["YOHN"], auto_monitor=True, callback=cb)
        self.PV_YOHP = PV(pvname=mac["YOHP"], auto_monitor=True, callback=cb)
        self.PV_ZOHN = PV(pvname=mac["ZOHN"], auto_monitor=True, callback=cb)
        self.PV_ZOHP = PV(pvname=mac["ZOHP"], auto_monitor=True, callback=cb)

        # Set state PV monitoring and callback.
        cb = self.motor_status
        self.PV_XSSTATE = PV(pvname=mac["XSSTATE"], auto_monitor=True,
                             callback=cb)
        self.PV_YSSTATE = PV(pvname=mac["YSSTATE"], auto_monitor=True,
                             callback=cb)
        self.PV_ZSSTATE = PV(pvname=mac["ZSSTATE"], auto_monitor=True,
                             callback=cb)
        self.PV_XOSTATE = PV(pvname=mac["XOSTATE"], auto_monitor=True,
                             callback=cb)
        self.PV_YOSTATE = PV(pvname=mac["YOSTATE"], auto_monitor=True,
                             callback=cb)
        self.PV_ZOSTATE = PV(pvname=mac["ZOSTATE"], auto_monitor=True,
                             callback=cb)

        # Initialize offset PV monitoring and callback.
        cb = self.change_display_vals
        self.PV_XSOFFSET = PV(pvname=mac["XSOFFSET"], auto_monitor=True,
                              callback=cb)
        self.PV_YSOFFSET = PV(pvname=mac["YSOFFSET"], auto_monitor=True,
                              callback=cb)
        self.PV_ZSOFFSET = PV(pvname=mac["ZSOFFSET"], auto_monitor=True,
                              callback=cb)
        self.PV_XOOFFSET = PV(pvname=mac["XOOFFSET"], auto_monitor=True,
                              callback=cb)
        self.PV_YOOFFSET = PV(pvname=mac["YOOFFSET"], auto_monitor=True,
                              callback=cb)
        self.PV_ZOOFFSET = PV(pvname=mac["ZOOFFSET"], auto_monitor=True,
                              callback=cb)

        # Intialize backlash PV's.
        self.PV_XSB = PV(mac["XSB"])
        self.PV_YSB = PV(mac["YSB"])
        self.PV_ZSB = PV(mac["ZSB"])
        self.PV_XOB = PV(mac["XOB"])
        self.PV_YOB = PV(mac["YOB"])
        self.PV_ZOB = PV(mac["ZOB"])

        # Print output statement.
        self.append_text("PVs configured and initialized.")

    def initialize_gui(self) -> None:
        """Configure user interface display values.

        This method initializes the user interface display by setting widget
        values to the current process variable values or, where applicable,
        setting thhe process variables to values from the initial configuration
        file.
        """

        def text_str_val(label: str) -> str:
            return str(float(self.gui.macros[label]))

        # Set THORLABS motor position line edits.
        self.gui.tab.TMTM.setText(text_str_val("TRANSMISSION_POSITION"))
        self.gui.tab.TMRM.setText(text_str_val("REFLECTION_POSITION"))
        self.gui.tab.TMVM.setText(text_str_val("VISIBLE_IMAGE_POSITION"))
        self.gui.tab.TMBM.setText(text_str_val("BEAMSPLITTER_POSITION"))

        # Set soft limit line edits.
        self.gui.tab.xSMin.setText(text_str_val("XSMIN_SOFT_LIMIT"))
        self.gui.tab.xSMax.setText(text_str_val("XSMAX_SOFT_LIMIT"))
        self.gui.tab.ySMin.setText(text_str_val("YSMIN_SOFT_LIMIT"))
        self.gui.tab.ySMax.setText(text_str_val("YSMAX_SOFT_LIMIT"))
        self.gui.tab.zSMin.setText(text_str_val("ZSMIN_SOFT_LIMIT"))
        self.gui.tab.zSMax.setText(text_str_val("ZSMAX_SOFT_LIMIT"))
        self.gui.tab.xOMin.setText(text_str_val("XOMIN_SOFT_LIMIT"))
        self.gui.tab.xOMax.setText(text_str_val("XOMAX_SOFT_LIMIT"))
        self.gui.tab.yOMin.setText(text_str_val("YOMIN_SOFT_LIMIT"))
        self.gui.tab.yOMax.setText(text_str_val("YOMAX_SOFT_LIMIT"))
        self.gui.tab.zOMin.setText(text_str_val("ZOMIN_SOFT_LIMIT"))
        self.gui.tab.zOMax.setText(text_str_val("ZOMAX_SOFT_LIMIT"))

        # Set all offset PV's to the saved offsets.
        self.PV_XSOFFSET.put(self.gui.macros["XS_OFFSET"])
        self.PV_YSOFFSET.put(self.gui.macros["YS_OFFSET"])
        self.PV_ZSOFFSET.put(self.gui.macros["ZS_OFFSET"])
        self.PV_XOOFFSET.put(self.gui.macros["XO_OFFSET"])
        self.PV_YOOFFSET.put(self.gui.macros["YO_OFFSET"])
        self.PV_ZOOFFSET.put(self.gui.macros["ZO_OFFSET"])

        # Set offset line edits to current PV values.
        self.gui.tab.xSOffset.setText(text_str_val("XS_OFFSET"))
        self.gui.tab.ySOffset.setText(text_str_val("YS_OFFSET"))
        self.gui.tab.zSOffset.setText(text_str_val("ZS_OFFSET"))
        self.gui.tab.xOOffset.setText(text_str_val("XO_OFFSET"))
        self.gui.tab.yOOffset.setText(text_str_val("YO_OFFSET"))
        self.gui.tab.zOOffset.setText(text_str_val("ZO_OFFSET"))

        # Set backlash PV values.
        self.PV_XSB.put(self.gui.macros["XS_BACKLASH"])
        self.PV_YSB.put(self.gui.macros["YS_BACKLASH"])
        self.PV_ZSB.put(self.gui.macros["ZS_BACKLASH"])
        self.PV_XOB.put(self.gui.macros["XO_BACKLASH"])
        self.PV_YOB.put(self.gui.macros["YO_BACKLASH"])
        self.PV_ZOB.put(self.gui.macros["ZO_BACKLASH"])

        # Set backlash line edits to current PV values.
        self.gui.tab.xSB.setText(text_str_val("XS_BACKLASH"))
        self.gui.tab.ySB.setText(text_str_val("YS_BACKLASH"))
        self.gui.tab.zSB.setText(text_str_val("ZS_BACKLASH"))
        self.gui.tab.xOB.setText(text_str_val("XO_BACKLASH"))
        self.gui.tab.yOB.setText(text_str_val("YO_BACKLASH"))
        self.gui.tab.zOB.setText(text_str_val("ZO_BACKLASH"))

        # Set step line edits to current PV values.
        self.gui.xSStep.setText(str(float(self.PV_XSSTEP.get())))
        self.gui.ySStep.setText(str(float(self.PV_YSSTEP.get())))
        self.gui.zSStep.setText(str(float(self.PV_ZSSTEP.get())))
        self.gui.xOStep.setText(str(float(self.PV_XOSTEP.get())))
        self.gui.yOStep.setText(str(float(self.PV_YOSTEP.get())))
        self.gui.zOStep.setText(str(float(self.PV_ZOSTEP.get())))

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
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                self.soft_lim_indicators(object, axis)

        # Print output statement.
        self.append_text("Display values and macros initialized.")

    def connect_signals(self) -> None:
        """Connect widgets to control sequences.

        This method connects each control widget from the user interface to a
        control sequence. This allows the program to respond to user inputs to
        widgets and enact change to local hardware.
        """

        # Mode select functionality.
        self.gui.tab.RDM1.pressed.connect(
            partial(self.mode_state, "TRANSMISSION_POSITION", self.modeMotor))
        self.gui.tab.RDM2.pressed.connect(
            partial(self.mode_state, "REFLECTION_POSITION", self.modeMotor))
        self.gui.tab.RDM3.pressed.connect(
            partial(self.mode_state, "VISIBLE_IMAGE_POSITION", self.modeMotor))
        self.gui.tab.RDM4.pressed.connect(
            partial(self.mode_state, "BEAMSPLITTER_POSITION", self.modeMotor))

        # THORLABS/mode motor functionality.
        self.gui.tab.enableDisable.clicked.connect(self.enable_thorlabs)
        self.gui.tab.home.clicked.connect(self.home_thorlabs)

        # Mode position-set functionality.
        self.gui.tab.TMTMbutton.clicked.connect(
            partial(self.mode_position, "TRANSMISSION_POSITION"))
        self.gui.tab.TMRMbutton.clicked.connect(
            partial(self.mode_position, "REFLECTION_POSITION"))
        self.gui.tab.TMVMbutton.clicked.connect(
            partial(self.mode_position, "VISIBLE_IMAGE_POSITION"))
        self.gui.tab.TMBMbutton.clicked.connect(
            partial(self.mode_position, "BEAMSPLITTER_POSITION"))

        # Increment sample and objective stage functionality.
        self.gui.xSN.clicked.connect(
            partial(self.increment, "S", "X", "N", self.gui.xSStep))
        self.gui.xSP.clicked.connect(
            partial(self.increment, "S", "X", "P", self.gui.xSStep))
        self.gui.ySN.clicked.connect(
            partial(self.increment, "S", "Y", "N", self.gui.ySStep))
        self.gui.ySP.clicked.connect(
            partial(self.increment, "S", "Y", "P", self.gui.ySStep))
        self.gui.zSN.clicked.connect(
            partial(self.increment, "S", "Z", "N", self.gui.zSStep))
        self.gui.zSP.clicked.connect(
            partial(self.increment, "S", "Z", "P", self.gui.zSStep))
        self.gui.xON.clicked.connect(
            partial(self.increment, "O", "X", "N", self.gui.xOStep))
        self.gui.xOP.clicked.connect(
            partial(self.increment, "O", "X", "P", self.gui.xOStep))
        self.gui.yON.clicked.connect(
            partial(self.increment, "O", "Y", "N", self.gui.yOStep))
        self.gui.yOP.clicked.connect(
            partial(self.increment, "O", "Y", "P", self.gui.yOStep))
        self.gui.zON.clicked.connect(
            partial(self.increment, "O", "Z", "N", self.gui.zOStep))
        self.gui.zOP.clicked.connect(
            partial(self.increment, "O", "Z", "P", self.gui.zOStep))

        # Move sample and objective stage to absolute position functionality.
        self.gui.xSMove.clicked.connect(partial(self.absolute, "S", "X"))
        self.gui.ySMove.clicked.connect(partial(self.absolute, "S", "Y"))
        self.gui.zSMove.clicked.connect(partial(self.absolute, "S", "Z"))
        self.gui.xOMove.clicked.connect(partial(self.absolute, "O", "X"))
        self.gui.yOMove.clicked.connect(partial(self.absolute, "O", "Y"))
        self.gui.zOMove.clicked.connect(partial(self.absolute, "O", "Z"))

        # Continuous motion of the sample and objective stages functionality.
        self.gui.xSCn.clicked.connect(
            partial(self.continuous, "S", "X", "CN"))
        self.gui.xSStop.clicked.connect(
            partial(self.continuous, "S", "X", "STOP"))
        self.gui.xSCp.clicked.connect(
            partial(self.continuous, "S", "X", "CP"))
        self.gui.ySCn.clicked.connect(
            partial(self.continuous, "S", "Y", "CN"))
        self.gui.ySStop.clicked.connect(
            partial(self.continuous, "S", "Y", "STOP"))
        self.gui.ySCp.clicked.connect(
            partial(self.continuous, "S", "Y", "CP"))
        self.gui.zSCn.clicked.connect(
            partial(self.continuous, "S", "Z", "CN"))
        self.gui.zSStop.clicked.connect(
            partial(self.continuous, "S", "Z", "STOP"))
        self.gui.zSCp.clicked.connect(
            partial(self.continuous, "S", "Z", "CP"))
        self.gui.xOCn.clicked.connect(
            partial(self.continuous, "O", "X", "CN"))
        self.gui.xOStop.clicked.connect(
            partial(self.continuous, "O", "X", "STOP"))
        self.gui.xOCp.clicked.connect(
            partial(self.continuous, "O", "X", "CP"))
        self.gui.yOCn.clicked.connect(
            partial(self.continuous, "O", "Y", "CN"))
        self.gui.yOStop.clicked.connect(
            partial(self.continuous, "O", "Y", "STOP"))
        self.gui.yOCp.clicked.connect(
            partial(self.continuous, "O", "Y", "CP"))
        self.gui.zOCn.clicked.connect(
            partial(self.continuous, "O", "Z", "CN"))
        self.gui.zOStop.clicked.connect(
            partial(self.continuous, "O", "Z", "STOP"))
        self.gui.zOCp.clicked.connect(
            partial(self.continuous, "O", "Z", "CP"))

        # Updating soft limits functionality.
        self.gui.tab.SSL.clicked.connect(partial(self.update_soft_lim, 0))
        self.gui.tab.SMSL.clicked.connect(partial(self.update_soft_lim, 1))
        self.gui.tab.SESL.clicked.connect(partial(self.update_soft_lim, 2))

        # Zero'ing absolute position functionality.
        self.gui.tab.xSZero.clicked.connect(partial(self.zero, "S", "X"))
        self.gui.tab.ySZero.clicked.connect(partial(self.zero, "S", "Y"))
        self.gui.tab.zSZero.clicked.connect(partial(self.zero, "S", "Z"))
        self.gui.tab.xOZero.clicked.connect(partial(self.zero, "O", "X"))
        self.gui.tab.yOZero.clicked.connect(partial(self.zero, "O", "Y"))
        self.gui.tab.zOZero.clicked.connect(partial(self.zero, "O", "Z"))

        # Un-zero'ing absolute position functionality.
        self.gui.tab.xSActual.clicked.connect(partial(self.actual, "S", "X"))
        self.gui.tab.ySActual.clicked.connect(partial(self.actual, "S", "Y"))
        self.gui.tab.zSActual.clicked.connect(partial(self.actual, "S", "Z"))
        self.gui.tab.xOActual.clicked.connect(partial(self.actual, "O", "X"))
        self.gui.tab.yOActual.clicked.connect(partial(self.actual, "O", "Y"))
        self.gui.tab.zOActual.clicked.connect(partial(self.actual, "O", "Z"))

        # Updating backlash functionality.
        self.gui.tab.SBL.clicked.connect(self.update_backlash)

        # Switching between actual and relative values functionality.
        self.gui.tab.allActual.clicked.connect(self.change_to_actual)
        self.gui.tab.zeroAll.clicked.connect(self.change_to_relative)

        # Toggle units between steps and microns.
        self.gui.positionUnits.clicked.connect(self.change_units)

        # Load and save configuration functionality.
        self.gui.savePos.clicked.connect(self.save_position)
        self.gui.loadPos.clicked.connect(self.load_position)
        self.gui.deletePos.clicked.connect(self.delete_position)
        self.gui.clearPos.clicked.connect(self.clear_position)

        # Configuration functionality.
        self.gui.loadConfig.clicked.connect(self.load_config)
        self.gui.saveConfig.clicked.connect(self.save_config)

        # Print output statement.
        self.append_text("Widgets connected to control sequences.")

    def mode_state(self, mode: str, modeMotor: Motor) -> None:
        """Change microscope mode.

        This method is enacted when a THORLABS mode button is pressed to
        change the THORLABS motor position.

        Parameters
        ----------
        mode : str
            String identifier specifying the pressed mode button. The `mode`
            parameter can take only the following valid inputs:
            "TRANSMISSION_POSITION", "REFLECTION_POSITION",
            "VISIBLE_IMAGE_POSITION", and "BEAMSPLITTER_POSITION".
        modeMotor : Motor
            `Motor` object controlling the mode stage.

        Notes
        -----
        The method will print a status statement when the motor is successfully
        changing modes, else it will print an error message.
        """

        # Set move_to position based on mode.
        position = self.gui.macros[mode]
        status = changeMode(pos=position, modeMotor=modeMotor)

        if status == -1:
            # Print output statement.
            self.append_text("ERROR: Can not change mode.", QColor(255, 0, 0))
        else:
            # Print output statement.
            self.append_text(f"Changing mode to {mode}.")

    def mode_position(self, mode: str) -> None:
        """Update mode position.

        This method is enacted when a "Set Position" button on the "Mode" tab
        is pressed to update the modes positon.

        Parameters
        ----------
        mode : str
            The mode identifier specifying the mode position to be updated.
        """

        # Get the line edit object and check if the current mode is selected.
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

        # Update the macro mode position variable.
        self.gui.macros[mode] = float(pos_line_edit.text())
        pos_line_edit.setText(str(self.gui.macros[mode]))

        # If the mode is selected, move to the updated position.
        if radio_select:
            self.mode_state(mode, self.modeMotor)

        # Print output statement.
        self.append_text("Setting new mode position.")

    def enable_thorlabs(self) -> None:
        """Enable or disable the THORLABS motor.

        This method checkes the motor is currently enabled or disabled and
        applies the opposite operation to change the state of the THORLABS
        motor.
        """

        # Get widget text.
        label = self.gui.tab.enableDisable.text()

        if label == "Enable":
            # Enable the motor and change its label.
            enable(self.modeMotor)
            self.gui.tab.enableDisable.setText("Disable")

            message = "THORLABS motor enabled."
        else:
            # Disabl the motor and change its label.
            disable(self.modeMotor)
            self.gui.tab.enableDisable.setText("Enable")

            message = "THORLABS motor disabled."

        # Print output statement.
        self.append_text(message)

    def home_thorlabs(self) -> None:
        """Home the THORLABS motor.

        This method homes the THORLABS motor to its zero position. If the
        motor successfully homes, the mode select buttons will be unchecked and
        an output statement will be printed or else an error statement will be
        printed.

        Notes
        -----
        The mode select buttons are all unchecked if the motor successfully
        homes instead of moving to a mode with a 0 position as these values are
        subject to change is calibration dictates. Thus, there may not always
        exist a mode with a zero position.
        """

        try:
            # Home motor.
            home(self.modeMotor)

            # Uncheck all mode select buttons.
            self.gui.tab.group.setExclusive(False)
            self.gui.tab.RDM1.setChecked(False)
            self.gui.tab.RDM2.setChecked(False)
            self.gui.tab.RDM3.setChecked(False)
            self.gui.tab.RDM4.setChecked(False)
            self.gui.tab.group.setExclusive(True)

            # Print output statement.
            self.append_text("THORLABS motor homing.")
        except:
            # Print output statement.
            self.append_text("ERROR: THORLABS motor can not be homed.",
                             QColor(255, 0, 0))


    def increment(self, object: Literal["S", "O"], axis:
                  Literal["X", "Y", "Z"], direction: Literal["N", "P"], step:
                  QLineEdit) -> None:
        """Increment motor position.

        Increment the motor defined by 'object' and 'axis' in the direction
        defined by 'direction' by the amount 'step.text()'.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample ("S") or orbjective ("O").
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z.
        direction : {"N", "P"}
            Defines increment direction as either negative ("N") or positive
            ("P").
        step : QLineEdit
            The step line edit for the specific stage.

        Notes
        -----
        The step value can be found from the `step` parameter as
        `float(step.text())`.

        The step value must be positive to keep motion consistency with the
        programs diagram.

        If a step size takes the motor beyond a soft limit then the step size
        will be updated to take the motor to the soft limit.
        """

        # Get current absolute position and step size.
        absPos = self.__dict__[f"PV_{axis}{object}POS_ABS"].get()
        incPos = float(step.text())

        # If the step size is negative, make it possitive.
        if incPos < 0:
            incPos = -incPos
            step.setText(str(incPos))
            self.append_text("WARNING: Step must be positive.",
                             QColor(250, 215, 0))

        # Get soft limits.
        PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

        # Change step size if it breaches soft limits.
        if direction == "P" and absPos + incPos > PSL:
            incPos = PSL - absPos
        elif direction == "N" and absPos - incPos < NSL:
            incPos = absPos - NSL

        # Write to process variables.
        self.__dict__[f"PV_{axis}{object}STEP"].put(incPos)
        caput(self.gui.macros[f"{axis}{object}{direction}"], 1)

    def absolute(self, object: Literal["S", "O"], axis:
                 Literal["X", "Y", "Z"]) -> None:
        """Move motor to an absolute position.

        This method moves the motor defined by 'object' and 'axis' to the
        absolute position types into the corresponding line edit.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample ("S") or orbjective ("O").
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z.

        Notes
        -----
        If the absolute position lays outside of the soft limits, the program
        will move the motor to the soft limit.
        """

        # Get absolute position.
        absPosLineEdit = self.__dict__["gui"].__dict__[f"{axis.lower()}{object}AbsPos"]
        absPos = float(absPosLineEdit.text())
        absPosLineEdit.setText(str(absPos))

        # Get spft limits.
        PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
        NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

        # Change absolute position if it breaches soft limits.
        if absPos > PSL:
            absPos = PSL
        elif absPos < NSL:
            absPos = NSL

        # Write to process variables.
        self.__dict__[f"PV_{axis}{object}ABSPOS"].put(absPos)
        self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
        self.__dict__[f"PV_{axis}{object}MOVE"].put(0)

    def continuous(self, object: Literal["S", "O"], axis:
                   Literal["X", "Y", "Z"], type:
                   Literal["CN", "STOP", "CP"]) -> None:
        """Control continuous motion of the motor.

        This method allows for the continuous motion functionality of the
        sample and objective stages. It will invoke continuous positive motion,
        continuous negative motion, or cease of motion (dictated by 'type') of
        the motor defined by 'object' and 'axis'.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample ("S") or orbjective ("O").
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z.
        type : {"CN", "STOP", "CP"}
            Defines motion as continuous negative ("CN"), stop ("STOP"), or
            continuous positive ("CP").

        Notes
        -----
        The program will write the inbound soft limit to the continuous motion
        proces variables so that it will stop at the soft limit if "STOP" is
        not pressed.
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

    def update_soft_lim(self, buttonID: Literal[0, 1, 2]) -> None:
        """Update sample and objective soft limits.

        This method is called when one of the three update soft limit buttons
        are pressed. The method will set the soft limits to either the inputted
        values, zero, or to the hard limits.

        Parameters
        ----------
        buttonID : {0, 1, 2}
            Defines the method of soft limit updating. If `buttonID==0`, the
            soft limits will be set to the input values. If `buttonID==1`, the
            soft limits will be set to zero. If `buttonID==2`, the soft limits
            will be set to the hard limits.

        Notes
        -----
        In the case that `buttonID==2` and an input soft limit lay beyond the
        hard limit values, the soft limit will be set to the hard limit. If the
        lower soft limit is greater than the higher soft limit, the program
        will not update the soft limit.
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
            # Set soft limits to input values
            for object in ["S", "O"]:
                for axis in ["X", "Y", "Z"]:

                    offset = self.__dict__[f"PV_{axis}{object}OFFSET"].get()

                    tabDict = self.__dict__["gui"].__dict__["tab"].__dict__

                    # Get the input limits.
                    min = float(tabDict[
                        f"{axis.lower()}{object}Min"].text()) - offset
                    max = float(tabDict[
                        f"{axis.lower()}{object}Max"].text()) - offset

                    # Check if the minimum limit is greater than the upper.
                    if min > max:
                        self.append_text(f"WARNING: Invalid limit. Minimum limits must be less then maximum limits.",
                                         QColor(250, 215, 0))

                    else:
                        min_soft_ind = f"{axis}{object}MIN_SOFT_LIMIT"
                        max_soft_ind = f"{axis}{object}MAX_SOFT_LIMIT"

                        min_hard = self.gui.macros[f"{axis}{object}MIN_HARD_LIMIT"]
                        max_hard = self.gui.macros[f"{axis}{object}MAX_HARD_LIMIT"]

                        # Check that the new limit is within the hard limits.
                        val = min_hard if min < min_hard else min
                        self.gui.macros[min_soft_ind] = val

                        # Check that the new limit is within the hard limits.
                        val = max_hard if max > max_hard else max
                        self.gui.macros[max_soft_ind] = val

        # Create heler function to generate soft limit text.
        def set(label: str, offset: PV) -> str:
            return str(self.gui.macros[label] + offset.get())

        # Update soft limit line edits.
        self.gui.tab.xSMin.setText(set("XSMIN_SOFT_LIMIT", self.PV_XSOFFSET))
        self.gui.tab.xSMax.setText(set("XSMAX_SOFT_LIMIT", self.PV_XSOFFSET))
        self.gui.tab.ySMin.setText(set("YSMIN_SOFT_LIMIT", self.PV_YSOFFSET))
        self.gui.tab.ySMax.setText(set("YSMAX_SOFT_LIMIT", self.PV_YSOFFSET))
        self.gui.tab.zSMin.setText(set("ZSMIN_SOFT_LIMIT", self.PV_ZSOFFSET))
        self.gui.tab.zSMax.setText(set("ZSMAX_SOFT_LIMIT", self.PV_ZSOFFSET))
        self.gui.tab.xOMin.setText(set("XOMIN_SOFT_LIMIT", self.PV_XOOFFSET))
        self.gui.tab.xOMax.setText(set("XOMAX_SOFT_LIMIT", self.PV_XOOFFSET))
        self.gui.tab.yOMin.setText(set("YOMIN_SOFT_LIMIT", self.PV_YOOFFSET))
        self.gui.tab.yOMax.setText(set("YOMAX_SOFT_LIMIT", self.PV_YOOFFSET))
        self.gui.tab.zOMin.setText(set("ZOMIN_SOFT_LIMIT", self.PV_ZOOFFSET))
        self.gui.tab.zOMax.setText(set("ZOMAX_SOFT_LIMIT", self.PV_ZOOFFSET))

        # Move motors to within soft limits.
        self.check_motor_position()

        # Set soft limit indicators.
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                self.soft_lim_indicators(object, axis)

        # Print output statement.
        self.append_text("Updating soft limits.")

    def update_backlash(self) -> None:
        """Update backlash variables.

        This method takes the input backlash values and writes them to the
        backlash process variables and saves them to macro variables.
        """

        tabDict = self.__dict__["gui"].__dict__["tab"].__dict__

        # Set global backlash variables (used to save configuration files).
        self.gui.macros["XS_BACKLASH"] = abs(int(float(tabDict["xSB"].text())))
        self.gui.macros["YS_BACKLASH"] = abs(int(float(tabDict["ySB"].text())))
        self.gui.macros["ZS_BACKLASH"] = abs(int(float(tabDict["zSB"].text())))
        self.gui.macros["XO_BACKLASH"] = abs(int(float(tabDict["xOB"].text())))
        self.gui.macros["YO_BACKLASH"] = abs(int(float(tabDict["yOB"].text())))
        self.gui.macros["ZO_BACKLASH"] = abs(int(float(tabDict["zOB"].text())))

        # Set backlash process variables.
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

        # Print output statement
        self.append_text("Updating backlash values.")

    def motor_status(self, **kwargs: Dict[str, Any]) -> None:
        """Set motor status indicators.

        This method takes the current motor status to update the motor status
        indicators.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `motor_status`: refer to PyEpics documentation
            for a list of all possible arguments for PV callback functions.

        Notes
        -----
        The `soft_lim_indicators` method is called within to approximate
        live soft limit updating by polling.
        """

        # Get process variable information.
        pvname = kwargs["pvname"]
        value = kwargs["value"]

        # Get the process variable name.
        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        # Get the motor stage information.
        axis = pvKey[0]
        object = pvKey[1]

        label = self.__dict__["gui"].__dict__[f"{axis.lower()}Idle{object}"]

        if value == 0:
            text = "IDLE"
            style = "background-color: lightgrey; border: 1px solid black;"

            # Poll soft limit checks for "live" limit indicator updates.
            self.soft_lim_indicators(object, axis)
        elif value == 1:
            text = "POWERING"
            style = "background-color: #ff4747; border: 1px solid black;"
        elif value == 2:
            text = "POWERED"
            style = "background-color: #ff4747; border: 1px solid black;"
        elif value == 3:
            text = "RELEASING"
            style = "background-color: #edde07; border: 1px solid black;"
        elif value == 4:
            text = "ACTIVE"
            style = "background-color: #3ac200; border: 1px solid black;"
        elif value == 5:
            text = "APPLYING"
            style = "background-color: #edde07; border: 1px solid black;"
        else:
            text = "UNPOWERING"
            style = "background-color: #ff4747; border: 1px solid black;"

        label.setText(text)
        label.setStyleSheet(style)

    def check_motor_position(self) -> None:
        """Assert motor positions are within soft limits.

        This method checkes each motors position to see if it lays within
        soft limits. If a motor is out of the soft limits, it will be moved to
        the closest limit.

        Notes
        -----
        This method was inspired by the need to ensure the motors stay within
        soft limits even when more constraining limits are set.
        """

        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:

                PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
                NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

                currPos = self.__dict__[f"PV_{axis}{object}POS_ABS"].get()

                # If position breaches a limit, move to that limit.
                if currPos >= PSL:
                    self.__dict__[f"PV_{axis}{object}ABSPOS"].put(PSL)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(0)
                elif currPos <= NSL:
                    self.__dict__[f"PV_{axis}{object}ABSPOS"].put(NSL)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(0)

    def soft_lim_indicators(self, object: Literal["S", "O"], axis:
                            Literal["X", "Y", "Z"]) -> None:
        """Set soft limit indicators.

        This method checks the motor stage specified by `object` and `axis` to
        see if it has reached a soft limit. If a soft limit is reached,
        illuminate the soft limit indicator.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample ("S") or orbjective ("O").
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z.
        """

        value = self.__dict__[f"PV_{axis}{object}POS"].get()

        negLim = self.__dict__["gui"].__dict__[f"{axis.lower()}{object}Sn"]
        posLim = self.__dict__["gui"].__dict__[f"{axis.lower()}{object}Sp"]

        minSoftLim = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]
        maxSoftLim = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]

        # Define style sheets.
        grey = "background-color: lightgrey; border: 1px solid black;"
        green = "background-color: #3ac200; border: 1px solid black;"

        # Set minimum and maximum soft limit indicators.
        negLim.setStyleSheet(green if value <= minSoftLim else grey)
        posLim.setStyleSheet(green if maxSoftLim <= value else grey)

    def hard_lim_indicators(self, **kwargs: Dict[str, Any]) -> None:
        """Set hard limit indicators.

        This method is called when a hard limit process variable value changes
        to check if a limit has activated or deactivated such that the
        indicator can be updated.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `hard_lim_indicators`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        """

        # Get process variable information.
        pvname = kwargs["pvname"]
        value = kwargs["value"]

        # Get the process variable name.
        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        # Get the motor stage information.
        axis = pvKey[0]
        object = pvKey[1]
        direction = pvKey[3]

        # Get the hard limit label.
        label = self.__dict__["gui"].__dict__[
            f"{axis.lower()}{object}H{direction.lower()}"]

        # Set style sheets.
        green = "background-color: #3ac200; border: 1px solid black;"
        grey = "background-color: lightgrey; border: 1px solid black;"

        # Set hard limit indicator.
        label.setStyleSheet(green if value > 0 else grey)

    def change_display_vals(self, **kwargs: Dict[str, Any]) -> None:
        """Toggle display values between actual and relative.

        This method changes all position based line edits and labels between
        actual values and relative values. Relative values are taken with
        reference to the zeroed datum whereas actual values are measured with
        respect to the original datum.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `change_display_vals`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        """

        # Get process variable and motor stage information.
        pvname = kwargs["pvname"]
        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]
        axis = pvKey[0]
        object = pvKey[1]

        guiDict = self.__dict__["gui"].__dict__

        # Get display labels that need to be updated.
        hardLims = guiDict["tab"].__dict__[f"{axis.lower()}{object}MM"]
        minSoftLim = guiDict["tab"].__dict__[f"{axis.lower()}{object}Min"]
        maxSoftLim = guiDict["tab"].__dict__[f"{axis.lower()}{object}Max"]
        offsetLabel = guiDict["tab"].__dict__[f"{axis.lower()}{object}Offset"]

        offset = self.__dict__[f"PV_{axis}{object}OFFSET"].get()
        currAbsPos = self.__dict__[f"PV_{axis}{object}POS_ABS"].get()

        # Update the absolute position line edit.
        self.__dict__[f"PV_{axis}{object}ABSPOS"].put(currAbsPos)

        # Update the hard limit indicators.
        minLim = self.gui.macros[f"{axis}{object}MIN_HARD_LIMIT"] + offset
        maxLim = self.gui.macros[f"{axis}{object}MAX_HARD_LIMIT"] + offset
        hardLims.setText(f"{minLim} to {maxLim}")

        # Update the soft limit indicators.
        minLim = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"] + offset
        maxLim = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"] + offset
        minSoftLim.setText(str(minLim))
        maxSoftLim.setText(str(maxLim))

        # Update the offset label.
        offsetLabel.setText(str(offset))

    def change_to_actual(self) -> None:
        """Change display values to actual values.

        This method changes all display values to actual values by setting all
        offsets to zero.

        Notes
        -----
        The `change_display_vals` method serves as a callback function to the
        offset process variables. By setting each offset to zero will cause the
        `change_display_vals` method will be called to update the display
        values.
        """

        # Un-zero each motor stage.
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                self.actual(object, axis)

    def change_to_relative(self) -> None:
        """Change display values to relative values.

        This method changes all display values to relative values by zeroing
        all motor stages.

        Notes
        -----
        The `change_display_vals` method serves as a callback function to the
        offset process variables. By zeroing each stage a change in the offset
        process variable will be made causing the `change_display_vals` method
        to be called to update the display values.
        """

        # Zero each motor stage.
        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:
                self.zero(object, axis)

    def zero(self, object: Literal["S", "O"], axis:
             Literal["X", "Y", "Z"]) -> None:
        """Zero motor position.

        This method zeros the motor defined by 'object' and 'axis'.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample ("S") or orbjective ("O").
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z.

        Notes
        -----
        Values iput into the program are relative if `offset!=0` and are
        absolute if `offset==0`. A relative value can be attained by adding the
        offset value to the corresponding absolute value.

        The `change_display_vals` method serves as a callback function to the
        offset process variables. By zeroing a stage, a change in the offset
        process variable will be made causing the `change_display_vals` method
        to be called to update the display values.
        """

        caput(self.gui.macros[f"{axis}{object}ZERO"], 1)
        caput(self.gui.macros[f"{axis}{object}ZERO"], 0)

        self.gui.macros[f"{axis}{object}_OFFSET"] = self.__dict__[
            f"PV_{axis}{object}OFFSET"].get()

        # Print output statement.
        self.append_text(f"Zero'ing the {axis}{object}ABSPOS line edit.")

    def actual(self, object: Literal["S", "O"], axis:
               Literal["X", "Y", "Z"]) -> None:
        """Un-zero motor position.

        This method converts motor's position defined by 'object' and 'axis' to
        a relative position by setting the offset to zero.

        Parameters
        ----------
        object : {"S", "O"}
            Defines the stage as either sample ("S") or orbjective ("O").
        axis : {"X", "Y", "Z"}
            Defines the motor axis as x, y, or z.

        Notes
        -----
        The `change_display_vals` method serves as a callback function to the
        offset process variables. Setting the offset to zero will cause the
        `change_display_vals` method to be called to update the display
        values.
        """

        # Set offset value to zero.
        self.__dict__[f"PV_{axis}{object}OFFSET"].put(0)
        self.gui.macros[f"{axis}{object}_OFFSET"] = 0

    def set_current_position(self, **kwargs: Dict[str, Any]) -> None:
        """Update current position label.

        This method is called at each change of the current position process
        variable to update current position label.

        Parameters
        ----------
        **kwargs : dict
            Extra arguments to `set_current_position`: refer to PyEpics
            documentation for a list of all possible arguments for PV callback
            functions.
        """

        # Get process variable information.
        pvname = kwargs["pvname"]
        value = kwargs["value"]

        # Get process variable name.
        keys = list(self.gui.macros.keys())
        vals = list(self.gui.macros.values())
        pvKey = keys[vals.index(pvname)]

        # Get motor information.
        axis = pvKey[0]
        object = pvKey[1]

        # Generate label text.
        if self.gui.positionUnits.isChecked():
            factor = self.gui.macros[f"{axis}{object}_STEP2MICRON"]
            stepText = f"<b>{round(factor * value, 1)} MICRONS</b>"
        else:
            stepText = f"<b>{round(value, 1)} STEPS</b>"

        # Update the step label text.
        stepLabel = self.__dict__["gui"].__dict__[f"{axis.lower()}Step{object}"]
        stepLabel.setText(stepText)

    def append_text(self, text: str, color: QColor=QColor(0, 0, 0)) -> None:
        """Append text to console window.

        This method adds `text` of color `color` to the interface's program
        status window.

        Parameters
        ----------
        text : str
            String of text to be appended to the console window.
        color : QColor, optional
            RGB color specification for the appended text.

        Notes
        -----
        Regular text is used to communicate information about what the program
        is doing. Regular text should use the default text color (i.e.
        `QColor=QColor(0, 0, 0)`).

        Warning labels are provided when the program will execute a request but
        with slight modifications (e.g. correcting a negative step size before
        incrementing a motor position). Warning labels should have a yellow
        text color, `QColor=QColor(250, 215, 0)`.

        Error labels are provided when the program can not execute a request
        (e.g. changing modes when the THORLABS motor is disabled). Error labels
        should have a red text color, `QColor=QColor(255, 0, 0)`.
        """

        self.gui.textWindow.setTextColor(color)
        self.gui.textWindow.append(text)
        maxVal = self.gui.textWindow.verticalScrollBar().maximum()
        self.gui.textWindow.verticalScrollBar().setValue(maxVal)

    def load_config(self) -> None:
        """Load new configuration.

        This method will open a window to allow a user to select a
        configuration file to upload.

        Notes
        -----
        Once the file is loaded, the macro variables will be overwritten and
        a call to the `initialize_gui` method will be called to change process
        variable and display values.
        """

        params = {"parent": self.gui,
                  "caption": "Open File",
                  "directory": "../configuration files",
                  "filter": "configuration files (*.json)"}
        path, _ = QFileDialog.getOpenFileName(**params)

        # Print output statement.
        self.append_text(f"Loading configuration from {path}")

        data, macros = load_config(path)
        self.gui.data = data
        self.gui.macros = macros
        self.initialize_gui()

    def save_config(self) -> None:
        """Save current configuration.

        This method will open a window to allow a user to select a location
        and file name to save to.

        Notes
        -----
        Once the path and file name is attained, the macro variables will be
        restructured into a non-linear dictionary and then saved to a
        configuration file.
        """

        params = {"parent": self.gui,
                  "caption": "Save File",
                  "directory": "../configuration files",
                  "filter": "configuration files (*.json)"}
        path, _ = QFileDialog.getSaveFileName(**params)

        save_config(path, self.gui.data, self.gui.macros)

        # Print output statement.
        self.append_text(f"Configuration saved to {path}")

    def change_units(self) -> None:
        """Changes the current position's display units.

        This method toggles the current step labels between displaying units of
        steps or microns.
        """

        for object in ["O", "S"]:
            for axis in ["X", "Y", "Z"]:

                # Get the current position.
                value = self.__dict__[f"PV_{axis}{object}POS"].get()

                # Generate the step text.
                if self.gui.positionUnits.isChecked():
                    factor = self.gui.macros[f"{axis}{object}_STEP2MICRON"]
                    stepText = f"<b>{round(factor * value, 1)} MICRONS</b>"
                else:
                    stepText = f"<b>{round(value, 1)} STEPS</b>"

                # Update the current position label text.
                stepLabel = self.__dict__["gui"].__dict__[f"{axis.lower()}Step{object}"]
                stepLabel.setText(stepText)

    def save_position(self):
        """Save the current position to a configuration file.

        This method takes the current absolute positions of all motors and
        saves them to a configuration file.

        Notes
        -----
        Once the positions are gained from each motor, they will be organized
        into a dictionary where the keys define the motor and the values are
        the corresponding positions. This position dictionary is then saved
        into the gui's `savedPos` attribute (which is a dictionary) with the
        key being the position label and the values being the dictionary of
        position.

        Once the position is saved in dynamic memory, the program updates the
        `saved_positions.json` file to keep the saved positions in memory even
        if the program crashes.
        """

        # Get position label.
        label = self.gui.posLabel.text()

        # Check that the label is unique
        if self.gui.posSelect.findText(label) == -1:

            # Generate position dictionary.
            position = {}
            position["XS"] = self.PV_XSPOS_ABS.get()
            position["YS"] = self.PV_YSPOS_ABS.get()
            position["ZS"] = self.PV_ZSPOS_ABS.get()
            position["XO"] = self.PV_XOPOS_ABS.get()
            position["YO"] = self.PV_YOPOS_ABS.get()
            position["ZO"] = self.PV_ZOPOS_ABS.get()

            # Save position into dynamic memory.
            self.gui.savedPos[label] = position

            # Update the position select drop down menu.
            self.gui.posSelect.insertItem(1, label)

            # Update the saved positions file.
            save_pos_config(path="saved_positions.json",
                            data=self.gui.savedPos)

            # Print output statement.
            self.append_text(f"Position saved: {label}")

        else:
            # Print output statement.
            self.append_text("ERROR: Position label already exists, change the position label and try again.",
                             QColor(255, 0, 0))

    def load_position(self):
        """Move motors to the selected position.

        This method takes the selected position and moves each motor to their
        saved position.

        Notes
        -----
        This method takes the selected label to use as the key to the
        `GUI.savedPos` dictionary to get the dictionary of positions. Each
        position is then loaded into the corresponding motor. The motor is then
        moved to the loaded position.
        """

        # Get position label.
        label = self.gui.posSelect.currentText()

        # Exit the method if the selected position is the "--None--" statement.
        if label == "--None--":
            return None

        # Get the positions corresponding to the label.
        position = self.gui.savedPos[label]

        for object in ["S", "O"]:
            for axis in ["X", "Y", "Z"]:

                # Get the position for the current motor.
                absPos = position[f"{axis}{object}"]

                # Get the soft limits.
                PSL = self.gui.macros[f"{axis}{object}MAX_SOFT_LIMIT"]
                NSL = self.gui.macros[f"{axis}{object}MIN_SOFT_LIMIT"]

                # Check if the loaded position falls within the soft limits.
                if absPos > PSL or absPos < NSL:
                    self.append_text("ERROR: Position falls outside of soft limits.",
                                     QColor(255, 0, 0))
                else:
                    # Load and move to position.
                    offset = self.__dict__[f"PV_{axis}{object}OFFSET"].get()
                    self.__dict__[f"PV_{axis}{object}ABSPOS"].put(absPos + offset)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(1)
                    self.__dict__[f"PV_{axis}{object}MOVE"].put(0)

        # Print output statement.
        self.append_text(f"Position loaded: {label}")

    def delete_position(self):
        """Delete the selected position.

        Notes
        -----
        This method deletes the current position from the program by removing
        its position from the `GUI.savedPos` dictionary and the positions
        drop down menu before updating the saved positions configuration file.
        """

        # Get information on the selected position
        label = self.gui.posSelect.currentText()
        index = self.gui.posSelect.currentIndex()

        # Check if the selected position is the "--None--" label.
        if index == 0:
            return None

        self.gui.posSelect.removeItem(index)
        del self.gui.savedPos[label]
        save_pos_config(path="saved_positions.json", data=self.gui.savedPos)

        # Print output statement.
        self.append_text(f"Position deleted: {label}")

    def clear_position(self):
        """Clear all saved positions.

        Notes
        -----
        This method removes all items from the positions drop down menu and
        `GUI.savedPos` dictionary before updating the saved positions
        configuration file.
        """

        # Remove each item from the drop down menu and positions dictionary.
        for key in self.gui.savedPos.keys():
            index = self.gui.posSelect.findText(key)
            self.gui.posSelect.removeItem(index)
            del self.gui.savedPos[key]

        save_pos_config(path="saved_positions.json", data=self.gui.savedPos)

        # Print output statement.
        self.append_text("All positions cleared.")
