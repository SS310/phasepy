"""
Summary
-------
Module on main calculations

Update log
----------
At the final update date : 2022/06/03
"""

#********** Import major pakage or module **********
import numpy as np
import random as rd
import math
from numba import jit, prange

#********** Import orizinal module **********
from . import _const as const

#********** Constant Value **********
PI = const.MathConst().PI
R_GAS = const.MathConst().R_GAS

#********** Function **********
@jit(nopython=True, parallel=True)
def _calc_fluct(phase_f: np.ndarray, tem_fluct: np.ndarray,
                penal_barrier: float, nois: float) -> np.ndarray:
    """
    Calculate Thermal fluctuations
    """
    y_max, x_max = phase_f.shape
    for y in prange(y_max):
        for x in prange(x_max):
            tem_fluct[y, x] = (4.0*penal_barrier*phase_f[y, x]
                            *(1.0-phase_f[y, x])*nois*(rd.random()-0.5))
    
    return tem_fluct

@jit(nopython=True, parallel=True)
def _calc_chem(phase_f: np.ndarray, tem_f: np.ndarray, chem_e: np.ndarray,
            penal_barrier: float, melt_tem: float, lat_heat: float) -> np.ndarray:
    """
    Calculate chemical energy
    """
    y_max, x_max = phase_f.shape
    for y in prange(y_max):
        for x in prange(x_max):
            dF = (15.0/(2.0*penal_barrier)*lat_heat*(tem_f[y, x]-melt_tem)
                /melt_tem*phase_f[y, x]*(1.0-phase_f[y, x]))

            chem_e[y, x] = (4.0*penal_barrier*phase_f[y, x]
                            *(1.0-phase_f[y, x])*(0.5-phase_f[y, x]+dF))
    
    return chem_e

@jit(nopython=True, parallel=True)
def _calc_grad(phase_f: np.ndarray, grad_e: np.ndarray, si_ta_glow: float,
            grad_e_cf: float, anis_str: float, anis_num: float, cell_size: float) -> np.ndarray:
    """
    Calculate gradient energy
    """
    y_max, x_max = phase_f.shape
    for y in prange(y_max):
        for x in prange(x_max):
            if y == 0:
                ym = 1
                yp = 1
            elif y == (y_max-1):
                ym = y_max-2
                yp = y_max-2
            else:
                ym = y-1
                yp = y+1

            if x == 0:
                xm = 1
                xp = 1
            elif x == (x_max-1):
                xm = x_max-2
                xp = x_max-2
            else:
                xm = x-1
                xp = x+1  

            dy_p = (phase_f[yp, x]-phase_f[ym, x])/(2.0*cell_size)
            dx_p = (phase_f[y, xp]-phase_f[y, xm])/(2.0*cell_size)
            dyy_p = (phase_f[yp, x]+phase_f[ym, x]-2.0*phase_f[y, x])/(cell_size**2)
            dxx_p = (phase_f[y, xp]+phase_f[y, xm]-2.0*phase_f[y, x])/(cell_size**2)
            dyx_p = (phase_f[yp, xp]+phase_f[ym, xm]-phase_f[yp, xm]-phase_f[ym, xp])/(4.0*cell_size**2)
            
            si_ta = math.atan(dy_p/(dx_p+1.0e-20))

            ep = grad_e_cf*(1.0+anis_str*math.cos(anis_num*(si_ta-si_ta_glow)))
            ep1p = -1.0*grad_e_cf*anis_str*anis_num*math.sin(anis_num*(si_ta-si_ta_glow))
            ep2p = -1.0*grad_e_cf*anis_str*(anis_num**2)*math.cos(anis_num*(si_ta-si_ta_glow))

            grad_e[y, x] = (-1.0*(ep**2.0)*(dxx_p+dyy_p)
						 -1.0*ep*ep1p*((dyy_p-dxx_p)*math.sin(2.0*si_ta)+2.0*dyx_p*math.cos(2.0*si_ta))
						 +0.5*(ep1p*ep1p+ep*ep2p)*(2.0*dyx_p*math.sin(2.0*si_ta)-dxx_p-dyy_p-(dyy_p-dxx_p)*math.cos(2.0*si_ta)))

    return grad_e

@jit(nopython=True, parallel=True)
def _update(phase_f: np.ndarray, tem_f: np.ndarray, mob: float, tem_fluct: np.ndarray,
            chem_e: np.ndarray, grad_e: np.ndarray, delt: float, cell_size: float,
            tem_cond: float, lat_heat: float, spec_heat: float):
    """
    Update Phase field variable and Temperture feild
    """
    y_max, x_max = phase_f.shape

    phase_t = np.copy(phase_f)
    tem_t = np.copy(tem_f)

    for y in prange(y_max):
        for x in prange(x_max):
            if y == 0:
                ym = 1
                yp = 1
            elif y == (y_max-1):
                ym = y_max-2
                yp = y_max-2
            else:
                ym = y-1
                yp = y+1

            if x == 0:
                xm = 1
                xp = 1
            elif x == (x_max-1):
                xm = x_max-2
                xp = x_max-2
            else:
                xm = x-1
                xp = x+1
            
            phase_dt = -1.0*mob*(tem_fluct[y, x]+chem_e[y, x]+grad_e[y, x])

            tem_dt = ((tem_cond*((tem_t[y, xp]+tem_t[y, xm]-2.0*tem_t[y, x])/(cell_size**2)
                    +(tem_t[yp, x]+tem_t[ym, x]-2.0*tem_t[y, x])/(cell_size**2))
      	            +30.0*((phase_t[y, x]*(1.0-phase_t[y, x]))**2)*lat_heat*phase_dt)/spec_heat)
            
            tem_f[y, x] = tem_t[y ,x] + tem_dt*delt
            phase_f[y, x] = phase_t[y, x] + phase_dt*delt

            if phase_f[y, x] >= 1.0:
                phase_f[y, x] = 1.0
            elif phase_f[y, x] <= 0.0:
                phase_f[y, x] = 0.0

    return phase_f, tem_f

