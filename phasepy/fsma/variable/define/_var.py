"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np
from numba.experimental import jitclass
from numba import types, typed

#********** Import orizinal module **********
from phasepy.tools._xytools import xy_pm, xy_rad, xy_four
from phasepy._const import MathConst

#********** Constant Value **********


#********** Class **********
# ----------------------------------------------------------
# spec1 is type-list of SimuVal for the jitclass
spec1 = [
    ('xmax', types.i4), 
    ('ymax', types.i4),
    ('xsize', types.f8),
    ('ysize', types.f8),
    ('maxstep', types.i8),
    ('savestep', types.i4),
    ('delt', types.f4),
    ('xp', types.i4[:,:]),
    ('xm', types.i4[:,:]),
    ('yp', types.i4[:,:]),
    ('ym', types.i4[:,:]),
    ('xr', types.f4[:,:]),
    ('yr', types.f4[:,:]),
    ('rad', types.f4[:,:]),
    ('xk', types.f4[:,:]),
    ('yk', types.f4[:,:]),
    ('alnn', types.f4[:,:]),
    ('nxx', types.f4[:,:]),
    ('nyy', types.f4[:,:]),
    ('elas_81to66', types.i4[:,:]),
    ('elas_81to3333', types.i4[:,:])
]
@jitclass(spec=spec1)
class SimuVal():
    """
    Variable about basical simulation parameter
    """
    def __init__(self, simulation_parameter: typed.Dict, i4_xy: np.ndarray, f4_xy: np.ndarray, 
                i4_814: np.ndarray, i4_812: np.ndarray) -> None:
        """
        Variable about simulation basic parameter
        """
        # Externally configurable variables
        """
        Set the variable according to the following

        variable: variable-type = Initialization
        ```Explain for variable``` # default=1.0, unit=m/s

        - default is the initial value of variable        
        - unit is physical units
        """
        # SETTING-SIMULATION-PARAMETER-START   
        self.xmax: types.i4 = types.i4(simulation_parameter["xmax"])
        """x of cell amount""" # default=256, unit=None
        self.ymax: types.i4 = types.i4(simulation_parameter["ymax"])
        """y of cell amount""" # default=256, unit=None
        self.xsize: types.f8 = types.f8(simulation_parameter["xsize"])
        """x of cell size""" # default=18e-9, unit=m
        self.ysize: types.f8 = types.f8(simulation_parameter["ysize"])
        """y of cell size""" # default=18e-9, unit=N/m
        self.maxstep: types.i8 = types.i8(simulation_parameter["maxstep"])
        """Max step of simulation""" # default=3000, unit=None
        self.savestep: types.i4 = types.i4(simulation_parameter["savestep"])
        """Decide how many times you get output""" # default=100, unit=None
        self.delt: types.f4 = types.f4(simulation_parameter["delt"])
        """Clock tick (The smaller, the more accurate)""" # default=0.1, unit=None
        # SETTING-SIMULATION-PARAMETER-FINISH
        
        # -----------------------------------
        # Externally unconfigurable variables
        self.xp: np.ndarray = np.copy(i4_xy)
        """Array of x+1"""
        self.xm: np.ndarray = np.copy(i4_xy)
        """Array of x-1"""
        self.yp: np.ndarray = np.copy(i4_xy)
        """Array of y+1"""
        self.ym: np.ndarray = np.copy(i4_xy)
        """Array of y-1"""
        self.xr: np.ndarray = np.copy(f4_xy)
        """Array of x-(xmax-1)/2"""
        self.yr: np.ndarray = np.copy(f4_xy)
        """Array of y-(ymax-1)/2""" 
        self.rad: np.ndarray = np.copy(f4_xy)
        """Array of radius"""
        self.xk: np.ndarray = np.copy(f4_xy)
        """Array of wavenumbers in fourier space"""
        self.yk: np.ndarray = np.copy(f4_xy)
        """Array of wavenumbers in fourier space""" 
        self.alnn: np.ndarray = np.copy(f4_xy)
        """Squrt of wavenumbers in fourier space""" 
        self.nxx: np.ndarray = np.copy(f4_xy)
        """Special variables for fourier transform"""
        self.nyy: np.ndarray = np.copy(f4_xy)
        """Special variables for fourier transform"""
        self.elas_81to66: np.ndarray = np.copy(i4_814)
        """Special variables for elastic tensor"""
        self.elas_81to3333: np.ndarray = np.copy(i4_812)
        """Special variables for elastic tensor"""


        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        n = l + 3*k + 9*j + 27*i
                        self.elas_81to3333[n,0] = i
                        self.elas_81to3333[n,1] = j
                        self.elas_81to3333[n,2] = k
                        self.elas_81to3333[n,3] = l
                        if i == j:
                            self.elas_81to66[n,0] = i
                        else:
                            self.elas_81to66[n,0] = 6-(i+j)
                        if k == l:
                            self.elas_81to66[n,1] = k
                        else:
                            self.elas_81to66[n,1] = 6-(k+l)


        # ---------------------
        # Calculating Variables
        (self.xp, self.xm, self.yp, self.ym) = xy_pm(xmax=self.xmax, ymax=self.ymax, xp=self.xp, xm=self.xm, yp=self.yp, ym=self.ym)
        (self.xr, self.yr, self.rad) = xy_rad(xmax=self.xmax, ymax=self.ymax, xr=self.xr, yr=self.yr, rad=self.rad)
        (self.xk, self.yk, self.alnn, self.nxx, self.nyy) = xy_four(xmax=self.xmax, ymax=self.ymax, xk=self.xk, yk=self.yk, alnn=self.alnn, nxx=self.nxx, nyy=self.nyy)

