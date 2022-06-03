"""
Summary
-------
Module on output file

Update log
----------
At the final update date : 2022/06/03
"""

#********** Import major pakage or module **********
import os
import shutil
import numpy as np
import cv2

#********** Import orizinal module **********
from . import _const as const
from . import _input as input

#********** Constant Value **********
OUTPUT_PATH = const.MainPath().OUTPUT_PATH

OUTDATA_PATH = const.InputPath().OUTDATA_PATH
PARAM_PATH = const.InputPath().PARAM_PATH
PROPERTY_PATH = const.InputPath().PROPERTY_PATH
SET_PATH = const.InputPath().SET_PATH

COND_NAM = const.OutDirNam().COND_NAM
SIMU_NAM = const.OutDirNam().SIMU_NAM

OUT_DIR_LIST = const.OutDirNam().OUT_DIR_LIST

WHITE_NUM = const.MathConst().WHITE_NUM

#********** Function **********
def _mk_output() -> any:
    """
    Output directory processing summary function
    """
    new_out_path = __mk_output_main()
    __cp_input(new_out_path=new_out_path)
    outdata_param = __mk_outdata(new_out_path=new_out_path)

    return new_out_path, outdata_param

def _save_output(new_out_path: str, step_cnt :int, melt_tem: float, supercool_tem: float,
                phase_f: np.ndarray, tem_f: np.ndarray, outdata_param: np.ndarray,
                tem_fluct: np.ndarray, chem_e: np.ndarray, grad_e: np.ndarray) -> None:
    """
    Saving statement processing summary function
    """
    png_nam = "data_" + str(step_cnt) + ".png"
    npy_nam = "data_" + str(step_cnt) + ".npy"

    data = [phase_f, phase_f, tem_f, tem_f, tem_fluct, chem_e, grad_e]

    for i in range(len(outdata_param)):
        if outdata_param[i] == 0:
            if i == 0:
                data[i] = data[i]*WHITE_NUM
                path = os.path.join(new_out_path, OUT_DIR_LIST[i], png_nam)
                cv2.imwrite(path, data[i])
            elif i == 2:
                data[i] = (melt_tem-data[i])/(melt_tem-supercool_tem)*WHITE_NUM
                path = os.path.join(new_out_path, OUT_DIR_LIST[i], png_nam)
                cv2.imwrite(path, data[i])
            else:
                path = os.path.join(new_out_path, OUT_DIR_LIST[i], npy_nam)
                np.save(path, data[i])
    
#********** Internal Function **********
def __mk_output_main() -> str:
    """
    Creation of parent directory of output directory
    """
    out_num = 1
    while True:
        new_out_path = os.path.join(OUTPUT_PATH, SIMU_NAM + str(out_num))
        if os.path.exists(new_out_path) == False:
            os.mkdir(new_out_path)
            break
        out_num+=1
    return new_out_path


def __mk_outdata(new_out_path: str) -> np.ndarray:
    """
    Creation of child directory of output directory into the parent directory
    """
    outdata_param = input._outdata()
    
    for i in range(len(outdata_param)):
        if outdata_param[i] == 0:
            os.mkdir(os.path.join(new_out_path, OUT_DIR_LIST[i]))
    
    return outdata_param

def __cp_input(new_out_path: str) -> None:
    """
    Save a copy of the input condition into the output directory
    """
    cond_path = os.path.join(new_out_path, COND_NAM)
    os.mkdir(cond_path)

    param = input._setting()
    for i in range(len(param)):
        shutil.copy2(param[i], os.path.join(cond_path, os.path.basename(param[i])))


    
    
