"""
"""


import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from thorlabs_motor_control import changeModeTEST
from globals import *


class Controller:
    """
    """

    def __init__(self, gui, modeMotor):
        """Initialize the Controller."""
        self.gui = gui
        self.modeMotor = modeMotor
        self.connectSignals()
    
    def connectSignals(self):
        """
        This method connects each of the components on the interface with an
        action.

        Parameters
        ----------
        None
        """
        
        # Image Window
        self.gui.WCB.clicked.connect(partial(self.saveImage, self.gui.SIFN, self.gui.image))

        self.gui.tab.RDM1.pressed.connect(partial(self.modeState, self.gui.tab.RDM1, self.modeMotor))
        self.gui.tab.RDM2.pressed.connect(partial(self.modeState, self.gui.tab.RDM2, self.modeMotor))
        self.gui.tab.RDM3.pressed.connect(partial(self.modeState, self.gui.tab.RDM3, self.modeMotor))
        self.gui.tab.RDM4.pressed.connect(partial(self.modeState, self.gui.tab.RDM4, self.modeMotor))

        self.gui.xSN.clicked.connect(partial(self.incPos, 0, 0, 0, self.gui.xSStep))
        self.gui.xSP.clicked.connect(partial(self.incPos, 0, 0, 1, self.gui.xSStep))
        self.gui.ySN.clicked.connect(partial(self.incPos, 0, 1, 0, self.gui.ySStep))
        self.gui.ySP.clicked.connect(partial(self.incPos, 0, 1, 1, self.gui.ySStep))
        self.gui.zSN.clicked.connect(partial(self.incPos, 0, 2, 0, self.gui.zSStep))
        self.gui.zSP.clicked.connect(partial(self.incPos, 0, 2, 1, self.gui.zSStep))
        self.gui.xON.clicked.connect(partial(self.incPos, 1, 0, 0, self.gui.xOStep))
        self.gui.xOP.clicked.connect(partial(self.incPos, 1, 0, 1, self.gui.xOStep))
        self.gui.yON.clicked.connect(partial(self.incPos, 1, 1, 0, self.gui.yOStep))
        self.gui.yOP.clicked.connect(partial(self.incPos, 1, 1, 1, self.gui.yOStep))
        self.gui.zON.clicked.connect(partial(self.incPos, 1, 2, 0, self.gui.zOStep))
        self.gui.zOP.clicked.connect(partial(self.incPos, 1, 2, 1, self.gui.zOStep))

        self.gui.xSMove.clicked.connect(partial(self.absMove, 0, 0, self.gui.xSAbsPos))
        self.gui.ySMove.clicked.connect(partial(self.absMove, 0, 1, self.gui.ySAbsPos))
        self.gui.zSMove.clicked.connect(partial(self.absMove, 0, 2, self.gui.zSAbsPos))
        self.gui.xOMove.clicked.connect(partial(self.absMove, 1, 0, self.gui.xOAbsPos))
        self.gui.yOMove.clicked.connect(partial(self.absMove, 1, 1, self.gui.yOAbsPos))
        self.gui.zOMove.clicked.connect(partial(self.absMove, 1, 2, self.gui.zOAbsPos))

        self.gui.xSCn.clicked.connect(partial(self.continuousMotion, 0, 0, 0))
        self.gui.xSStop.clicked.connect(partial(self.continuousMotion, 0, 0, 1))
        self.gui.xSCp.clicked.connect(partial(self.continuousMotion, 0, 0, 2))
        self.gui.ySCn.clicked.connect(partial(self.continuousMotion, 0, 1, 0))
        self.gui.ySStop.clicked.connect(partial(self.continuousMotion, 0, 1, 1))
        self.gui.ySCp.clicked.connect(partial(self.continuousMotion, 0, 1, 2))
        self.gui.zSCn.clicked.connect(partial(self.continuousMotion, 0, 2, 0))
        self.gui.zSStop.clicked.connect(partial(self.continuousMotion, 0, 2, 1))
        self.gui.zSCp.clicked.connect(partial(self.continuousMotion, 0, 2, 2))
        self.gui.xOCn.clicked.connect(partial(self.continuousMotion, 1, 0, 0))
        self.gui.xOStop.clicked.connect(partial(self.continuousMotion, 1, 0, 1))
        self.gui.xOCp.clicked.connect(partial(self.continuousMotion, 1, 0, 2))
        self.gui.yOCn.clicked.connect(partial(self.continuousMotion, 1, 1, 0))
        self.gui.yOStop.clicked.connect(partial(self.continuousMotion, 1, 1, 1))
        self.gui.yOCp.clicked.connect(partial(self.continuousMotion, 1, 1, 2))
        self.gui.zOCn.clicked.connect(partial(self.continuousMotion, 1, 2, 0))
        self.gui.zOStop.clicked.connect(partial(self.continuousMotion, 1, 2, 1))
        self.gui.zOCp.clicked.connect(partial(self.continuousMotion, 1, 2, 2))

        self.gui.tab.SSL.clicked.connect(partial(self.updateSoftLimits, 0))
        self.gui.tab.SESL.clicked.connect(partial(self.updateSoftLimits, 1))

        self.gui.tab.xSZero.clicked.connect(partial(self.zeroPos, 0, 0))
        self.gui.tab.ySZero.clicked.connect(partial(self.zeroPos, 0, 1))
        self.gui.tab.zSZero.clicked.connect(partial(self.zeroPos, 0, 2))
        self.gui.tab.xOZero.clicked.connect(partial(self.zeroPos, 1, 0))
        self.gui.tab.yOZero.clicked.connect(partial(self.zeroPos, 1, 1))
        self.gui.tab.zOZero.clicked.connect(partial(self.zeroPos, 1, 2))
        self.gui.tab.SBL.clicked.connect(self.updateBacklash)

    def saveImage(self, fileName, image):
        """
        Save current live stream image to current working directory.

        Parameters
        ----------
        fileName : str
            Name of the image file.
        image : np.ndarray
            Array representing the image data.
        """
        filename = fileName.text() + ".png"
        figure = plt.figure()
        plt.imshow(np.rot90(image, 1))
        figure.savefig(filename)
    
    def modeState(self, radioButton, modeMotor):
        """
        Change microscope mode.

        Parameters
        ----------
        radioButton : QtWidget Type
            Radiobutton representing the mode to transfer to.
        modeMotor : Motor Type
            Motor controlling the mode stage.
        """
        modeDict = {"Transmission": 1, "Reflection": 2, "Visible Image": 3, "Beamsplitter": 4}
        changeModeTEST(mode=modeDict[radioButton.text()], modeMotor=modeMotor)

    def incPos(self, object, axis, direction, step):
        """
        Increment motor position.

        Parameters
        ----------
        object : int
            Defines object as either sample or orbjective using 0 and 1.
        axis : int
            Defines axis as x, y, or z using 0, 1, 2.
        direction : int
            Defines object as either negative or positibe using 0 and 1.
        step : QLineEdit
            float(QLineEdit.text()) defines the stepsize to use.
        """
        # USE float(step.text())
        # MAKE CHANGES TO MOTORS
        self.updateAbsPos(object, axis, direction, step)
        self.setRelPos(object, axis)

        #-SIMULATION-----------------------------------------------------------
        Object = {0: 'Sample', 1: 'Objective'}
        Axis = {0: 'x', 1: 'y', 2: 'z'}
        Direction = {0: 'Negative', 1: 'Positive'}
        print(f"{Object[object]} Motion -> {Axis[axis]}-axis, {Direction[direction]}-direction, {step.text()}")
        #----------------------------------------------------------------------
        pass

    def updateAbsPos(self, object, axis, direction, step):
        """
        Increment absolute position line edit.

        Parameters
        ----------
        object : int
            Defines object as either sample or orbjective using 0 and 1.
        axis : int
            Defines axis as x, y, or z using 0, 1, 2.
        direction : int
            Defines object as either negative or positibe using 0 and 1.
        step : QLineEdit
            float(QLineEdit.text()) defines the stepsize to use.
        """
        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}

        currentVal = float(lineEdit[(object, axis)].text())
        stepVal = float(step.text())

        if direction:
            lineEdit[(object, axis)].setText(str(currentVal + stepVal))
        else:
            lineEdit[(object, axis)].setText(str(currentVal - stepVal))

    def absMove(self, object, axis, pos):
        """
        Move sample or objective motor to specified position.

        Parameters
        ----------
        object : int
            Defines object as either sample or orbjective using 0 and 1.
        axis : int
            Defines axis as x, y, or z using 0, 1, 2.
        pos : QLineEdit
            float(QLineEdit.text()) defines the absolute position to use.
        """
        self.setRelPos(object, axis)

        # Move Motor
        
        #-SIMULATION-----------------------------------------------------------
        Object = {0: 'Sample', 1: 'Objective'}
        Axis = {0: 'x', 1: 'y', 2: 'z'}
        print(f"{Object[object]} Motion -> {Axis[axis]}-axis to absolute position: {pos.text()}")
        #----------------------------------------------------------------------

    def updateSoftLimits(self, buttonID):
        """
        Update sample and objective soft limits 

        Parameters
        ----------
        buttonID : int
            Integer representing the button pressed being SSL or SESL using a 0
            or 1 respectively.
        """
        if buttonID:
            # Set soft limits to be equal to hard limits.
            GL = globals()

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

            #-SIMULATION-------------------------------------------------------
            print("Setting soft limits to corresponding hard limits.")
            #------------------------------------------------------------------
        else:
            # UPDATE SOFT LIMIT PARAMETERS
            xSMin = float(self.gui.tab.xSMin.text())
            xSMax = float(self.gui.tab.xSMax.text())
            ySMin = float(self.gui.tab.ySMin.text())
            ySMax = float(self.gui.tab.ySMax.text())
            zSMin = float(self.gui.tab.zSMin.text())
            zSMax = float(self.gui.tab.zSMax.text())
            xOMin = float(self.gui.tab.xOMin.text())
            xOMax = float(self.gui.tab.xOMax.text())
            yOMin = float(self.gui.tab.yOMin.text())
            yOMax = float(self.gui.tab.yOMax.text())
            zOMin = float(self.gui.tab.zOMin.text())
            zOMax = float(self.gui.tab.zOMax.text())

            #-SIMULATION-------------------------------------------------------
            strOne ="Setting:\n"
            strTwo = f"\tSample x -> {xSMin}-Min & {xSMax}-Max, y -> {ySMin}-Min & {ySMax}-Max, z -> {zSMin}-Min & {zSMax}-Max\n"
            strThree = f"\tObjective x -> {xOMin}-Min & {xOMax}-Max, y -> {yOMin}-Min & {yOMax}-Max, z -> {zOMin}-Min & {zOMax}-Max"
            print(strOne + strTwo + strThree)
            #------------------------------------------------------------------
            pass
    
    def continuousMotion(self, object, axis, type):
        """
        Controls continuous motion of the sample and objective stages.

        Parameters
        ----------
        object : int
            Defines object as either sample or orbjective using 0 and 1.
        axis : int
            Defines axis as x, y, or z using 0, 1, 2.
        type : int
            Defines button type as either "continuous negative", "stop", or
            "continuous positive" using 0, 1 and 2, respectively.
        """
        # Fill with motor PVs
        motorPVs = {(0, 0): "Sample X motor", (0, 1): "Sample y motor",
                    (0, 2): "Sample z motor", (1, 0): "Objective x motor",
                    (1, 1): "Objective y motor", (1, 2): "Objective z motor"}
        
        #-SIMULATION-----------------------------------------------------------
        if type == 0:
            print(f"Starting continuous negative motion of: {motorPVs[(object, axis)]}")
        elif type == 1:
            print(f"Stopping all continuous motion of: {motorPVs[(object, axis)]}")
        else:
            print(f"Starting continuous positive motion of: {motorPVs[(object, axis)]}")
        #----------------------------------------------------------------------

    def updateBacklash(self):
        """
        Update backlash variables.

        Parameters
        ----------
        None
        """
        XS_BACKLASH = float(self.gui.tab.xSB.text())
        YS_BACKLASH = float(self.gui.tab.ySB.text())
        ZS_BACKLASH = float(self.gui.tab.zSB.text())
        XO_BACKLASH = float(self.gui.tab.xOB.text())
        YO_BACKLASH = float(self.gui.tab.yOB.text())
        ZO_BACKLASH = float(self.gui.tab.zOB.text())

        #-SIMULATION-----------------------------------------------------------
        strOne = "Updating backlash values:\n"
        strTwo = f"\tXSB -> {XS_BACKLASH}, YSB -> {YS_BACKLASH}, ZSB -> {ZS_BACKLASH}\n"
        strThree = f"\tXOB -> {XO_BACKLASH}, YOB -> {YO_BACKLASH}, ZOB -> {ZO_BACKLASH}\n"
        print(strOne + strTwo + strThree)
        #----------------------------------------------------------------------

    def zeroPos(self, object, axis):
        """
        Zero object axis position.

        Parameters
        ----------
        object : int
            Defines object as either sample or orbjective using 0 and 1.
        axis : int
            Defines axis as x, y, or z using 0, 1, 2.
        """
        GL = globals()

        basePos = {(0, 0): "XS_BASE_POSITION", (1, 0): "XO_BASE_POSITION",
                   (0, 1): "YS_BASE_POSITION", (1, 1): "YO_BASE_POSITION",
                   (0, 2): "ZS_BASE_POSITION", (1, 2): "ZO_BASE_POSITION"}

        relPos = {(0, 0): "XS_RELATIVE_POSITION",
                  (1, 0): "XO_RELATIVE_POSITION",
                  (0, 1): "YS_RELATIVE_POSITION",
                  (1, 1): "YO_RELATIVE_POSITION",
                  (0, 2): "ZS_RELATIVE_POSITION",
                  (1, 2): "ZO_RELATIVE_POSITION"}

        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}

        basePosStr = basePos[(object, axis)]
        relPosStr = relPos[(object, axis)]

        GL[basePosStr] += GL[relPosStr]
        GL[relPosStr] = 0
        lineEdit[(object, axis)].setText("0")

        #-SIMULATION-----------------------------------------------------------
        self.printPositions()
        #----------------------------------------------------------------------
    
    def setRelPos(self, object, axis):
        """
        Set the relative position.

        Parameters
        ----------
        object : int
            Defines object as either sample or orbjective using 0 and 1.
        axis : int
            Defines axis as x, y, or z using 0, 1, 2.
        """
        GL = globals()

        relPos = {(0, 0): "XS_RELATIVE_POSITION",
                  (1, 0): "XO_RELATIVE_POSITION",
                  (0, 1): "YS_RELATIVE_POSITION",
                  (1, 1): "YO_RELATIVE_POSITION",
                  (0, 2): "ZS_RELATIVE_POSITION",
                  (1, 2): "ZO_RELATIVE_POSITION"}

        lineEdit = {(0, 0): self.gui.xSAbsPos, (1, 0): self.gui.xOAbsPos,
                    (0, 1): self.gui.ySAbsPos, (1, 1): self.gui.yOAbsPos,
                    (0, 2): self.gui.zSAbsPos, (1, 2): self.gui.zOAbsPos}

        GL[relPos[(object, axis)]] = float(lineEdit[(object, axis)].text())

    #-SIMULATION---------------------------------------------------------------
        self.printPositions()

    def printPositions(self):
        """
        """
        print(f"XS_BASE_POSITION: {XS_BASE_POSITION}, XS_RELATIVE_POSITION: {XS_RELATIVE_POSITION}")
        print(f"YS_BASE_POSITION: {YS_BASE_POSITION}, YS_RELATIVE_POSITION: {YS_RELATIVE_POSITION}")
        print(f"ZS_BASE_POSITION: {ZS_BASE_POSITION}, ZS_RELATIVE_POSITION: {ZS_RELATIVE_POSITION}")
        print(f"XO_BASE_POSITION: {XO_BASE_POSITION}, XO_RELATIVE_POSITION: {XO_RELATIVE_POSITION}")
        print(f"YO_BASE_POSITION: {YO_BASE_POSITION}, YO_RELATIVE_POSITION: {YO_RELATIVE_POSITION}")
        print(f"ZO_BASE_POSITION: {ZO_BASE_POSITION}, ZO_RELATIVE_POSITION: {ZO_RELATIVE_POSITION}")
    #--------------------------------------------------------------------------
