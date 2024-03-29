"""
Summary
-------
Module on main calculations

See Also
--------

"""

#********** Import major pakage or module **********
import random as rd
import math
from numba import jit, prange

#********** Import orizinal module **********
from phasepy.dendrite.variable.define._var import SimuVal, PropVal, CellVal

#********** Constant Value **********

#********** Function **********

class PhaseEnergy():
    """
    Energy of phase field variable
    """
    class ThermalFluct():
        """
        Thermal fluctuations
        """
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Calculate Thermal fluctuations
            """
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.tem_fluct[x,y] = (4.0*prop_val.penal_barrier*cell_val.phase_f[x,y]*(1.0-cell_val.phase_f[x,y])*prop_val.nois*(rd.random()-0.5))
    
    # ---------------------------------------------------------
    class Chemical():
        """
        Chemical Energy
        """
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Calculate chemical driving force
            """
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.chem_drive[x,y] = (30.0*cell_val.phase_f[x,y]**4-60.0*cell_val.phase_f[x,y]**3+30.0*cell_val.phase_f[x,y]**2)*\
                                               (prop_val.lat_heat*(cell_val.tem_f[x,y]-prop_val.melt_tem)/prop_val.melt_tem)


        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Calculate chemical energy
            """
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.chem_energy[x,y] = (cell_val.phase_f[x,y]**3)*(10.0-15.0*cell_val.phase_f[x,y]+6.0*cell_val.phase_f[x,y]**2)*(prop_val.lat_heat*(cell_val.tem_f[x,y]-prop_val.melt_tem)/prop_val.melt_tem)

    # ---------------------------------------------------------
    class Gradient():
        """
        Gradient Energy
        """
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Calculate gradient driving force
            """
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    dx_p = (cell_val.phase_f[simu_val.xp[x,y],y]-cell_val.phase_f[simu_val.xm[x,y],y])/(2.0*simu_val.xsize)
                    dy_p = (cell_val.phase_f[x,simu_val.yp[x,y]]-cell_val.phase_f[x,simu_val.ym[x,y]])/(2.0*simu_val.ysize)
                    dxx_p = (cell_val.phase_f[simu_val.xp[x,y],y]+cell_val.phase_f[simu_val.xm[x,y],y]-2.0*cell_val.phase_f[x,y])/(simu_val.xsize*simu_val.ysize)
                    dyy_p = (cell_val.phase_f[x,simu_val.yp[x,y]]+cell_val.phase_f[x,simu_val.ym[x,y]]-2.0*cell_val.phase_f[x,y])/(simu_val.xsize*simu_val.ysize)
                    dxy_p = (cell_val.phase_f[simu_val.xp[x,y],simu_val.yp[x,y]]+cell_val.phase_f[simu_val.xm[x,y],simu_val.ym[x,y]]-cell_val.phase_f[simu_val.xp[x,y],simu_val.ym[x,y]]-cell_val.phase_f[simu_val.xm[x,y],simu_val.yp[x,y]])/(4.0*simu_val.xsize*simu_val.ysize)
                    
                    sita = math.atan(dy_p/(dx_p+1.0e-20))

                    ep = prop_val.grad_coef*(1.0+prop_val.anis_str*math.cos(prop_val.anis_num*(sita-prop_val.grow_sita)))
                    ep1p = -1.0*prop_val.grad_coef*prop_val.anis_str*prop_val.anis_num*math.sin(prop_val.anis_num*(sita-prop_val.grow_sita))
                    ep2p = -1.0*prop_val.grad_coef*prop_val.anis_str*(prop_val.anis_num**2)*math.cos(prop_val.anis_num*(sita-prop_val.grow_sita))

                    cell_val.grad_drive[x,y] = (-1.0*(ep**2.0)*(dxx_p+dyy_p)-\
                        1.0*ep*ep1p*((dyy_p-dxx_p)*math.sin(2.0*sita)+2.0*dxy_p*math.cos(2.0*sita))+\
                        0.5*(ep1p*ep1p+ep*ep2p)*(2.0*dxy_p*math.sin(2.0*sita)-dxx_p-dyy_p-(dyy_p-dxx_p)*math.cos(2.0*sita)))

        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Calculate gradient energy
            """
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    dx_p = (cell_val.phase_f[simu_val.xp[x,y],y]-cell_val.phase_f[simu_val.xm[x,y],y])/(2.0*simu_val.xsize)
                    dy_p = (cell_val.phase_f[x,simu_val.yp[x,y]]-cell_val.phase_f[x,simu_val.ym[x,y]])/(2.0*simu_val.ysize)
                    sita = math.atan(dy_p/(dx_p+1.0e-20))

                    cell_val.grad_energy[x,y] = 0.5*(prop_val.grad_coef*(1.0+prop_val.anis_str*math.cos(prop_val.anis_num*(sita-prop_val.grow_sita))))**2*(dx_p**2+dy_p**2)

    class DoubleWell():
        """
        Double-well Potential
        """
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Calculate double-well driving force
            """
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.dw_drive[x,y] = prop_val.penal_barrier*(2.0*cell_val.phase_f[x,y]-6.0*cell_val.phase_f[x,y]**2+4.0*cell_val.phase_f[x,y]**3)

        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal, prop_val: PropVal, cell_val: CellVal) -> None:
            """
            Calculate double-well energy
            """
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.dw_energy[x,y] = prop_val.penal_barrier*cell_val.phase_f[x,y]**2*((1.0-cell_val.phase_f[x,y])**2)