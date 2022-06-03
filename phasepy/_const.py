"""
Summary
-------
Module on Constant

Update log
----------
At the final update date : 2022/06/03
"""

#********** Import major pakage or module **********
import math
import os

#********** Import orizinal module **********

#********** Constant Value **********
class MathConst():
    def __init__(self) -> None:
        self.PI = math.pi
        self.R_GAS = 8.3145
        self.WHITE_NUM = 255

class FileNam():
    def __init__(self) -> None:
        self.SET = "setting.txt"

class DirNam():
    def __init__(self) -> None:
        self.PYTHON = "phasepy"
        self.INPUT = "input"
        self.OUTPUT = "output"
        self.PROPERTY = "property"
        self.PARAM = "param"
        self.OUTDATA = "outdata"

class OutDirNam():
    def __init__(self) -> None:
        self.COND_NAM = "condition"
        self.SIMU_NAM = "simulation_"
        self.PHASE_IMG_NAM = "phase_img"
        self.PHASE_NPY_NAM = "phase_npy"
        self.TEM_IMG_NAM = "tem_img"
        self.TEM_NPY_NAM = "tem_npy"
        self.TEM_FLUCT_NAM = "fluct_npy"
        self.CHEM_ENE_NAM = "chem_npy"
        self.GRAD_ENE_NAM = "grad_npy"
    
    @property
    def OUT_DIR_LIST(self) -> list:
        return [self.PHASE_IMG_NAM, self.PHASE_NPY_NAM, self.TEM_IMG_NAM,
                self.TEM_NPY_NAM, self.TEM_FLUCT_NAM, self.CHEM_ENE_NAM, self.GRAD_ENE_NAM]

class MainPath():
    def __init__(self) -> None:
        self.MAIN_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        self.PYTHON_PATH = os.path.join(self.MAIN_PATH, DirNam().PYTHON)
        self.INPUT_PATH = os.path.join(self.MAIN_PATH, DirNam().INPUT)
        self.OUTPUT_PATH = os.path.join(self.MAIN_PATH, DirNam().OUTPUT)
        
class InputPath(MainPath):
    def __init__(self) -> None:
        super().__init__()
        self.SET_PATH = os.path.join(self.INPUT_PATH, FileNam().SET) 
        self.PROPERTY_PATH = os.path.join(self.INPUT_PATH, DirNam().PROPERTY)    
        self.PARAM_PATH = os.path.join(self.INPUT_PATH, DirNam().PARAM)
        self.OUTDATA_PATH = os.path.join(self.INPUT_PATH, DirNam().OUTDATA) 