# ----------------------------------------------------------
# spec2 is type-list of PropertyVal for the jitclass
spec2 = [
    ('k_s', types.f8),
    ('phase_strain', types.f8),
    ('c_11', types.f8),
    ('c_12', types.f8),
    ('c_44', types.f8),
    ('grad_coef', types.f8),
    ('p_mob', types.f8),
    ('fluct', types.f8),
    ('alpha', types.f8),
    ('m_s', types.f8), 
    ('k_1', types.f8),
    ('k_2', types.f8),
    ('exch_coef', types.f8),
    ('me_coef_1', types.f8),
    ('me_coef_2', types.f8),
    ('m_mob', types.f8),
    ('nu0', types.f8),
    ('s_11', types.f8),
    ('s_12', types.f8),
    ('s_44', types.f8),
    ('ep_phase', types.f8[:,:,:]),
    ('k_s1', types.f4),
    ('k_s2', types.f4),
    ('k_s3', types.f4),
    ('k_s4', types.f4),
    ('c_matrix', types.f8[:,:]),
    ('s_matrix', types.f8[:,:]),
    ('mu0', types.f8),
    ('ramda_100', types.f8),
    ('ramda_111', types.f8),
    ('exch_coef_star', types.f8),
    ('n_shape', types.f8[:]),
    ('ramda', types.f8[:,:]),
]
@jitclass(spec=spec2)
class PropVal():
    """
    Variable about physical property
    """
    def __init__(self, material_property: typed.Dict,xsize: float, ysize: float, MU0: float = MathConst.MU0) -> None:
        """
        Variable about physical property
        """
        # Externally configurable variables
        """
        Set the variable according to the following

        variable: variable-type = Initialization
        ```Explain for variable``` # default=1.0, unit=m/s

        - default is the initial value of variable        
        - unit is physical units
        """
        # SETTING-MATERIAL-PROPERTY-START
        self.k_s: types.f8 = types.f8(material_property["k_s"])
        """Driving force of metamorphosis""" # default=1.55e+8, unit=J/m^3
        self.phase_strain: types.f8 = types.f8(material_property["phase_strain"])
        """Metamorphic strain""" # default=0.034, unit=None
        self.c_11: types.f8 = types.f8(material_property["c_11"])
        """Elastic tensor coefficient of cubic crystal""" # default=1.6e+11, unit=N/m^2
        self.c_12: types.f8 = types.f8(material_property["c_12"])
        """Elastic tensor coefficient of cubic crystal""" # default=1.52e+11, unit=N/m^2
        self.c_44: types.f8 = types.f8(material_property["c_44"])
        """Elastic tensor coefficient of cubic crystal""" # default=0.43e+11, unit=N/m^2
        self.grad_coef: types.f8 = types.f8(material_property["grad_coef"])
        """Gradient energy coefficient""" # default=2.0e+7, unit=J/m^3
        self.p_mob: types.f8 = types.f8(material_property["p_mob"])
        """Mobility(Relaxation coefficient of crystal transformation)""" # default=6.0e-8, unit=None
        self.fluct: types.f8 = types.f8(material_property["fluct"])
        """Fluctuation coefficient of crystal transformation""" # default=0.01, unit=None
        self.alpha: types.f8 = types.f8(material_property["alpha"])
        """Magnetic damping constant""" # default=1.5, unit=None
        self.m_s: types.f8 = types.f8(material_property["m_s"])
        """Saturation of magnetization""" # default=1.65e+5, unit=A/m
        self.k_1: types.f8 = types.f8(material_property["k_1"])
        """Anisotropic constant""" # default=2.7e+3, unit=J/m^3
        self.k_2: types.f8 = types.f8(material_property["k_2"])
        """Anisotropic constant""" # default=-6.1e+3, unit=J/m^3
        self.exch_coef: types.f8 = types.f8(material_property["exch_coef"])
        """Exchange energy coefficient""" # default=2.0e-11, unit=J/m
        self.me_coef_1: types.f8 = types.f8(material_property["me_coef_1"])
        """Magnetoelastic energy cofficient""" # default=4.0e+6, unit=J/m^3
        self.me_coef_2: types.f8 = types.f8(material_property["me_coef_2"])
        """Magnetoelastic energy cofficient""" # default=0.0, unit=J/m^3
        self.m_mob: types.f8 = types.f8(material_property["m_mob"])
        """Mobility(Relaxation coefficient of magnetic moment)""" # default=1.0e-6, unit=Non
        # SETTING-MATERIAL-PROPERTY-FINISH

        # -----------------------------------
        # Externally unconfigurable variables
        self.c_11 = self.c_12 + 2.0*self.c_44

        self.nu0: types.f8 = self.c_12/(2.0*(self.c_12+self.c_44))
        """Poisson's ratio"""
        self.ep_phase: np.ndarray = np.zeros((3,3,2))
        """Metamorphic strain"""

        self.k_s1: types.f4 = 1.0
        """Driving force of metamorphosis cofficient"""
        self.k_s2: types.f4 = 3.0*self.k_s1+12.0
        """Driving force of metamorphosis cofficient"""
        self.k_s3: types.f4 = 2.0*self.k_s1+12.0
        """Driving force of metamorphosis cofficient"""
        self.k_s4: types.f4 = 2.0*self.k_s1+12.0
        """Driving force of metamorphosis cofficient"""
  
        self.ep_phase[0,0,0] = -1.0*self.phase_strain
        self.ep_phase[1,1,0] = self.ep_phase[2,2,0] = self.phase_strain/2.0

        self.ep_phase[1,1,1] = -1.0*self.phase_strain
        self.ep_phase[0,0,1] = self.ep_phase[2,2,1] = self.phase_strain/2.0

        self.c_matrix: np.ndarray = np.zeros((6,6))
        """Elastic tensor coefficient of cubic crystal"""
        self.s_matrix: np.ndarray = np.zeros((6,6))
        """Elastic compliance tensor coefficient of cubic crystal"""

        for i in range(6):
            for j in range(6):
                if i == j:
                    if (i == 0) or  (i == 1) or (i == 2):
                        self.c_matrix[i,j] = self.c_11
                    else:
                        self.c_matrix[i,j] = self.c_44
                elif (i <= 2) and (j <= 2):
                    self.c_matrix[i,j] = self.c_12
            
        self.s_matrix = np.linalg.inv(self.c_matrix)

        self.s_11: types.f8 = self.s_matrix[0,0]
        """Elastic compliance tensor coefficient of cubic crystal"""
        self.s_12: types.f8 = self.s_matrix[0,1]
        """Elastic compliance tensor coefficient of cubic crystal"""
        self.s_44: types.f8 = self.s_matrix[3,3]
        """Elastic compliance tensor coefficient of cubic crystal"""


        self.mu0: types.f8 = MU0
        """Permeability of vacuum"""

        self.exch_coef_star: types.f8 = 2.0*self.exch_coef/(self.mu0*self.m_s**2*xsize*ysize)
        """Standardized exchange energy coefficient"""
        
        self.ramda_100: types.f8 = (2.0/3.0)*(self.me_coef_1/(self.c_12-self.c_11))
        """Magnetostriction constant""" 
        self.ramda_111: types.f8 = (-1.0/3.0)*(self.me_coef_2/self.c_44)
        """Magnetostriction constant""" 


        self.n_shape: np.ndarray = np.zeros(3)
        """Coefficient of antimagnetic field"""

        self.n_shape[0] = 0.0
        self.n_shape[1] = 0.0
        self.n_shape[2] = 1.0

        self.ramda: np.ndarray = np.zeros((3,3))
        """Magnetostriction constant array"""

        for i in range(3):
            for j in range(3):
                # For x-, y-, and z-axis directions
                if i == j:
                    self.ramda[i,j] = self.ramda_100
                # For mixed x,y,z axis directions
                else:
                    self.ramda[i,j] = self.ramda_111

