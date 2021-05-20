"""Global variables for the microgui project.

The globals module defines global variables used throughout the various modules
of the microgui project. These variables act as placeholders for system
parameters, both constant and variable.
"""

# Define and instantiate hard limit constants.
global XSMIN_HARD_LIMIT
global XSMAX_HARD_LIMIT
global YSMIN_HARD_LIMIT
global YSMAX_HARD_LIMIT
global ZSMIN_HARD_LIMIT
global ZSMAX_HARD_LIMIT
global XOMIN_HARD_LIMIT
global XOMAX_HARD_LIMIT
global YOMIN_HARD_LIMIT
global YOMAX_HARD_LIMIT
global ZOMIN_HARD_LIMIT
global ZOMAX_HARD_LIMIT

XSMIN_HARD_LIMIT = -1000
XSMAX_HARD_LIMIT = 1000
YSMIN_HARD_LIMIT = -1000
YSMAX_HARD_LIMIT = 1000
ZSMIN_HARD_LIMIT = -1000
ZSMAX_HARD_LIMIT = 1000
XOMIN_HARD_LIMIT = -1000
XOMAX_HARD_LIMIT = 1000
YOMIN_HARD_LIMIT = -1000
YOMAX_HARD_LIMIT = 1000
ZOMIN_HARD_LIMIT = -1000
ZOMAX_HARD_LIMIT = 1000

# Define and instantiate soft limit variables.
global XSMIN_SOFT_LIMIT
global XSMAX_SOFT_LIMIT
global YSMIN_SOFT_LIMIT
global YSMAX_SOFT_LIMIT
global ZSMIN_SOFT_LIMIT
global ZSMAX_SOFT_LIMIT
global XOMIN_SOFT_LIMIT
global XOMAX_SOFT_LIMIT
global YOMIN_SOFT_LIMIT
global YOMAX_SOFT_LIMIT
global ZOMIN_SOFT_LIMIT
global ZOMAX_SOFT_LIMIT

XSMIN_SOFT_LIMIT = -1000
XSMAX_SOFT_LIMIT = 1000
YSMIN_SOFT_LIMIT = -1000
YSMAX_SOFT_LIMIT = 1000
ZSMIN_SOFT_LIMIT = -1000
ZSMAX_SOFT_LIMIT = 1000
XOMIN_SOFT_LIMIT = -1000
XOMAX_SOFT_LIMIT = 1000
YOMIN_SOFT_LIMIT = -1000
YOMAX_SOFT_LIMIT = 1000
ZOMIN_SOFT_LIMIT = -1000
ZOMAX_SOFT_LIMIT = 1000

# Define and instantiate backlash variables.
global XS_BACKLASH
global YS_BACKLASH
global ZS_BACKLASH
global XO_BACKLASH
global YO_BACKLASH
global ZO_BACKLASH

XS_BACKLASH = 0
YS_BACKLASH = 0
ZS_BACKLASH = 0
XO_BACKLASH = 0
YO_BACKLASH = 0
ZO_BACKLASH = 0

# Define and instantiate base position variables.
global XS_BASE_POSITION
global YS_BASE_POSITION
global ZS_BASE_POSITION
global XO_BASE_POSITION
global YO_BASE_POSITION
global ZO_BASE_POSITION

XS_BASE_POSITION = 0
YS_BASE_POSITION = 0
ZS_BASE_POSITION = 0
XO_BASE_POSITION = 0
YO_BASE_POSITION = 0
ZO_BASE_POSITION = 0

# Define and instantiate relative position variables.
global XS_RELATIVE_POSITION
global YS_RELATIVE_POSITION
global ZS_RELATIVE_POSITION
global XO_RELATIVE_POSITION
global YO_RELATIVE_POSITION
global ZO_RELATIVE_POSITION

