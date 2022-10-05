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
from phasepy.fsma.variable.define._var import SimuVal, PropVal, CellVal
from phasepy.fsma.variable.update._energy import MagneEnergy

#********** Constant Value **********

class UpdateField():
    @staticmethod
    @jit(nopython=True, parallel=True)
    def phase_f(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        for pf in prange(2):
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    # Explicit calculation
                    cell_val.phase_f[x,y,pf] = cell_val.phase_f[x,y,pf] + (-1.0*prop_val.p_mob*(cell_val.chem_drive[x,y,pf]+cell_val.grad_drive[x,y,pf]+cell_val.elas_drive[x,y,pf]) + prop_val.fluct*(2.0*np.random.rand()-1.0))*simu_val.delt
                    
                    # Correction of calculated values
                    if cell_val.phase_f[x,y,pf] > 1.0:
                        cell_val.phase_f[x,y,pf] = 1.0
                    elif cell_val.phase_f[x,y,pf] < 0.0:
                        cell_val.phase_f[x,y,pf] = 0.0

    @staticmethod
    def magne_f(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> np.ndarray:        
        # Step 1 of the Gauss-Seidel Method
        _GaussStep1.routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val)
        # Step 2 of the Gauss-Seidel Method
        _GaussStep2.routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val)
        # Step 3 of the Gauss-Seidel Method
        _GaussStep3.routine(simu_val=simu_val, cell_val=cell_val)