# ----------------------------------------------------------
# spec3 is type-list of CellVal for the jitclass
spec3 = [
    ('phase_f', types.f8[:,:,:]),
    ('chem_drive', types.f8[:,:,:]),
    ('grad_drive', types.f8[:,:,:]),
    ('elas_drive', types.f8[:,:,:]),
    ('chem_energy', types.f8[:,:]),
    ('grad_energy', types.f8[:,:]),
    ('elas_energy', types.f8[:,:]),
    ('ep_eigen', types.f8[:,:,:,:]),
    ('ep_eigen_p', types.f8[:,:,:,:]),
    ('ep_eigen_ave', types.f8[:,:]),
    ('ep_ex', types.f8[:,:]),
    ('ep_hetero', types.f8[:,:,:,:]),
    ('ex_stress', types.f8[:,:]),
    ('ep_hetero_four', types.c16[:,:,:,:]),
    ('ep_eigen_four', types.c16[:,:,:,:]),
    ('magne_f', types.f8[:,:,:]),
    ('h_ms', types.f8[:,:,:]),
    ('h_exch', types.f8[:,:,:]),
    ('h_anis', types.f8[:,:,:]),
    ('h_me', types.f8[:,:,:]),
    ('h_zeeman', types.f8[:]),
    ('ms_energy', types.f8[:,:]),
    ('exch_energy', types.f8[:,:]),
    ('anis_energy', types.f8[:,:]),
    ('me_energy', types.f8[:,:]),
    ('zeeman_energy', types.f8[:,:]),
    ('ep_eigen_m', types.f8[:,:,:,:]),
    ('magne_f_four', types.c16[:,:,:]),
    ('phi', types.f8[:,:]),
    ('phi_four', types.c16[:,:]),
    ('h', types.f8[:,:,:]),
    ('h_four', types.c16[:,:,:]),
    ('g', types.f8[:,:,:]),
    ('g_four', types.c16[:,:,:]),
    ('g_star', types.f8[:,:,:]),
    ('g_star_four', types.c16[:,:,:]),
    ('magne_f_star', types.f8[:,:,:]),
    ('magne_f_star2', types.f8[:,:,:]),
    ('magne_f_star_four', types.c16[:,:,:]),
    ('magne_f_star2_four', types.c16[:,:,:]),
    ('h_star_ms', types.f8[:,:,:]),
    ('h_star_exch', types.f8[:,:,:]),
    ('h_star_anis', types.f8[:,:,:]),
    ('h_star_me', types.f8[:,:,:]),
    ('h_star', types.f8[:,:,:]),
    ('h_star_four', types.c16[:,:,:]),
    ('h_dummy', types.f8[:,:,:]),
]
@jitclass(spec=spec3)
class CellVal():
    """
    Array based on simulation's cell
    """
    def __init__(self, xmax: int, ymax: int, c16_xy: np.ndarray,
                c16_xy33: np.ndarray, c16_xy3: np.ndarray) -> None:
        """
        Array based on simulation's cell
        """
        # Variables that can retrieve arrays
        """
        Set the variable according to the following

        variable: variable-type = Initialization
        ```Explain for variable``` # default=False, unit=bool

        - default is the initial value of whether to get that variable or not        
        - unit is physical units
        """
        # SETTING-OUTPUT-PARAMETER-START
        self.phase_f: np.ndarray = np.zeros((xmax,ymax,2))
        """Field variable of metal structure""" # default=False, unit=bool
        self.chem_drive: np.ndarray  = np.zeros((xmax,ymax,2))
        """Chemical driving force of metal structure""" # default=False, unit=bool
        self.grad_drive: np.ndarray  = np.zeros((xmax,ymax,2))
        """Gradient driving force of metal structure""" # default=False, unit=bool
        self.elas_drive: np.ndarray  = np.zeros((xmax,ymax,2))
        """Elastic driving force of metal structure""" # default=False, unit=bool
        self.chem_energy: np.ndarray  = np.zeros((xmax,ymax))
        """Chemical energy of metal structure""" # default=False, unit=bool
        self.grad_energy: np.ndarray  = np.zeros((xmax,ymax))
        """Gradient energy of metal structure""" # default=False, unit=bool
        self.elas_energy: np.ndarray  = np.zeros((xmax,ymax))
        """Elastic energy of metal structure""" # default=False, unit=bool
        self.ep_eigen_p: np.ndarray = np.zeros((xmax,ymax,3,3))
        """Eigen strain of metamorphosis""" # default=False, unit=bool
        self.ep_eigen: np.ndarray = np.zeros((xmax,ymax,3,3))
        """Eigen strain (metamorphosis + magnetic-moment)""" # default=False, unit=bool
        self.ep_eigen_ave: np.ndarray = np.zeros((3,3))
        """Average of eigen strain""" # default=False, unit=bool
        self.ep_ex: np.ndarray = np.zeros((3,3))
        """Strain due to external stress""" # default=False, unit=bool
        self.ep_hetero: np.ndarray = np.zeros((xmax,ymax,3,3))
        """Heterogeneous strain""" # default=False, unit=bool
        self.ex_stress: np.ndarray = np.zeros((3,3))
        """External stress""" # default=False, unit=bool
        self.magne_f: np.ndarray = np.zeros((xmax,ymax,3))
        """Field variable of magnetic domain""" # default=False, unit=bool
        self.h_ms: np.ndarray = np.zeros((xmax,ymax,3))
        """Magnetostatic magnetic field of magnetic domain""" # default=False, unit=bool
        self.h_exch: np.ndarray = np.zeros((xmax,ymax,3))
        """Exchange magnetic field of magnetic domain""" # default=False, unit=bool
        self.h_anis: np.ndarray = np.zeros((xmax,ymax,3))
        """Anisotropy magnetic field of magnetic domain""" # default=False, unit=bool
        self.h_me: np.ndarray = np.zeros((xmax,ymax,3))
        """Magnetoelastic magnetic field of magnetic domain""" # default=False, unit=bool
        self.h_zeeman: np.ndarray = np.zeros(3)
        """Zeeman magnetic field of magnetic domain""" # default=False, unit=bool
        self.ms_energy: np.ndarray = np.zeros((xmax,ymax))
        """Magnetostatic energy of magnetic domain""" # default=False, unit=bool
        self.exch_energy: np.ndarray = np.zeros((xmax,ymax))
        """Exchange energy of magnetic domain""" # default=False, unit=bool
        self.anis_energy: np.ndarray = np.zeros((xmax,ymax))
        """Anisotropy energy of magnetic domain""" # default=False, unit=bool
        self.me_energy: np.ndarray = np.zeros((xmax,ymax))
        """Magnetoelastic energy of magnetic domain""" # default=False, unit=bool
        self.zeeman_energy: np.ndarray = np.zeros((xmax,ymax))
        """Zeeman energy of magnetic domain""" # default=False, unit=bool
        self.ep_eigen_m: np.ndarray = np.zeros((xmax,ymax,3,3))
        """Eigen strain of magnetic moment""" # default=False, unit=bool
        # SETTING-OUTPUT-PARAMETER-FINISH

        # -------------------------------------------------
        # Variables required during the calculation process
        self.ep_hetero_four: np.ndarray = np.copy(c16_xy33)
        """Heterogeneous strain in fourie space"""
        self.ep_eigen_four: np.ndarray = np.copy(c16_xy33)
        """Eigen strain in fourie space"""

        self.magne_f_four: np.ndarray = np.copy(c16_xy3)
        """Field variable of magnetic domain in fourie space"""
        self.phi: np.ndarray = np.zeros((xmax,ymax))
        """Variable for magnetostatic energy"""
        self.phi_four: np.ndarray = np.copy(c16_xy)
        """Variable for magnetostatic energy in fourie space"""

        self.h: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for Magnetic field of magnetic domain"""
        self.h_four: np.ndarray = np.copy(c16_xy3)
        """Variable for Magnetic field of magnetic domain in fourie space"""

        self.g: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for magnetic field of magnetic domain"""
        self.g_four: np.ndarray = np.copy(c16_xy3)
        """Variable for magnetic field of magnetic domain in fourie space"""  
        self.g_star: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for magnetic field of magnetic domain"""
        self.g_star_four: np.ndarray = np.copy(c16_xy3)
        """Variable for magnetic field of magnetic domain in fourie space"""  

        self.magne_f_star: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for magnetic moment"""
        self.magne_f_star2: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for magnetic moment"""
        
        self.magne_f_star_four: np.ndarray = np.copy(c16_xy3)
        """Variable for magnetic moment in fourie space"""
        self.magne_f_star2_four: np.ndarray = np.copy(c16_xy3)
        """Variable for magnetic moment in fourie space"""

        self.h_star_ms: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for Magnetostatic magnetic field of magnetic domain"""
        self.h_star_exch: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for Exchange magnetic field of magnetic domain"""
        self.h_star_anis: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for Anisotropy magnetic field of magnetic domain"""
        self.h_star_me: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for Magnetoelastic magnetic field of magnetic domain"""

        self.h_star: np.ndarray = np.zeros((xmax,ymax,3))
        """Variable for Magnetic field of magnetic domain"""
        self.h_star_four: np.ndarray = np.copy(c16_xy3)
        """Variable for Magnetic field of magnetic domain in fourie space"""

        self.h_dummy: np.ndarray = np.zeros((xmax,ymax,3))
        """Dummy variable for Magnetostatic magnetic field of magnetic domain"""