XS_RELATIVE_POSITION = 0
YS_RELATIVE_POSITION = 0
ZS_RELATIVE_POSITION = 0
XO_RELATIVE_POSITION = 0
YO_RELATIVE_POSITION = 0
ZO_RELATIVE_POSITION = 0

# -----------------------------------------------------------------------------
# Axis definition for sample and objective stages:                            -
#  - axisHorizontal -> x,                                                     -
#  - vertical -> y, and                                                       -
#  - focus -> z.                                                              -
# -----------------------------------------------------------------------------

# Define and initantiate process variables for the sample's x dimension.
global XSN
global XSP
global XSSTEP
global XSABSPOS
global XSMOVE
global XSCN
global XSSTOP
global XSCP
global XSSN
global XSSP
global XSHN
global XSHP
global XSZERO
global XSB

XSN = "fihr:SMTR1601-1-R10-28:step:moveDeltaIn"
XSP = "fihr:SMTR1601-1-R10-28:step:moveDeltaOut"
XSSTEP = "fihr:SMTR1601-1-R10-28:step:delta"
XSABSPOS = "fihr:SMTR1601-1-R10-28:step:c:target"
XSMOVE = "fihr:SMTR1601-1-R10-28:step:c:moveTo"
XSCN = "SMTR1601-1-R10-28:step"
XSSTOP = "SMTR1601-1-R10-28:emergStop"
XSCP = "SMTR1601-1-R10-28:step"
XSSN = ""
XSSP = ""
XSHN = "SMTR1601-1-R10-28:ccw"
XSHP = "SMTR1601-1-R10-28:cw"
XSZERO = "fihr:SMTR1601-1-R10-28:setAsZero"
XSB = "fihr:SMTR1601-1-R10-28:step:backlash"

# Define and initantiate process variables for the sample's y dimension.
global YSN
global YSP
global YSSTEP
global YSABSPOS
global YSMOVE
global YSCN
global YSSTOP
global YSCP
global YSSN
global YSSP
global YSHN
global YSHP
global YSZERO
global YSB

YSN = "fihr:SMTR1601-1-R10-29:step:moveDeltaOut"
YSP = "fihr:SMTR1601-1-R10-29:step:moveDeltaIn"
YSSTEP = "fihr:SMTR1601-1-R10-29:step:delta"
YSABSPOS = "fihr:SMTR1601-1-R10-29:step:c:target"
YSMOVE = "fihr:SMTR1601-1-R10-29:step:c:moveTo"
YSCN = "SMTR1601-1-R10-29:step"
YSSTOP = "SMTR1601-1-R10-29:emergStop"
YSCP = "SMTR1601-1-R10-29:step"
YSSN = ""
YSSP = ""
YSHN = "SMTR1601-1-R10-29:ccw"
YSHP = "SMTR1601-1-R10-29:cw"
YSZERO = "fihr:SMTR1601-1-R10-29:setAsZero"
YSB = "fihr:SMTR1601-1-R10-29:step:backlash"

# Define and initantiate process variables for the sample's z dimension.
global ZSN
global ZSP
global ZSSTEP
global ZSABSPOS
global ZSMOVE
global ZSCN
global ZSSTOP
global ZSCP
global ZSSN
global ZSSP
global ZSHN
global ZSHP
global ZSZERO
global ZSB

ZSN = "fihr:SMTR1601-1-R10-30:step:moveDeltaOut"
ZSP = "fihr:SMTR1601-1-R10-30:step:moveDeltaIn"
ZSSTEP = "fihr:SMTR1601-1-R10-30:step:delta"
ZSABSPOS = "fihr:SMTR1601-1-R10-30:step:c:target"
ZSMOVE = "fihr:SMTR1601-1-R10-30:step:c:moveTo"
ZSCN = "SMTR1601-1-R10-30:step"
ZSSTOP = "SMTR1601-1-R10-30:emergStop"
ZSCP = "SMTR1601-1-R10-30:step"
ZSSN = ""
ZSSP = ""
ZSHN = "SMTR1601-1-R10-30:ccw"
ZSHP = "SMTR1601-1-R10-30:cw"
ZSZERO = "fihr:SMTR1601-1-R10-30:setAsZero"
ZSB = "fihr:SMTR1601-1-R10-30:step:backlash"