# ---------- Internal functions
class _GaussStep1():    
    @staticmethod
    def routine(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        # Normalize magnetic field by magnetization
        _GaussStep1._calc_h(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val)
        
        # Fourie transformation
        for mf in range(3):
            # Magnetic moment is already transformed in Calculation function for Magnetostatic Energy
            #cell_val.magne_f_four[:,:,mf] = np.fft.fft2(cell_val.magne_f[:,:,mf])
            cell_val.h_four[:,:,mf] = np.fft.fft2(cell_val.h[:,:,mf])

        _GaussStep1._calc_g_four(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val)

        # Fourie transformation
        for mf in range(3):
            cell_val.g[:,:,mf] = np.real(np.fft.ifft2(cell_val.g_four[:,:,mf]))

        # --------------------------------------------
        for mf in range(3):
            # Magnetic moment calculation in x,y,z direction
            _GaussStep1._calc_magne_f_star(simu_val=simu_val, cell_val=cell_val, mf=mf)

            # Fourie transformation
            cell_val.magne_f_star_four[:,:,mf] = np.fft.fft2(cell_val.magne_f_star[:,:,mf])

            if mf !=2:
                _GaussStep1._calc_g_star_four(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, mf=mf)
                # Inverse fourie transformation
                cell_val.g_star[:,:,mf] = np.real(np.fft.ifft2(cell_val.g_star_four[:,:,mf]))

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _calc_h(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        for mf in prange(3):
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.h[x,y,mf] = (cell_val.h_anis[x,y,mf]+cell_val.h_me[x,y,mf]+cell_val.h_ms[x,y,mf]+cell_val.h_zeeman[mf])/prop_val.m_s

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _calc_g_four(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        for mf in prange(3):
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.g_four[x,y,mf] = (cell_val.magne_f_four[x,y,mf]+prop_val.m_mob*simu_val.delt*cell_val.h_four[x,y,mf])/\
                                              (1.0+simu_val.alnn[x,y]**2*prop_val.exch_coef_star*prop_val.m_mob*simu_val.delt)

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _calc_magne_f_star(simu_val: SimuVal, cell_val: CellVal, mf: int) -> None:
        # Magnetic moment calculation in x direction
        if mf == 0:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.magne_f_star[x,y,0] = cell_val.magne_f[x,y,0] + (cell_val.g[x,y,1]*cell_val.magne_f[x,y,2]-cell_val.g[x,y,2]*cell_val.magne_f[x,y,1])
        # Magnetic moment calculation in y direction
        elif mf == 1:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.magne_f_star[x,y,0] = cell_val.magne_f[x,y,1] + (cell_val.g[x,y,2]*cell_val.magne_f_star[x,y,0]-cell_val.g_star[x,y,0]*cell_val.magne_f[x,y,2])
        # Magnetic moment calculation in z direction
        elif mf == 2:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.magne_f_star[x,y,2] = cell_val.magne_f[x,y,2] + (cell_val.g_star[x,y,0]*cell_val.magne_f_star[x,y,1]-cell_val.g_star[x,y,1]*cell_val.magne_f_star[x,y,0])
        else:
            raise AttributeError("mf is only 0,1,2")

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _calc_g_star_four(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal, mf: int) -> None:
        for x in prange(simu_val.xmax):
            for y in prange(simu_val.ymax):
                cell_val.g_star_four[x,y,mf] = (cell_val.magne_f_star_four[x,y,mf]+prop_val.m_mob*simu_val.delt*cell_val.h_four[x,y,mf])/\
                                            (1.0+simu_val.alnn[x,y]**2*prop_val.exch_coef_star*prop_val.m_mob*simu_val.delt)


# -------------------------------------------------------------------------
class _GaussStep2():
    @staticmethod
    def routine(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        # For Gauss-Seidel method, exchange energy is calculated separately
        #MagneEnergy.Exchange.calc_h_star(simu_val=simu_val,prop_val=prop_val,cell_val=cell_val)
        MagneEnergy.Anisotropy.calc_h_star(simu_val=simu_val,prop_val=prop_val,cell_val=cell_val)
        MagneEnergy.MagnetoElastic.calc_h_star(simu_val=simu_val,prop_val=prop_val,cell_val=cell_val)
        MagneEnergy.MagnetoStatic.calc_h_star(simu_val=simu_val,prop_val=prop_val,cell_val=cell_val)

        # Normalize magnetic field by magnetization
        _GaussStep2._calc_h_star(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val)

        _GaussStep2._calc_magne_f_star2_four(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val)

        for mf in range(3):
            cell_val.magne_f_star2[:,:,mf] = np.real(np.fft.ifft2(cell_val.magne_f_star2_four[:,:,mf]))

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _calc_h_star(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        for mf in prange(3):
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.h_star[x,y,mf] = (cell_val.h_star_anis[x,y,mf]+cell_val.h_star_me[x,y,mf]+cell_val.h_star_ms[x,y,mf]+cell_val.h_zeeman[mf])/prop_val.m_s

    @staticmethod
    @jit(nopython=True, parallel=True)
    def _calc_magne_f_star2_four(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
        for mf in prange(3):
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.magne_f_star2_four[x,y,mf] = (cell_val.magne_f_star_four[x,y,mf]+prop_val.alpha*prop_val.m_mob*simu_val.delt*cell_val.h_star_four[x,y,mf])/\
                                                     (1.0+simu_val.alnn[x,y]**2*prop_val.exch_coef_star*prop_val.alpha*prop_val.m_mob*simu_val.delt)

# ----------------------------------------------------------------------------------
class _GaussStep3():
    @staticmethod
    @jit(nopython=True, parallel=True)
    def routine(simu_val: SimuVal, cell_val: CellVal) -> None:
        # ----- Normalization
        m_length: float
        for x in prange(simu_val.xmax):
            for y in prange(simu_val.ymax):
                # Length of each magnetic moment
                m_length = (cell_val.magne_f_star2[x,y,0]**2
                            +cell_val.magne_f_star2[x,y,1]**2+cell_val.magne_f_star2[x,y,2]**2)**0.5

                # To avoid division by zero
                if m_length == 0:
                    cell_val.magne_f[x,y,0] = 1.0/3.0
                    cell_val.magne_f[x,y,1] = 1.0/3.0
                    cell_val.magne_f[x,y,2] = 1.0/3.0
                # Normalization
                else:
                    cell_val.magne_f[x,y,0] = cell_val.magne_f_star2[x,y,0]/m_length
                    cell_val.magne_f[x,y,1] = cell_val.magne_f_star2[x,y,1]/m_length
                    cell_val.magne_f[x,y,2] = cell_val.magne_f_star2[x,y,2]/m_length