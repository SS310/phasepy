"""
Summary
-------


See Also
--------

"""

#********** Import major pakage or module **********

#********** Import orizinal module **********
from phasepy._const import SetPathKey

#********** Constant Value **********


#********** Class **********

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
        
        self.counter :dict = {
            SetPathKey.MAIN:
                {
                SetPathKey.OUTPUT:False,
                SetPathKey.INPUT:False
                }
        }
        """Counter of setting"""