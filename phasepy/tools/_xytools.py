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
def xy_rad(xmax: int, ymax: int, xr: np.ndarray, yr: np.ndarray, rad: np.ndarray) -> tuple:
    for x in range(xmax):
        for y in range(ymax):
            xr[x,y] = x - (xmax-1)/2.0
            yr[x,y] = y - (ymax-1)/2.0

            if x == (xmax-1)/2.0 and y == (ymax-1)/2.0:
                rad[x,y] = 0.0
            else:
                rad[x,y] = math.sqrt(xr[x,y]**2+yr[x,y]**2)

    return (xr, yr, rad)

@jit(nopython=True)
def xy_four(xmax: int, ymax: int, xk: np.ndarray, yk: np.ndarray, nxx: np.ndarray, nyy: np.ndarray) -> tuple:
    """
    Able to compute Fourier coordinates
    
    See Also
    --------
    In numpy, wavenumbers in fourier space is treated in comparison to real space coordinates as follows

    - Odd number

    | Real  | 0| 1| 2| 3| 4|
    |-------|--|--|--|--|--|
    |Fourier| 0| 1| 2|-2|-1|
    
    - Even number

    | Real  | 0| 1| 2| 3| 4| 5|
    |-------|--|--|--|--|--|--|
    |Fourier| 0| 1| 2| 3|-2|-1|
    """
    for x in range(xmax):
        for y in range(ymax):
            if x <= xmax/2.0:
                xk[x,y] = x
            else:
                xk[x,y] = x-xmax
            
            if y <= ymax/2.0:
                yk[x,y] = y
            else:
                yk[x,y] = y-xmax

            alnn = math.sqrt(xk[x,y]*xk[x,y]+yk[x,y]*yk[x,y])
            if alnn == 0.0:
                alnn = 1.0

            nxx[x,y] = (xk[x,y]/alnn)*(xk[x,y]/alnn)
            nyy[x,y] = (yk[x,y]/alnn)*(yk[x,y]/alnn)

    return (xk, yk, nxx, nyy)