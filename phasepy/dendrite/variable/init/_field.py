"""
Summary
-------
Module on initial conditions

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np
import math

#********** Import orizinal module **********


#********** Constant Value **********
from phasepy.dendrite.variable.define._var import SimuVal, PropVal, CellVal
from phasepy.dendrite.variable.define._model import *

#********** Function **********
class InitField():
    class Temperture():
        def center(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Set initial conditions of temperture field for **RoundCenter** model
            """
            for x in range(simu_val.xmax):
                for y in range(simu_val.ymax):
                    cell_val.tem_f[x,y] = prop_val.supercool_tem + cell_val.phase_f[x,y]*(prop_val.melt_tem-prop_val.supercool_tem)


    class Phase():
        def round_center(simu_val: SimuVal, cell_val: CellVal, model_val: RoundCenterModel) -> any:
            """
            Set initial conditions of phase field variable for **RoundCenter** model
            """
            for x in range(simu_val.xmax):
                for y in range(simu_val.ymax):
                    if simu_val.rad[x,y] <= model_val.nucleus_size:
                        cell_val.phase_f[y, x] = model_val.nucleus_state