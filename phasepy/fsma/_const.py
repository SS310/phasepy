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
    __MAGNE_FIELD = "magne_f"
    """Variable name for magnetic moment"""
    __MAGNE_FIELD_IMG = "magne_img"
    """Directry name for image of magnetic moment"""
    OUTIMG_LIST = [
        [__PHASE_FIELD, SaveImgMode.PHASE_TWO, __PHASE_FIELD_IMG],
        [__MAGNE_FIELD, SaveImgMode.MAGNETIC_MOMENT, __MAGNE_FIELD_IMG]
    ]
    """
    """

class FsmaSetPathKey():
    PHASE_PATH = "phase_path"
    """Key of phase-path"""    
    MAGNE_PATH = "magne_path"
    """Key of magne-path"""