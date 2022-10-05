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
from phasepy._const import MathConst

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

        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.chem_energy[x,y] = prop_val.k_s*((prop_val.k_s1/2.0)*(cell_val.phase_f[x,y,0]**2+cell_val.phase_f[x,y,1]**2)-prop_val.k_s2/3.0*(cell_val.phase_f[x,y,0]**3+cell_val.phase_f[x,y,1]**3)+\
                                                prop_val.k_s3/4.0*(cell_val.phase_f[x,y,0]**4+cell_val.phase_f[x,y,1]**4)+prop_val.k_s4/2.0*(cell_val.phase_f[x,y,0]**2*cell_val.phase_f[x,y,1]**2))

    class Gradient():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    for pf in prange(2):
                        cell_val.grad_drive[x,y,pf] = -1.0*prop_val.grad_coef*((cell_val.phase_f[simu_val.xp[x,y],y,pf]+cell_val.phase_f[simu_val.xm[x,y],y,pf]-2.0*cell_val.phase_f[x,y,pf])/(simu_val.xsize**2)+\
                                                                               (cell_val.phase_f[x,simu_val.yp[x,y],pf]+cell_val.phase_f[x,simu_val.ym[x,y],pf]-2.0*cell_val.phase_f[x,y,pf])/(simu_val.ysize**2))
        
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.grad_energy[x,y] = prop_val.grad_coef/2.0*(((cell_val.phase_f[simu_val.xp[x,y],y,0]-cell_val.phase_f[simu_val.xm[x,y],y,0])/(2.0*simu_val.xsize))*2+\
                                                                        ((cell_val.phase_f[x,simu_val.yp[x,y],0]-cell_val.phase_f[x,simu_val.ym[x,y],0])/(2.0*simu_val.ysize))**2+\
                                                                        ((cell_val.phase_f[simu_val.xp[x,y],y,1]-cell_val.phase_f[simu_val.xm[x,y],y,1])/(2.0*simu_val.xsize))**2+\
                                                                        ((cell_val.phase_f[x,simu_val.yp[x,y],1]-cell_val.phase_f[x,simu_val.ym[x,y],1])/(2.0*simu_val.ysize))**2)


    class Elastic():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_drive(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.elas_drive[:,:,:] = 0.0
            for n in range(81):
                i = simu_val.elas_81to3333[n,0]
                j = simu_val.elas_81to3333[n,1]
                k = simu_val.elas_81to3333[n,2]
                l = simu_val.elas_81to3333[n,3]
                ij = simu_val.elas_81to66[n,1]
                kl = simu_val.elas_81to66[n,2]
                for pf in prange(2):
                    for x in prange(simu_val.xmax):
                        for y in prange(simu_val.ymax):
                            cell_val.elas_drive[x,y,pf] += 0.5*prop_val.c_matrix[ij,kl]*(cell_val.ep_eigen[x,y,i,j]-cell_val.ep_eigen_ave[i,j]-cell_val.ep_hetero[x,y,i,j]-cell_val.ep_ex[i,j])*prop_val.ep_phase[k,l,pf]
                            cell_val.elas_drive[x,y,pf] += 0.5*prop_val.c_matrix[ij,kl]*(cell_val.ep_eigen[x,y,k,l]-cell_val.ep_eigen_ave[k,l]-cell_val.ep_hetero[x,y,k,l]-cell_val.ep_ex[k,l])*prop_val.ep_phase[i,j,pf]

        
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.elas_energy[:,:] = 0.0
            for n in range(81):
                i = simu_val.elas_81to3333[n,0]
                j = simu_val.elas_81to3333[n,1]
                k = simu_val.elas_81to3333[n,2]
                l = simu_val.elas_81to3333[n,3]
                ij = simu_val.elas_81to66[n,1]
                kl = simu_val.elas_81to66[n,2]
                for x in prange(simu_val.xmax):
                    for y in prange(simu_val.ymax):
                        cell_val.elas_energy[x,y] += 0.5*prop_val.c_matrix[ij,kl]*(cell_val.ep_eigen[x,y,i,j]-cell_val.ep_eigen_ave[i,j]-cell_val.ep_hetero[x,y,i,j]-cell_val.ep_ex[i,j])*(cell_val.ep_eigen[x,y,k,l]-cell_val.ep_eigen_ave[k,l]-cell_val.ep_hetero[x,y,k,l]-cell_val.ep_ex[k,l])
                        

class MagneEnergy():
    class Exchange():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def _calc_h_routine(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal, magne_f: np.ndarray) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    for mf in prange(3):
                        cell_val.h_dummy[x,y,mf] = 2.0*prop_val.exch_coef/(prop_val.mu0*prop_val.m_s**2)*((magne_f[simu_val.xp[x,y],y,mf]+magne_f[simu_val.xm[x,y],y,mf]-2.0*magne_f[x,y,mf])/(simu_val.xsize**2)+\
                                                                                                         (magne_f[x,simu_val.yp[x,y],mf]+magne_f[x,simu_val.ym[x,y],mf]-2.0*magne_f[x,y,mf])/(simu_val.ysize**2))
            return cell_val.h_dummy

        @staticmethod
        def calc_h(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_exch = MagneEnergy.Exchange._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f)

        @staticmethod
        def calc_h_star(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_star_exch = MagneEnergy.Exchange._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f_star)

        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.exch_energy[x,y] = prop_val.exch_coef*(((cell_val.magne_f[simu_val.xp[x,y],y,0]-cell_val.magne_f[simu_val.xm[x,y],y,0])/(2.0*simu_val.xsize))**2+\
                                                                    ((cell_val.magne_f[x,simu_val.yp[x,y],0]-cell_val.magne_f[x,simu_val.ym[x,y],0])/(2.0*simu_val.ysize))**2+\
                                                                    ((cell_val.magne_f[simu_val.xp[x,y],y,1]-cell_val.magne_f[simu_val.xm[x,y],y,1])/(2.0*simu_val.xsize))**2+\
                                                                    ((cell_val.magne_f[x,simu_val.yp[x,y],1]-cell_val.magne_f[x,simu_val.ym[x,y],1])/(2.0*simu_val.ysize))**2+\
                                                                    ((cell_val.magne_f[simu_val.xp[x,y],y,2]-cell_val.magne_f[simu_val.xm[x,y],y,2])/(2.0*simu_val.xsize))**2+\
                                                                    ((cell_val.magne_f[x,simu_val.yp[x,y],2]-cell_val.magne_f[x,simu_val.ym[x,y],2])/(2.0*simu_val.ysize))**2)
    
    # --------------------
    class MagnetoStatic():
        @staticmethod
        def _calc_h_routine(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal, magne_f: np.ndarray, magne_f_four: np.ndarray) -> None:
            for mf in range(3):
                magne_f_four[:,:,mf] = np.fft.fft2(magne_f[:,:,mf])
            
            MagneEnergy.MagnetoStatic._calc_phi(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f_four=magne_f_four)    
        
            cell_val.phi[:,:] = np.real(np.fft.ifft2(cell_val.phi_four[:,:]))

            MagneEnergy.MagnetoStatic._calc_h_dummy(simu_val=simu_val, cell_val=cell_val) 

            for mf in range(3):
                cell_val.h_dummy[:,:,mf] += -1.0*prop_val.m_s*np.sum(magne_f[:,:,mf])*prop_val.n_shape[mf]

            return cell_val.h_dummy
        
        @staticmethod
        @jit(nopython=True, parallel=True)
        def _calc_phi(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal, magne_f_four: np.ndarray) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    real_data =       prop_val.m_s*(np.imag(magne_f_four[x,y,0])*simu_val.xk[x,y]+np.imag(magne_f_four[x,y,1])*simu_val.yk[x,y])/(simu_val.alnn[x,y]**2)
                    imag_data = -1.0j*prop_val.m_s*(np.real(magne_f_four[x,y,0])*simu_val.xk[x,y]+np.real(magne_f_four[x,y,1])*simu_val.yk[x,y])/(simu_val.alnn[x,y]**2)
                    cell_val.phi_four[x,y] = real_data + imag_data

        @staticmethod
        @jit(nopython=True, parallel=True)
        def _calc_h_dummy(simu_val: SimuVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.h_dummy[:,:,0] = -1.0*(cell_val.phi[simu_val.xp[x,y],y]-cell_val.phi[simu_val.xm[x,y],y])/2.0
                    cell_val.h_dummy[:,:,1] = -1.0*(cell_val.phi[x,simu_val.yp[x,y]]-cell_val.phi[x,simu_val.ym[x,y]])/2.0
                    cell_val.h_dummy[:,:,2] = 0.0

        @staticmethod
        def calc_h(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_ms = MagneEnergy.MagnetoStatic._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f, magne_f_four=cell_val.magne_f_four)

        @staticmethod
        def calc_h_star(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_star_ms = MagneEnergy.MagnetoStatic._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f_star, magne_f_four=cell_val.magne_f_star_four)

        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.ms_energy[x,y] = -0.5*prop_val.mu0*prop_val.m_s*(cell_val.h_ms[x,y,0]*cell_val.magne_f[x,y,0]+cell_val.h_ms[x,y,1]*cell_val.magne_f[x,y,1]+cell_val.h_ms[x,y,2]*cell_val.magne_f[x,y,2])
    
    # --------------------
    class Anisotropy():
        @staticmethod
        @jit(nopython=True, parallel=True)
        def _calc_h_routine(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal, magne_f: np.ndarray) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.h_dummy[x,y,0] = -1.0/prop_val.mu0*(2.0*prop_val.k_1*(magne_f[x,y,0]*magne_f[x,y,1]**2+magne_f[x,y,2]**2*magne_f[x,y,0])+\
                                                                2.0*prop_val.k_2*(magne_f[x,y,0]*magne_f[x,y,1]**2*magne_f[x,y,2]**2))
                    cell_val.h_dummy[x,y,1] = -1.0/prop_val.mu0*(2.0*prop_val.k_1*(magne_f[x,y,1]*magne_f[x,y,2]**2+magne_f[x,y,0]**2*magne_f[x,y,1])+\
                                                                2.0*prop_val.k_2*(magne_f[x,y,0]**2*magne_f[x,y,1]*magne_f[x,y,2]**2))
                    cell_val.h_dummy[x,y,2] = -1.0/prop_val.mu0*(2.0*prop_val.k_1*(magne_f[x,y,2]*magne_f[x,y,0]**2+magne_f[x,y,1]**2*magne_f[x,y,2])+\
                                                                2.0*prop_val.k_2*(magne_f[x,y,0]**2*magne_f[x,y,1]**2*magne_f[x,y,2]))
            return cell_val.h_dummy

        @staticmethod
        def calc_h(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_anis = MagneEnergy.Anisotropy._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f)

        @staticmethod
        def calc_h_star(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_star_anis = MagneEnergy.Anisotropy._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f_star)


        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.anis_energy[x,y] = prop_val.k_1*(cell_val.magne_f[x,y,0]**2*cell_val.magne_f[x,y,1]**2+cell_val.magne_f[x,y,1]**2*cell_val.magne_f[x,y,2]**2+cell_val.magne_f[x,y,2]**2*cell_val.magne_f[x,y,0]**2)+\
                                                prop_val.k_2*(cell_val.magne_f[x,y,0]**2*cell_val.magne_f[x,y,1]**2*cell_val.magne_f[x,y,2]**2)

    # --------------------
    class MagnetoElastic():
        @staticmethod
        @jit(nopython=True)
        def _calc_h_routine(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal, magne_f: np.ndarray) -> None:
            for x in range(simu_val.xmax):
                for y in range(simu_val.ymax):
                    cell_val.h_dummy[x,y,0] = prop_val.me_coef_1*(2.0*cell_val.ep_eigen[x,y,0,0]*magne_f[x,y,0]+3.0*prop_val.ramda[0,0]*magne_f[x,y,0])+\
                                              prop_val.me_coef_2*(cell_val.ep_eigen[x,y,0,1]*magne_f[x,y,1]+cell_val.ep_eigen[x,y,2,0]*magne_f[x,y,2]+1.5*prop_val.ramda[0,1]*magne_f[x,y,1]+1.5*prop_val.ramda[2,0]*magne_f[x,y,2])
                    cell_val.h_dummy[x,y,1] = prop_val.me_coef_1*(2.0*cell_val.ep_eigen[x,y,1,1]*magne_f[x,y,1]+3.0*prop_val.ramda[1,1]*magne_f[x,y,1])+\
                                              prop_val.me_coef_2*(cell_val.ep_eigen[x,y,1,2]*magne_f[x,y,2]+cell_val.ep_eigen[x,y,0,1]*magne_f[x,y,0]+1.5*prop_val.ramda[1,2]*magne_f[x,y,2]+1.5*prop_val.ramda[0,1]*magne_f[x,y,0])
                    cell_val.h_dummy[x,y,2] = prop_val.me_coef_1*(2.0*cell_val.ep_eigen[x,y,2,2]*magne_f[x,y,2]+3.0*prop_val.ramda[2,2]*magne_f[x,y,2])+\
                                              prop_val.me_coef_2*(cell_val.ep_eigen[x,y,2,0]*magne_f[x,y,0]+cell_val.ep_eigen[x,y,1,2]*magne_f[x,y,1]+1.5*prop_val.ramda[2,0]*magne_f[x,y,0]+1.5*prop_val.ramda[1,2]*magne_f[x,y,1])


                    return cell_val.h_dummy

        @staticmethod
        def calc_h(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_me = MagneEnergy.MagnetoElastic._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f)

        @staticmethod
        def calc_h_star(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            cell_val.h_star_me = MagneEnergy.MagnetoElastic._calc_h_routine(simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, magne_f=cell_val.magne_f_star)

        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.me_energy[x,y] = prop_val.me_coef_1*(cell_val.ep_eigen[x,y,0,0]*(cell_val.magne_f[x,y,0]**2-1.0/3.0)+cell_val.ep_eigen[x,y,1,1]*(cell_val.magne_f[x,y,1]**2-1.0/3.0)+cell_val.ep_eigen[x,y,2,2]*(cell_val.magne_f[x,y,2]**2-1.0/3.0))+\
                                              prop_val.me_coef_2*(cell_val.ep_eigen[x,y,0,1]*cell_val.magne_f[x,y,0]*cell_val.magne_f[x,y,1]+cell_val.ep_eigen[x,y,1,2]*cell_val.magne_f[x,y,1]*cell_val.magne_f[x,y,2]+cell_val.ep_eigen[x,y,2,0]*cell_val.magne_f[x,y,2]*cell_val.magne_f[x,y,0])

    # --------------------
    class Zeeman():        
        @staticmethod
        @jit(nopython=True, parallel=True)
        def calc_energy(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
            for x in prange(simu_val.xmax):
                for y in prange(simu_val.ymax):
                    cell_val.zeeman_energy[x,y] = -1.0*prop_val.mu0*prop_val.m_s*(cell_val.h_zeeman[0]*cell_val.magne_f[x,y,0]+cell_val.h_zeeman[1]*cell_val.magne_f[x,y,1]+cell_val.h_zeeman[2]*cell_val.magne_f[x,y,2])

