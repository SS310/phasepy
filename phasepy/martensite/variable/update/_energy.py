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

class PhaseEnergy():
    class Chemical():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.chem_drive[x,y,0] = prop_val.k_s*cell_val.phase_f[x,y,0]*(prop_val.k_s1-prop_val.k_s2*cell_val.phase_f[x,y,0]
                                                +prop_val.k_s3*cell_val.phase_f[x,y,0]**2+prop_val.k_s4*cell_val.phase_f[x,y,1]**2)
                    cell_val.chem_drive[x,y,1] = prop_val.k_s*cell_val.phase_f[x,y,1]*(prop_val.k_s1-prop_val.k_s2*cell_val.phase_f[x,y,1]
                                                +prop_val.k_s3*cell_val.phase_f[x,y,1]**2+prop_val.k_s4*cell_val.phase_f[x,y,0]**2)
    class Gradient():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    for pf in prange(2):
                        cell_val.grad_drive[x,y,pf] = -1.0*prop_val.grad_coef*(cell_val.phase_f[simu_val.xp[x,y],y,pf]+cell_val.phase_f[simu_val.xm[x,y],y,pf]
                                                    +cell_val.phase_f[x,simu_val.yp[x,y],pf]+cell_val.phase_f[x,simu_val.ym[x,y],pf]-4.0*cell_val.phase_f[x,y,pf])

    class Elastic():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    for pf in prange(2):
                        cell_val.elas_drive[x,y,pf] = ((cell_val.ep_eigen[x,y,0,0]-cell_val.ep_eigen_ave[0,0]-cell_val.ep_hetero[x,y,0]-cell_val.ep_ex[0,0])*\
                                                    (prop_val.c_11*prop_val.ep_phase[0,0,pf]+prop_val.c_12*prop_val.ep_phase[1,1,pf])+\
                                                    (cell_val.ep_eigen[x,y,1,1]-cell_val.ep_eigen_ave[1,1]-cell_val.ep_hetero[x,y,1]-cell_val.ep_ex[1,1])*\
                                                    (prop_val.c_11*prop_val.ep_phase[1,1,pf]+prop_val.c_12*prop_val.ep_phase[0,0,pf]))