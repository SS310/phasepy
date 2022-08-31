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
    ('nxx', types.f4[:,:]),
    ('nyy', types.f4[:,:]),
]
@jitclass(spec=spec1)
class SimuVal():
    """
    Variable about basical simulation parameter
    """
    def __init__(self, simulation_parameter: typed.Dict, i4_xy: np.ndarray, f4_xy: np.ndarray) -> None:
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
        self.nxx: np.ndarray = np.copy(f4_xy)
        """Special variables for fourier transform"""
        self.nyy: np.ndarray = np.copy(f4_xy)
        """Special variables for fourier transform"""

        # ---------------------
        # Calculating Variables
        (self.xp, self.xm, self.yp, self.ym) = xy_pm(xmax=self.xmax, ymax=self.ymax, xp=self.xp, xm=self.xm, yp=self.yp, ym=self.ym)
        (self.xr, self.yr, self.rad) = xy_rad(xmax=self.xmax, ymax=self.ymax, xr=self.xr, yr=self.yr, rad=self.rad)
        (self.xk, self.yk, self.nxx, self.nyy) = xy_four(xmax=self.xmax, ymax=self.ymax, xk=self.xk, yk=self.yk, nxx=self.nxx, nyy=self.nyy)

# ----------------------------------------------------------
# spec2 is type-list of PropertyVal for the jitclass
spec2 = [
    ('k_s', types.f8),
    ('phase_strain', types.f8),
    ('c_11', types.f8),
    ('c_12', types.f8),
    ('c_44', types.f8),
    ('grad_coef', types.f8),
    ('mob', types.f8),
    ('fluct', types.f8),
    ('nu0', types.f8),
    ('s_11', types.f8),
    ('s_12', types.f8),
    ('s_44', types.f8),
    ('ep_phase', types.f8[:,:,:]),
    ('k_s1', types.f4),
    ('k_s2', types.f4),
    ('k_s3', types.f4),
    ('k_s4', types.f4),
]
@jitclass(spec=spec2)
class PropVal():
    """
    Variable about physical property
    """
    def __init__(self, material_property: typed.Dict) -> None:
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
        """Driving force of metamorphosis""" # default=1.65e+8, unit=J/m^3
        self.phase_strain: types.f8 = types.f8(material_property["phase_strain"])
        """Metamorphic strain""" # default=0.034, unit=None
        self.c_11: types.f8 = types.f8(material_property["c_11"])
        """Elastic tensor coefficient of cubic crystal""" # default=1.6e+11, unit=N/m^2
        self.c_12: types.f8 = types.f8(material_property["c_12"])
        """Elastic tensor coefficient of cubic crystal""" # default=1.52e+11, unit=N/m^2
        self.c_44: types.f8 = types.f8(material_property["c_44"])
        """Elastic tensor coefficient of cubic crystal""" # default=0.43e+11, unit=N/m^2
        self.grad_coef: types.f8 = types.f8(material_property["grad_coef"])
        """Gradient energy coefficient""" # default=6.2e+7, unit=J/m^3
        self.mob: types.f8 = types.f8(material_property["mob"])
        """Mobility(Relaxation coefficient of crystal transformation)""" # default=1.0e-9, unit=None
        self.fluct: types.f8 = types.f8(material_property["fluct"])
        """Fluctuation coefficient of crystal transformation""" # default=0.01, unit=None
        # SETTING-MATERIAL-PROPERTY-FINISH

        # -----------------------------------
        # Externally unconfigurable variables
        self.c_12 = self.c_11 + 2.0*self.c_44

        self.nu0: types.f8 = self.c_12/(2.0*(self.c_12+self.c_44))
        """Poisson's ratio"""
        self.s_11: types.f8 = (self.c_12+self.c_44)/self.c_44/(3.0*self.c_12+2.0*self.c_44)
        """Elastic compliance tensor coefficient of cubic crystal"""
        self.s_12: types.f8 = -0.5*self.c_12/self.c_44/(3.0*self.c_12+2.0*self.c_44)
        """Elastic compliance tensor coefficient of cubic crystal"""
        self.s_44: types.f8 = 1.0/self.c_44
        """Elastic compliance tensor coefficient of cubic crystal"""
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
        self.ep_phase[0,0,1] = self.ep_phase[2,2,0] = self.phase_strain/2.0

# ----------------------------------------------------------
# spec3 is type-list of CellVal for the jitclass
spec3 = [
    ('phase_f', types.f8[:,:,:]),
    ('chem_drive', types.f8[:,:,:]),
    ('grad_drive', types.f8[:,:,:]),
    ('elas_drive', types.f8[:,:,:]),
    ('chem_energy', types.f8[:,:,:]),
    ('grad_energy', types.f8[:,:,:]),
    ('elas_energy', types.f8[:,:,:]),
    ('ep_eigen', types.f8[:,:,:,:]),
    ('ep_eigen_ave', types.f8[:,:]),
    ('ep_ex', types.f8[:,:]),
    ('ep_hetero', types.f8[:,:,:]),
    ('ex_stress', types.f8[:,:]),
    ('ep_hetero_four', types.c16[:,:,:]),
    ('ep_eigen_four', types.c16[:,:,:,:]),
    ('drive_four', types.c16[:,:,:]),
    ('phase_four', types.c16[:,:,:]),
    ('phase_af_four', types.c16[:,:,:]),
]
@jitclass(spec=spec3)
class CellVal():
    """
    Array based on simulation's cell
    """
    def __init__(self, xmax: int, ymax: int,
                c16_xy33: np.ndarray, c16_xy2: np.ndarray) -> None:
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
        self.chem_energy: np.ndarray  = np.zeros((xmax,ymax,2))
        """Chemical energy of metal structure""" # default=False, unit=bool
        self.grad_energy: np.ndarray  = np.zeros((xmax,ymax,2))
        """Gradient energy of metal structure""" # default=False, unit=bool
        self.elas_energy: np.ndarray  = np.zeros((xmax,ymax,2))
        """Elastic energy of metal structure""" # default=False, unit=bool
        self.ep_eigen: np.ndarray = np.zeros((xmax,ymax,3,3))
        """Eigen strain""" # default=False, unit=bool
        self.ep_eigen_ave: np.ndarray = np.zeros((3,3))
        """Average of eigen strain""" # default=False, unit=bool
        self.ep_ex: np.ndarray = np.zeros((3,3))
        """Strain due to external stress""" # default=False, unit=bool
        self.ep_hetero: np.ndarray = np.zeros((xmax,ymax,2))
        """Heterogeneous strain""" # default=False, unit=bool
        self.ex_stress: np.ndarray = np.zeros((3,3))
        """External stress""" # default=False, unit=bool
        # SETTING-OUTPUT-PARAMETER-FINISH

        # -------------------------------------------------
        # Variables required during the calculation process
        self.ep_hetero_four: np.ndarray = np.copy(c16_xy2)
        """Heterogeneous strain in fourie space"""
        self.ep_eigen_four: np.ndarray = np.copy(c16_xy33)
        """Eigen strain in fourie space"""
        self.drive_four: np.ndarray = np.copy(c16_xy2)
        """Driving force in fourie space"""
        self.phase_four: np.ndarray = np.copy(c16_xy2)
        """Phase field variable in fourie space"""
        self.phase_af_four: np.ndarray = np.copy(c16_xy2)
        """Phase field variable in fourie space"""