# Define and initantiate process variables for the objective's x dimension.
global XON
global XOP
global XOSTEP
global XOABSPOS
global XOMOVE
global XOCN
global XOSTOP
global XOCP
global XOSN
global XOSP
global XOHN
global XOHP
global XOZERO
global XOB

XON = "obj:SMTR1601-1-R10-27:step:moveDeltaIn"
XOP = "obj:SMTR1601-1-R10-27:step:moveDeltaOut"
XOSTEP = "obj:SMTR1601-1-R10-27:step:delta"
XOABSPOS = "fihr:SMTR1601-1-R10-27:step:c:target"
XSMOVE = "obj:SMTR1601-1-R10-27:step:c:moveTo"
XOCN = "SMTR1601-1-R10-27:step"
XOSTOP = "SMTR1601-1-R10-27:emergStop"
XOCP = "SMTR1601-1-R10-27:step"
XOSN = ""
XOSP = ""
XOHN = "SMTR1601-1-R10-27:ccw"
XOHP = "SMTR1601-1-R10-27:cw"
XOZERO = "obj:SMTR1601-1-R10-27:setAsZero"
XOB = "obj:SMTR1601-1-R10-27:step:backlash"

# Define and initantiate process variables for the objective's y dimension.
global YON
global YOP
global YOSTEP
global YOABSPOS
global YOMOVE
global YOCN
global YOSTOP
global YOCP
global YOSN
global YOSP
global YOHN
global YOHP
global YOZERO
global YOB

YON = "obj:SMTR1601-1-R10-31:step:moveDeltaIn"
YOP = "obj:SMTR1601-1-R10-31:step:moveDeltaOut"
YOSTEP = "obj:SMTR1601-1-R10-31:step:delta"
YOABSPOS = "fihr:SMTR1601-1-R10-31:step:c:target"
YSMOVE = "obj:SMTR1601-1-R10-31:step:c:moveTo"
YOCN = "SMTR1601-1-R10-31:step"
YOSTOP = "SMTR1601-1-R10-31:emergStop"
YOCP = "SMTR1601-1-R10-31:step"
YOSN = ""
YOSP = ""
YOHN = "SMTR1601-1-R10-31:ccw"
YOHP = "SMTR1601-1-R10-31:cw"
YOZERO = "obj:SMTR1601-1-R10-31:setAsZero"
YOB = "obj:SMTR1601-1-R10-31:step:backlash"

# Define and initantiate process variables for the objective's z dimension.
global ZON
global ZOP
global ZOSTEP
global ZOABSPOS
global ZOMOVE
global ZOCN
global ZOSTOP
global ZOCP
global ZOSN
global ZOSP
global ZOHN
global ZOHP
global ZOZERO
global ZOB

ZON = "obj:SMTR1601-1-R10-32:step:moveDeltaOut"
ZOP = "obj:SMTR1601-1-R10-32:step:moveDeltaIn"
ZOSTEP = "obj:SMTR1601-1-R10-32:step:delta"
ZOABSPOS = "fihr:SMTR1601-1-R10-32:step:c:target"
ZSMOVE = "obj:SMTR1601-1-R10-32:step:c:moveTo"
ZOCN = "SMTR1601-1-R10-32:step"
ZOSTOP = "SMTR1601-1-R10-32:emergStop"
ZOCP = "SMTR1601-1-R10-32:step"
ZOSN = ""
ZOSP = ""
ZOHN = "SMTR1601-1-R10-32:cw"
ZOHP = "SMTR1601-1-R10-32:ccw"
ZOZERO = "obj:SMTR1601-1-R10-32:setAsZero"
ZOB = "obj:SMTR1601-1-R10-32:step:backlash"
