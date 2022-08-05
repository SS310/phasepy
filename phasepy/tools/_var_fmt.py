"""
Summary
-------


See Also
--------

"""

#********** Import major pakage or module **********

#********** Import orizinal module **********
from numba import types

#********** Constant Value **********


#********** Class **********

class PathVal():
    """
    Format variable about PATH
    """
    def __init__(self) -> None:
        """
        Fromay variable about PATH
        """
        self.output_path: str = None
        """PATH of output directry"""
        self.input_path: dict = None
        """PATH of input file"""
        
        self.counter :dict = {}
        """Counter of setting"""

class SimuVal():
    """
    Format variable about basical simulation parameter
    """
    def __init__(self) -> None:
        """
        Format variable about simulation basic parameter
        """
        self.xmax: types.i4 = None
        """x of cell amount"""
        self.ymax: types.i4 = None
        """y of cell amount"""

class PropVal():
    """
    Format variable about physical property
    """
    def __init__(self) -> None:
        """
        Format variable about physical property
        """
        self.melt_tem: types.f8 = None
        """Melting point (Temperture)"""
        self.supercool_tem: types.f8 = None
        """Supercooling temperture"""

class CellVal():
    """
    Format array based on simulation's cell
    """
    def __init__(self, xmax: int, ymax: int) -> None:
        """
        Format array based on simulation's cell
        """
        pass