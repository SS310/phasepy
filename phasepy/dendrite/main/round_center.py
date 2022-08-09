"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import sys

#********** Import original module **********
from ._base import Base

#********** Constant Value **********

#********** Class **********

class RoundCenter(Base):
    def __init__(self) -> None:
        super().__init__()

    def main(self):
        """
        Start **Center** model simulation

        See Also
        --------
        In the parent **main** owns the following routines

        - Monitoring of initial conditions
        - Declaration of Variables
        - Initialization of field variables
        - Saving Initial Conditions

        If you did not set key (input_path and output_path)
        
        ```python
        IndexError "< " + key + " > is not yet defined." 
        ```
        """
        super().main()

        #***** Start Simulation *****
        print("")
        print("********** Start Simulation **********")
        print("( First step is heavy becase of jit compile (< 30sec.))")

        for s in range(self.whole_val.simu_val.maxstep):
            step = s + 1

            self._update_field()
            self._calc_energy()

            if step % int(self.whole_val.simu_val.savestep/10) == 0:
                print("|", end="")
                sys.stdout.flush()

            if step % self.whole_val.simu_val.savestep == 0:
                self._save(step=step)
                print(" -> Completed Simulation : " + str(step) + " / " + str(self.whole_val.simu_val.maxstep))

        if self.whole_val.simu_val.maxstep % self.whole_val.simu_val.savestep != 0:
            self._save(step=self.whole_val.simu_val.maxstep)
            print(" -> Completed Simulation : " + str(self.whole_val.simu_val.maxstep) + " / " + str(self.whole_val.simu_val.maxstep))
