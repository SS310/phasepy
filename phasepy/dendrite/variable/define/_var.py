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
import math

#********** Import orizinal module **********
from phasepy.tools._xytools import xy_pm, xy_rad
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
    ('xp', types.i4[:,:]),
    ('xm', types.i4[:,:]),
    ('yp', types.i4[:,:]),
    ('ym', types.i4[:,:]),
    ('xr', types.f4[:,:]),
    ('yr', types.f4[:,:]),
    ('rad', types.f4[:,:]),
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
        """x of cell size""" # default=30e-9, unit=m
        self.ysize: types.f8 = types.f8(simulation_parameter["ysize"])
        """y of cell size""" # default=30e-9, unit=m
        self.maxstep: types.i8 = types.i8(simulation_parameter["maxstep"])
        """Max step of simulation""" # default=3000, unit=None
        self.savestep: types.i4 = types.i4(simulation_parameter["savestep"])
        """Decide how many times you get output""" # default=100, unit=None
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

        # ---------------------
        # Calculating Variables
        (self.xp, self.xm, self.yp, self.ym) = xy_pm(xmax=self.xmax, ymax=self.ymax, xp=self.xp, xm=self.xm, yp=self.yp, ym=self.ym)
        (self.xr, self.yr, self.rad) = xy_rad(xmax=self.xmax, ymax=self.ymax, xr=self.xr, yr=self.yr, rad=self.rad)      

# ----------------------------------------------------------
# spec2 is type-list of PropertyVal for the jitclass
spec2 = [
    ('tem_cond', types.f8),
    ('spec_heat', types.f8), 
    ('lat_heat', types.f8),
    ('melt_tem', types.f8),
    ('inter_kine_coef', types.f8),
    ('anis_num', types.f8),
    ('inter_w_coef', types.f8),
    ('inter_e', types.f8),
    ('lam', types.f8),
    ('anis_str', types.f8),
    ('supercool_tem', types.f8),
    ('nois', types.f8),
    ('grow_direct', types.f8),
    ('grow_sita', types.f8),
    ('inter_w', types.f8),
    ('inter_coef', types.f8),
    ('grad_coef', types.f8),
    ('penal_barrier', types.f8),
    ('mob', types.f8),
    ('delt', types.f8),
]
@jitclass(spec=spec2)
class PropVal():
    """
    Variable about physical property
    """
    def __init__(self, material_property: typed.Dict, xsize: float, ysize: float, PI = MathConst.PI) -> None:
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
        self.tem_cond: types.f8 = types.f8(material_property["tem_cond"])
        """Thermal conductivity""" # default=84.01, unit=W/mK
        self.spec_heat: types.f8 = types.f8(material_property["spec_heat"])
        """Specific heat""" # default=5.42e+6, unit=J/Km^3
        self.lat_heat: types.f8 = types.f8(material_property["lat_heat"])
        """Latent heat""" # default=2.35e+9, unit=J/m^3
        self.melt_tem: types.f8 = types.f8(material_property["melt_tem"])
        """Melting point (Temperture)""" # default=1728.0, unit=K
        self.inter_kine_coef: types.f8 = types.f8(material_property["inter_kine_coef"])
        """Interface kinetic cofficient""" # default=2.0, unit=m/Ks
        self.anis_num: types.f8 = types.f8(material_property["anis_num"])
        """Anisotropic number of directions""" # default=4.0, unit=None
        self.inter_w_coef: types.f8 = types.f8(material_property["inter_w_coef"])
        """Interface width (Factor for cell size)""" # default=3.0, unit=None
        self.inter_e: types.f8 = types.f8(material_property["inter_e"])
        """Interface energy""" # default=0.37, unit=J/m2
        self.lam: types.f8 = types.f8(material_property["lam"])
        """Lambda""" # default=0.1, unit=None
        self.anis_str: types.f8 = types.f8(material_property["anis_str"])
        """Anisotropic strength""" # default=0.01, unit=None
        self.supercool_tem: types.f8 = types.f8(material_property["supercool_tem"])
        """Supercooling temperture""" # default=1511.2, unit=K
        self.nois: types.f8 = types.f8(material_property["nois"])
        """Noise amplitude""" # default=0.1, unit=None
        self.grow_direct: types.f8 = types.f8(material_property["grow_direct"])
        """Anisotropic growth direction (normal angle from x-axis, expressed as 0 ~ 90)""" # default=0.0, unit=None
        # SETTING-MATERIAL-PROPERTY-FINISH

        # -----------------------------------
        # Externally unconfigurable variables
        self.grow_sita: types.f8 = (self.grow_direct/360)*(2.0*PI)
        """Anisotropic growth direction (normal angle from x-axis, expressed as 0 ~ π/2)"""
        self.inter_w: types.f8 = self.inter_w_coef*((xsize+ysize)/2.0)
        """Interface width"""
        self.inter_coef: types.f8 = 2.0*math.log((1.0+(1.0-2.0*self.lam))/(1.0-(1.0-2.0*self.lam)))/2.0
        """Coefficients for interface width"""
        self.grad_coef: types.f8 = math.sqrt(3.0*self.inter_w*self.inter_e/self.inter_coef)
        """Gradient energy coefficient"""
        self.penal_barrier: types.f8 = 6.0*self.inter_e*self.inter_coef/self.inter_w
        """Energy barrier for penalty term"""
        self.mob: types.f8 = self.inter_coef*self.melt_tem*self.inter_kine_coef/(3.0*self.inter_w*self.lat_heat)
        """Mobility"""

        dt1: types.f8 = (xsize*ysize)/(5.0*self.mob*self.grad_coef**2)
        dt2: types.f8 = (xsize*ysize)/(5.0*self.tem_cond/self.spec_heat)
        self.delt: types.f8 = min(dt1, dt2)
        """Clock tick (The smaller, the more accurate)"""

# ----------------------------------------------------------
# spec3 is type-list of CellVal for the jitclass
spec3 = [
    ('phase_f', types.f8[:,:]),
    ('tem_f', types.f8[:,:]),
    ('chem_energy', types.f8[:,:]),
    ('grad_energy', types.f8[:,:]),
    ('tem_fluct', types.f8[:,:]),
    ('chem_drive', types.f8[:,:]),
    ('grad_drive', types.f8[:,:]),
]
@jitclass(spec=spec3)
class CellVal():
    """
    Array based on simulation's cell
    """
    def __init__(self, xmax: int, ymax: int) -> None:
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
        self.phase_f: np.ndarray = np.zeros((xmax,ymax))
        """Phase field variable""" # default=False, unit=bool
        self.tem_f: np.ndarray = np.zeros((xmax,ymax))
        """Temperture field""" # default=False, unit=bool
        self.grad_energy: np.ndarray = np.zeros((xmax,ymax))
        """Gradient energy""" # default=False, unit=bool
        self.chem_energy: np.ndarray = np.zeros((xmax,ymax))
        """Chemical energy""" # default=False, unit=bool
        self.tem_fluct: np.ndarray = np.zeros((xmax,ymax))
        """Thermal fluctuations""" # default=False, unit=bool
        self.grad_drive: np.ndarray = np.zeros((xmax,ymax))
        """Gradient driving force""" # default=False, unit=bool
        self.chem_drive: np.ndarray = np.zeros((xmax,ymax))
        """Chemical driving force""" # default=False, unit=bool
        # SETTING-OUTPUT-PARAMETER-FINISH

        # -------------------------------------------------
        # Variables required during the calculation process