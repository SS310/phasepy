"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np

#********** Import original module **********

#********** Constant Value **********


class InitArray():
    def __init__(self, xmax: int, ymax: int) -> None:
        self.xmax: int = int(xmax)
        self.ymax: int = int(ymax)
        
        self.i4_xy: np.ndarray = np.zeros((self.xmax,self.ymax), dtype="int32")
        self.i4_33: np.ndarray = np.zeros((3,3), dtype="int32")
        self.f4_xy: np.ndarray = np.zeros((self.xmax,self.ymax), dtype="float32")
        self.c16_xy: np.ndarray = np.zeros((self.xmax,self.ymax), dtype="complex128")
        self.c16_xy2: np.ndarray = np.zeros((self.xmax,self.ymax,2), dtype="complex128")
        self.c16_xy3: np.ndarray = np.zeros((self.xmax,self.ymax,3), dtype="complex128")
        self.c16_xy33: np.ndarray = np.zeros((self.xmax,self.ymax,3,3), dtype="complex128")
        self.i4_812: np.ndarray = np.zeros((81,2), dtype="int32")
        self.i4_814: np.ndarray = np.zeros((81,4), dtype="int32")
        
        