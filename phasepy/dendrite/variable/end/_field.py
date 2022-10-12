"""
Summary
-------
Module on determination of end of variable

See Also
--------

"""

#********** Import major pakage or module **********
from numba import jit, prange

#********** Import orizinal module **********
from phasepy.dendrite.variable.define._var import SimuVal, PropVal, CellVal
from phasepy.dendrite.variable.define._model import *

#********** Constant Value **********

#********** Function **********

class Convergence():
    def round_center(simu_val: SimuVal, cell_val: CellVal, model_val: RoundCenterModel) -> int:
        return _ConvergenceTools.max_growth(simu_val=simu_val, cell_val=cell_val, max_rate=model_val.max_rate)
    

class _ConvergenceTools():
    @staticmethod
    @jit(nopython=True, parallel=True)
    def max_growth(simu_val: SimuVal, cell_val: CellVal, max_rate: float) -> None:
        """
        Judged by the size of the maximum growth area from the center

        Parameter
        ---------
        max_rate: float(0~1)


        Return
        ------
        1 : End
        0 : Continue
        """
        max_distance = max_rate*(simu_val.xmax/2.0+simu_val.ymax/2.0)/2.0

        for x in prange(simu_val.xmax):
            for y in prange(simu_val.ymax):
                if simu_val.rad[x,y] >= max_distance:
                    if cell_val.phase_f[x,y] >= 0.5:
                        return 1
        return 0

