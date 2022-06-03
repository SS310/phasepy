"""
Summary
-------
Module on initial conditions

Update log
----------
At the final update date : 2022/06/03
"""

#********** Import major pakage or module **********
from numba import jit
import numpy as np
import math

#********** Import orizinal module **********


#********** Constant Value **********
FIRST_NUCLEUS = 0.9

#********** Function **********
@jit
def _init_set(phase_f: np.ndarray, tem_f: np.ndarray,
            nuc_size: float, supercool_tem: float, melt_tem: float) -> any:
    """
    Setting initial conditions
    """
    y_max, x_max = phase_f.shape
    y_half = (y_max-1)/2
    x_half = (x_max-1)/2

    for y in range(y_max):
        for x in range(x_max):
            rad = math.sqrt((y-y_half)**2+(x-x_half)**2)
            if rad <= nuc_size:
                phase_f[y, x] = FIRST_NUCLEUS
            tem_f[y, x] = supercool_tem + phase_f[y, x]*(melt_tem - supercool_tem)

    return phase_f, tem_f
