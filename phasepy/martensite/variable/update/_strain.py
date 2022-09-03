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

#********** Function **********

class Strain():
    """
    Calculate class for various strain
    """
    @staticmethod
    def calc_ep_ex(prop_val: PropVal, cell_val: CellVal) -> None:
        """
        Calculate strain due to external stress

        Parameter
        ---------
        prop_val: PropVal
            Variable about physical property
        cell_val: CellVal
            Array based on simulation's cell

        See Also
        --------
        - If you call this function, the value of < ep_ex > is calculated and updated.
        - Before this value can be calculated, < ex_stress > must be updated.
        - The value is updated, so no return value is needed.
        """ 
        # For x-, y-, and z-axis directions
        cell_val.ep_ex[0,0] = prop_val.s_11*cell_val.ex_stress[0,0] + prop_val.s_12*(cell_val.ex_stress[1,1]+cell_val.ex_stress[2,2])
        cell_val.ep_ex[1,1] = prop_val.s_11*cell_val.ex_stress[1,1] + prop_val.s_12*(cell_val.ex_stress[0,0]+cell_val.ex_stress[2,2])
        cell_val.ep_ex[2,2] = prop_val.s_11*cell_val.ex_stress[2,2] + prop_val.s_12*(cell_val.ex_stress[0,0]+cell_val.ex_stress[1,1])
        # For mixed x,y,z axis directions
        for i in range(3):
            for j in range(3):
                if i !=j:
                    cell_val.ep_ex[i,j] = prop_val.s_44*cell_val.ex_stress[i,j]

    # ----------------------------------------------------------------------------
    @staticmethod
    def calc_ep_eigen_ave(cell_val: CellVal) -> None:
        """
        Calculate avarege of eigen strain

        Parameter
        ---------
        cell_val: CellVal
            Array based on simulation's cell

        See Also
        --------
        - If you call this function, the value of < ep_eigen_ave > is calculated and updated.
        - Before this value can be calculated, < ep_eigen > must be updated.
        - The value is updated, so no return value is needed.
        """
        for i in range(3):
            for j in range(3):
                cell_val.ep_eigen_ave[i,j] = np.average(cell_val.ep_eigen[:,:,i,j])

    # ----------------------------------------------------------------------------
    @staticmethod
    def calc_ep_eigen_four(cell_val: CellVal) -> None:
        """
        Calculate eigen strain in fourie space

        Parameter
        ---------
        cell_val: CellVal
            Array based on simulation's cell

        See Also
        --------
        - If you call this function, the value of < ep_eigen_four > is calculated and updated.
        - Before this value can be calculated, < ep_eigen > must be updated.
        - The value is updated, so no return value is needed.
        - Updated with the low frequency region shifted to the center
        """ 
        for i in range(3):
            for j in range(3):
                # Fourie transform and center shift
                cell_val.ep_eigen_four[:,:,i,j] = np.fft.fft2(cell_val.ep_eigen[:,:,i,j])

    # ----------------------------------------------------------------------------
    @staticmethod
    def calc_ep_hetero(cell_val: CellVal) -> None:
        """
        Calculate heterogeneous strain

        Parameter
        ---------
        cell_val: CellVal
            Array based on simulation's cell

        See Also
        --------
        - If you call this function, the value of < ep_hetero > is calculated and updated.
        - Before this value can be calculated, < ep_hetero_four > must be updated.
        - The value is updated, so no return value is needed.
        - Shifted to the center
        """ 
        for i in range(3):
            for j in range(3):
                # Inverse fourie transform and center shift
                cell_val.ep_hetero[:,:,i,j] = np.real(np.fft.ifft2(cell_val.ep_hetero_four[:,:,i,j]))

    # ----------------------------------------------------------------------------
    @staticmethod
    @jit(nopython=True, parallel=True)
    def calc_ep_eigen(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
        """
        Calculate eigen strain

        Parameter
        ---------
        simu_val: SimuVal
            Variable about basical simulation parameter
        prop_val: PropVal
            Variable about physical property
        cell_val: CellVal
            Array based on simulation's cell

        See Also
        --------
        - If you call this function, values of < ep_eigen, ep_eigen_grad > is calculated and updated.
        - The value is updated, so no return value is needed.
        - Use jit (parallel computation).
        """ 
        # < prange > is used in jit's parallel computation
        for i in prange(3):
            for j in range(3):                
                for x in prange(simu_val.xmax):
                    for y in prange(simu_val.ymax):
                        cell_val.ep_eigen[x,y,i,j] = prop_val.ep_phase[i,j,0]*cell_val.phase_f[x,y,0]+prop_val.ep_phase[i,j,1]*cell_val.phase_f[x,y,1]


    # ----------------------------------------------------------------------------
    @staticmethod
    @jit(nopython=True, parallel=True)
    def calc_ep_hetero_four(simu_val: SimuVal ,prop_val: PropVal, cell_val: CellVal) -> None:
        """
        Calculate heterogeneous strain in fourie space

        Parameter
        ---------
        simu_val: SimuVal
            Variable about basical simulation parameter
        prop_val: PropVal
            Variable about physical property
        cell_val: CellVal
            Array based on simulation's cell

        See Also
        --------
        - If you call this function, the value of < ep_hetero_four > is calculated and updated.
        - The value is updated, so no return value is needed.
        - Use jit (parallel computation).
        """ 
        # < prange > is used in jit's parallel computation
        for x in prange(simu_val.xmax):
            for y in prange(simu_val.ymax):
                # Calculation of the real part
                real_data = ((simu_val.nxx[x,y]*(2.0*(1.0-prop_val.nu0)-simu_val.nxx[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nyy[x,y])/(1.0-2.0*prop_val.nu0))*np.real(cell_val.ep_eigen_four[x,y,0,0]) 
                            + (simu_val.nxx[x,y]*(2.0*prop_val.nu0-simu_val.nyy[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nxx[x,y])/(1.0-2.0*prop_val.nu0))*np.real(cell_val.ep_eigen_four[x,y,1,1]))
                # Calculation of the imaginary part
                imag_data = 1.0j*((simu_val.nxx[x,y]*(2.0*(1.0-prop_val.nu0)-simu_val.nxx[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nyy[x,y])/(1.0-2.0*prop_val.nu0))*np.imag(cell_val.ep_eigen_four[x,y,0,0]) 
                            + (simu_val.nxx[x,y]*(2.0*prop_val.nu0-simu_val.nyy[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nxx[x,y])/(1.0-2.0*prop_val.nu0))*np.imag(cell_val.ep_eigen_four[x,y,1,1]))
                cell_val.ep_hetero_four[x,y,0,0] = real_data + imag_data

                # Calculation of the real part
                real_data = ((simu_val.nyy[x,y]*(2.0*prop_val.nu0-simu_val.nxx[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nyy[x,y])/(1.0-2.0*prop_val.nu0))*np.real(cell_val.ep_eigen_four[x,y,0,0])
                            + (simu_val.nyy[x,y]*(2.0*(1.0-prop_val.nu0)-simu_val.nyy[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nxx[x,y])/(1.0-2.0*prop_val.nu0))*np.real(cell_val.ep_eigen_four[x,y,1,1]))
                # Calculation of the imaginary part
                imag_data = 1.0j*((simu_val.nyy[x,y]*(2.0*prop_val.nu0-simu_val.nxx[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nyy[x,y])/(1.0-2.0*prop_val.nu0))*np.imag(cell_val.ep_eigen_four[x,y,0,0])
                            + (simu_val.nyy[x,y]*(2.0*(1.0-prop_val.nu0)-simu_val.nyy[x,y]-prop_val.nu0/(1.0-prop_val.nu0)*simu_val.nxx[x,y])/(1.0-2.0*prop_val.nu0))*np.imag(cell_val.ep_eigen_four[x,y,1,1]))
                cell_val.ep_hetero_four[x,y,1,1] = real_data + imag_data