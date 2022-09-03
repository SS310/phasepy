"""
Summary
-------
Module on main calculations

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np
from numba import jit, prange

#********** Import orizinal module **********
from phasepy.dendrite.variable.define._var import SimuVal, PropVal, CellVal


#********** Constant Value **********

#********** Function **********

class UpdateField():
    @staticmethod
    @jit(nopython=True, parallel=True)
    def tem_f(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        """
        Update Temperture feild
        """
        tem_t = np.copy(cell_val.tem_f)

        for x in prange(simu_val.xmax):
            for y in prange(simu_val.ymax):
                phase_dt = -1.0*prop_val.mob*(cell_val.tem_fluct[x,y]+cell_val.chem_drive[x,y]+cell_val.grad_drive[x,y])

                tem_dt = ((prop_val.tem_cond*((tem_t[simu_val.xp[x,y],y]+tem_t[simu_val.xm[x,y],y]-2.0*tem_t[x,y])/(simu_val.xsize*simu_val.ysize)+\
                        (tem_t[x,simu_val.yp[x,y]]+tem_t[x,simu_val.ym[x,y]]-2.0*tem_t[x,y])/(simu_val.xsize*simu_val.ysize))+\
                        30.0*((cell_val.phase_f[x,y]*(1.0-cell_val.phase_f[x,y]))**2)*prop_val.lat_heat*phase_dt)/prop_val.spec_heat)
                
                cell_val.tem_f[x,y] = tem_t[x,y] + tem_dt*prop_val.delt

    @staticmethod
    @jit(nopython=True, parallel=True)
    def phase_f(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        """
        Update Phase field variable
        """
        for x in prange(simu_val.xmax):
            for y in prange(simu_val.ymax):
                phase_dt = -1.0*prop_val.mob*(cell_val.tem_fluct[x,y]+cell_val.chem_drive[x,y]+cell_val.grad_drive[x,y])

                cell_val.phase_f[x,y] = cell_val.phase_f[x,y] + phase_dt*prop_val.delt

                if cell_val.phase_f[x,y] >= 1.0:
                    cell_val.phase_f[x,y] = 1.0
                elif cell_val.phase_f[x,y] <= 0.0:
                    cell_val.phase_f[x,y] = 0.0


