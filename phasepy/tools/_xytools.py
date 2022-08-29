"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np
from numba import jit
import math

#********** Import original module **********

#********** Constant Value **********

@jit(nopython=True)
def xy_pm(xmax: int, ymax: int, xp: np.ndarray, xm: np.ndarray, yp: np.ndarray, ym: np.ndarray) -> tuple:
    for x in range(xmax):
        for y in range(ymax):
            if x == 0:
                xm[x,y] = xmax-1
                xp[x,y] = 1
            elif x == (xmax-1):
                xm[x,y] = xmax-2
                xp[x,y] = 0
            else:
                xm[x,y] = x-1
                xp[x,y] = x+1

            if y == 0:
                ym[x,y] = ymax-1
                yp[x,y] = 1
            elif y == (ymax-1):
                ym[x,y] = ymax-2
                yp[x,y] = 0
            else:
                ym[x,y] = y-1
                yp[x,y] = y+1

    return (xp, xm, yp, ym)

@jit(nopython=True)
def xy_rad(xmax: int, ymax: int, xk: np.ndarray, yk: np.ndarray, rad: np.ndarray) -> tuple:
    for x in range(xmax):
        for y in range(ymax):
            xk[x,y] = x - (xmax-1)/2.0
            yk[x,y] = y - (ymax-1)/2.0

            if x == (xmax-1)/2.0 and y == (ymax-1)/2.0:
                rad[x,y] = 0.0
            else:
                rad[x,y] = math.sqrt(xk[x,y]**2+yk[x,y]**2)

    return (xk, yk, rad)
