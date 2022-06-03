"""
Summary
-------
Module on input file

Update log
----------
At the final update date : 2022/06/03
"""

#********** Import major pakage or module **********
import numpy as np
import os

#********** Import orizinal module **********
from . import _const as const

#********** Constant Value **********
OUTDATA_PATH = const.InputPath().OUTDATA_PATH
PARAM_PATH = const.InputPath().PARAM_PATH
PROPERTY_PATH = const.InputPath().PROPERTY_PATH
SET_PATH = const.InputPath().SET_PATH

#********** Function **********
def _setting() -> list:
    """
    Input setting file.
    """
    param=[]
    with open(SET_PATH) as f:
        for s_line in f:
            if s_line[0] != "#":
                s_line = s_line.splitlines()[0]
                param.append(s_line)
    param[0] = os.path.join(PROPERTY_PATH, param[0])
    param[1] = os.path.join(PARAM_PATH, param[1])
    param[2] = os.path.join(OUTDATA_PATH, param[2])
    return param

def _property() -> np.ndarray:
    """
    Input material property file.
    """
    path = _setting()[0]
    param = np.loadtxt(path, dtype=float, comments="#")
    return param

def _param() -> np.ndarray:
    """
    Input simulation parameter file.
    """
    path = _setting()[1]
    param = np.loadtxt(path, dtype=float, comments="#")
    return param

def _outdata() -> np.ndarray:
    """
    Input related to how to output file.
    """
    path = _setting()[2]
    param = np.loadtxt(path, dtype=int, comments="#")
    return param


