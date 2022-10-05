"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********

#********** Import orizinal module **********
from phasepy._const import SetPathKey
from phasepy.fsma._const import FsmaSetPathKey

#********** Constant Value **********

class PathVal():
    """
    Variable about PATH
    """
    def __init__(self) -> None:
        """
        Variable about PATH
        """
        self.output_path: str = None
        """PATH of output directry"""
        self.input_path: dict = None
        """PATH of input file"""
        self.phase_path: str = None
        """PATH of initial martensite structure image"""
        self.magne_path: str = None
        """PATH of initial magnetic domain image"""
        
        self.counter :dict = {
            SetPathKey.MAIN:
                {
                SetPathKey.OUTPUT:False,
                SetPathKey.INPUT:False
                },
            SetPathKey.SUB:
                {
                FsmaSetPathKey.PHASE_PATH:False,
                FsmaSetPathKey.MAGNE_PATH:False
                }
        }
        """Counter of setting"""
