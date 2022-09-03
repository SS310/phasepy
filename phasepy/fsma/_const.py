"""
Summary
-------
Module on Constant

See Also
--------

"""

#********** Import major pakage or module **********

#********** Import orizinal module **********
from phasepy.tools._save import SaveImgMode

#********** Constant Value **********

class OutputDir():
    __PHASE_FIELD = "phase_f"
    """Variable name for phase field variable"""
    __PHASE_FIELD_IMG = "phase_img"
    """Directry name for image of phase field variable"""
    OUTIMG_LIST = [
        [__PHASE_FIELD, SaveImgMode.PHASE_TWO, __PHASE_FIELD_IMG],
    ]
    """
    """