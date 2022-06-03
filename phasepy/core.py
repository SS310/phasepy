"""
Summary
-------
Main module

Update log
----------
At the final update date : 2022/06/03
"""

#********** Import major pakage or module **********
import math
import numpy as np

#********** Import orizinal module **********
from . import _output as output
from . import _input as input
from . import _init_func as init_func
from . import _calc_func as calc_func

from . import _const as const

#********** Constant Value **********
PI = const.MathConst().PI

#********** Main Routine **********

def simple():
    """
    This is the solidification simulation of metallographic structures.
    """
    #********** Setting **********
    # Input material property
    param: np.ndarray = input._property()
    tem_cond: float = param[0]              # Thermal Conductivity [W/mK]
    spec_heat: float = param[1]             # Specific Heat [J/Km^3]
    lat_heat: float = param[2]              # Latent Heat [J/m^3]
    melt_tem: float = param[3]              # Melting Point [K]
    inter_kine: float = param[4]            # Interface Kinetic Coefficient [m/Ks]
    anis_num: float = param[5]              # Anisotropic number of directions
    glow_angle: float = param[6]            # Angle of priority growth direction
    cell_size: float = param[7]             # Cell size [m]
    inter_w: float = param[8]*cell_size     # Interfacial Width
    inter_e: float = param[9]               # Interface Energy
    lam: float = param[10]                  # Lambda
    anis_str: float = param[11]             # Anisotropic strength
    supercool_tem: float = param[12]        # Supercooling temperature [K]
    nois: float = param[13]                 # Noise amplitude

    # Input simulation parameter
    param = input._param()
    x_cell: int = int(param[0])         # Number of cells (x)
    y_cell: int = int(param[1])         # Number of cells (y)
    max_step: int = int(param[2])       # Max step time
    save_step: int = int(param[3])      # Saving time step
    nuc_size: float = param[4]          # Size of the initial nucleus

    # Culcurate parameter to use input
    si_ta_glow = (2.0*PI)*(glow_angle/360)                                  # Convert angles to radians
    inter_cf = 2.0*math.log((1.0+(1.0-2.0*lam))/(1.0-(1.0-2.0*lam)))/2.0    # Coefficients for interface width
    grad_e_cf = math.sqrt(3.0*inter_w*inter_e/inter_cf)                     # Gradient energy coefficient
    penal_barrier = 6.0*inter_e*inter_cf/inter_w                            # Energy barrier for penalty term
    mob = inter_cf*melt_tem*inter_kine/(3.0*inter_w*lat_heat)               # Mobility

    # Determine time step
    dt1 = cell_size**2/(5.0*mob*grad_e_cf**2)
    dt2 = cell_size**2/(5.0*tem_cond/spec_heat)
    delt = min(dt1, dt2)

    # Initializing Cell-Dependent Variables
    phase_f = np.zeros((y_cell, x_cell))    # Phase field variable
    tem_f = np.zeros((y_cell, x_cell))      # Temperature field
    grad_e = np.zeros((y_cell, x_cell))     # Gradient energy
    chem_e = np.zeros((y_cell, x_cell))     # Chemical energy
    tem_fluct = np.zeros((y_cell, x_cell))  # Thermal fluctuations
    
    # Make outputting environment
    new_out_path, outdata_param = output._mk_output()

    print("Making output file at [ " + new_out_path + " ] is success !!")
    
    print("***** Finish setteing *****")

    #********** Start simulation **********
    # Setting the initial field
    print("***** Start simulation *****")

    # Setting initial conditions
    phase_f, tem_f = init_func._init_set(phase_f=phase_f, tem_f=tem_f, nuc_size=nuc_size,
                                        supercool_tem=supercool_tem, melt_tem=melt_tem)

    # Save initial conditions
    output._save_output(new_out_path=new_out_path, step_cnt=0, melt_tem=melt_tem,
                        supercool_tem=supercool_tem, phase_f=phase_f, tem_f=tem_f,
                        outdata_param=outdata_param, tem_fluct=tem_fluct, chem_e=chem_e, grad_e=grad_e)

    # Repeat according to max_step
    for cnt in range(max_step):
        step_cnt = cnt + 1

        # Calculate Thermal fluctuations
        tem_fluct = calc_func._calc_fluct(phase_f=phase_f, tem_fluct=tem_fluct,
                                        penal_barrier=penal_barrier, nois=nois)
        
        # Calculate chemical energy
        chem_e = calc_func._calc_chem(phase_f=phase_f, tem_f=tem_f, chem_e=chem_e,
                                    penal_barrier=penal_barrier, melt_tem= melt_tem, lat_heat=lat_heat)

        # Calculate gradient energy
        grad_e = calc_func._calc_grad(phase_f=phase_f, grad_e=grad_e, si_ta_glow=si_ta_glow,
                                    grad_e_cf=grad_e_cf, anis_str=anis_str, anis_num=anis_num, cell_size=cell_size)

        # Update Phase field variable and Temperture feild
        phase_f, tem_f = calc_func._update(phase_f=phase_f, tem_f=tem_f, mob=mob, tem_fluct=tem_fluct,
                                        chem_e=chem_e, grad_e=grad_e, delt=delt, cell_size=cell_size,
                                        tem_cond=tem_cond, lat_heat=lat_heat, spec_heat=spec_heat)

        # Save conditions according to save_step
        if step_cnt % save_step == 0:
            output._save_output(new_out_path=new_out_path, step_cnt=step_cnt, melt_tem=melt_tem,
                                supercool_tem=supercool_tem, phase_f=phase_f, tem_f=tem_f,
                                outdata_param=outdata_param, tem_fluct=tem_fluct, chem_e=chem_e, grad_e=grad_e)
            print("Finish saving " + str(step_cnt) + "/" + str(max_step) + " STEP")

    # Save final conditions
    if max_step % save_step != 0:
        output._save_output(new_out_path=new_out_path, step_cnt=max_step, melt_tem=melt_tem,
                            supercool_tem=supercool_tem, phase_f=phase_f, tem_f=tem_f,
                            outdata_param=outdata_param, tem_fluct=tem_fluct, chem_e=chem_e, grad_e=grad_e)

    print("***** Finish simulation *****")