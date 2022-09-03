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

        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.chem_energy[x,y,0] = prop_val.k_s*cell_val.phase_f[x,y,0]**2*(prop_val.k_s1/2.0-prop_val.k_s2*cell_val.phase_f[x,y,0]/3.0
                                                +prop_val.k_s3*cell_val.phase_f[x,y,0]**2/4.0+prop_val.k_s4*cell_val.phase_f[x,y,1]**2/2.0)
                    cell_val.chem_energy[x,y,1] = prop_val.k_s*cell_val.phase_f[x,y,1]**2*(prop_val.k_s1/2.0-prop_val.k_s2*cell_val.phase_f[x,y,1]/3.0
                                                +prop_val.k_s3*cell_val.phase_f[x,y,1]**2/4.0+prop_val.k_s4*cell_val.phase_f[x,y,0]**2/2.0)

    class Gradient():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    for pf in prange(2):
                        cell_val.grad_drive[x,y,pf] = -1.0*prop_val.grad_coef*(cell_val.phase_f[simu_val.xp[x,y],y,pf]+cell_val.phase_f[simu_val.xm[x,y],y,pf]
                                                    +cell_val.phase_f[x,simu_val.yp[x,y],pf]+cell_val.phase_f[x,simu_val.ym[x,y],pf]-4.0*cell_val.phase_f[x,y,pf])
        
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    for pf in prange(2):
                        cell_val.grad_energy[x,y,pf] = prop_val.grad_coef/2.0*(cell_val.phase_f[simu_val.xp[x,y],y,pf]+cell_val.phase_f[simu_val.xm[x,y],y,pf]
                                                    +cell_val.phase_f[x,simu_val.yp[x,y],pf]+cell_val.phase_f[x,simu_val.ym[x,y],pf]-4.0*cell_val.phase_f[x,y,pf])**2


    class Elastic():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.elas_drive[:,:,:] = 0.0
            for i in prange(3):
                for j in prange(3):               
                    for k in prange(3):
                        for l in prange(3):
                            for pf in prange(2):
                                for x in prange(simu_val.xmax):
                                    for y in prange(simu_val.ymax):
                                        cell_val.elas_drive[x,y,pf] += 0.5*prop_val.c_matrix[simu_val.elas_c[i,j],simu_val.elas_c[k,l]]*(cell_val.ep_eigen[x,y,i,j]-cell_val.ep_eigen_ave[i,j]-cell_val.ep_hetero[x,y,i,j]-cell_val.ep_ex[i,j])*prop_val.ep_phase[k,l,pf]
                                        cell_val.elas_drive[x,y,pf] += 0.5*prop_val.c_matrix[simu_val.elas_c[i,j],simu_val.elas_c[k,l]]*(cell_val.ep_eigen[x,y,k,l]-cell_val.ep_eigen_ave[k,l]-cell_val.ep_hetero[x,y,k,l]-cell_val.ep_ex[k,l])*prop_val.ep_phase[i,j,pf]

        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.elas_energy[:,:,:] = 0.0
            for i in prange(3):
                for j in prange(3):               
                    for k in prange(3):
                        for l in prange(3):
                            for pf in prange(2):
                                for x in prange(simu_val.xmax):
                                    for y in prange(simu_val.ymax):
                                        cell_val.elas_energy[x,y,pf] += 0.5*prop_val.c_matrix[simu_val.elas_c[i,j],simu_val.elas_c[k,l]]*(cell_val.ep_eigen[x,y,i,j]-cell_val.ep_eigen_ave[i,j]-cell_val.ep_hetero[x,y,i,j]-cell_val.ep_ex[i,j])*(cell_val.ep_eigen[x,y,k,l]-cell_val.ep_eigen_ave[k,l]-cell_val.ep_hetero[x,y,k,l]-cell_val.ep_ex[k,l])
                        