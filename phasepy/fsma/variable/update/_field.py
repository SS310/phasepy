"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np
from numba import jit, prange

#********** Import orizinal module **********
from phasepy.martensite.variable.define._var import SimuVal, PropVal, CellVal

#********** Constant Value **********

class UpdateField():
    @staticmethod
    @jit(nopython=True, parallel=True)
    def phase_f(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> np.ndarray:
        for x in prange(simu_val.xmax):
            for y in prange(simu_val.ymax):
                for pf in prange(2):
                    # Explicit calculation
                    cell_val.phase_f[x,y,pf] = cell_val.phase_f[x,y,pf] + (-1.0*prop_val.mob*(cell_val.chem_drive[x,y,pf]+cell_val.grad_drive[x,y,pf]+cell_val.elas_drive[x,y,pf]) + prop_val.fluct*(2.0*np.random.rand()-1.0))*simu_val.delt
                    
                    # Correction of calculated values
                    if cell_val.phase_f[x,y,pf] > 1.0:
                        cell_val.phase_f[x,y,pf] = 1.0
                    elif cell_val.phase_f[x,y,pf] < 0.0:
                        cell_val.phase_f[x,y,pf] = 0.0