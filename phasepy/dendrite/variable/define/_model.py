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


__all__ = ["RoundCenterModel"]

#********** Class **********
# ----------------------------------------------------------
# spec1 is type-list of CenterModel for the jitclass
spec1 = [
    ('nucleus_size', types.f8),
    ('nucleus_state', types.f8),
]
@jitclass(spec=spec1)
class RoundCenterModel():
    """
    Variable about using only **Center** simulation
    """
    def __init__(self, model_parameter: typed.Dict) -> None:
        """
        Variable about using only **RoundCenter** simulation
        """
        # Externally configurable variables
        """
        Set the variable according to the following

        variable: variable-type = Initialization
        ```Explain for variable``` # default=1.0, unit=m/s

        - default is the initial value of variable        
        - unit is physical units
        """
        # SETTING-Center-START
        self.nucleus_size: types.f8 = types.f8(model_parameter["nucleus_size"])
        """Initial nucleus radius (number of cells)""" # default=10, unit=None
        self.nucleus_state: types.f8 = types.f8(model_parameter["nucleus_state"])
        """Phase field variable value of the initial nucleus (0~1)""" # default=0.9, unit=None
        # SETTING-Center-FINISH
        
        # -----------------------------------
        # Externally unconfigurable variables

        # ---------------------
        # Calculating Variables 
        if self.nucleus_state > 1.0:
            self.nucleus_state = 1.0
        elif self.nucleus_state < 0.0:
            self.nucleus_state = 0.0

