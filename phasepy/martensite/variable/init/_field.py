"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np

#********** Import orizinal module **********
from phasepy.martensite.variable.define._var import SimuVal, CellVal

#********** Constant Value **********

class InitField():
    @staticmethod
    def toward_center(simu_val: SimuVal, cell_val: CellVal) -> None:
        # Create random metal structure
        _Phase.rand(simu_val=simu_val, cell_val=cell_val)
        print("Random metal structure variable were successfully created. -> ", end="")


#********** Internal function **********

class _Phase():
	@staticmethod
	def rand(simu_val: SimuVal, cell_val: CellVal) -> None:
		for x in range(simu_val.xmax):
			for y in range(simu_val.ymax):
				# Set random value (0~1)
				cell_val.phase_f[x,y,0] = np.random.rand()
				cell_val.phase_f[x,y,1] = 1.0 - cell_val.phase_f[x,y,0]