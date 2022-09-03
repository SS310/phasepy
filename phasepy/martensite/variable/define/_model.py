"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
from numba.experimental import jitclass
from numba import types, typed

#********** Import orizinal module **********

#********** Constant Value **********


__all__ = ["TowardStableModel"]

#********** Class **********
# ----------------------------------------------------------
# spec1 is type-list of TowardStableModel for the jitclass
spec1 = [
]
@jitclass(spec=spec1)
class TowardStableModel():
    """
    Variable about using only **TowardStable** simulation
    """
    def __init__(self, model_parameter: typed.Dict) -> None:
        """
        Variable about using only **TowardStable** simulation
        """
        # Externally configurable variables
        """
        Set the variable according to the following

        variable: variable-type = Initialization
        ```Explain for variable``` # default=1.0, unit=m/s

        - default is the initial value of variable        
        - unit is physical units
        """
        # SETTING-TowardStable-START
        # SETTING-TowardStable-FINISH
        
        # -----------------------------------
        # Externally unconfigurable variables

        # ---------------------
        # Calculating Variables 