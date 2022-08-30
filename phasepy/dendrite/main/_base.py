"""
Summary
-------

See Also
----------

"""

#********** Import major pakage or module **********
import sys

#********** Import original module **********
from phasepy.dendrite.variable.define._whole import WholeVal
from phasepy.tools._path import PathTools, Counter
from phasepy._const import SetPathKey, SimulationModelKey
from phasepy.dendrite._const import OutputDir
from phasepy.tools._save import SaveTools
from phasepy.dendrite.variable.update._energy import PhaseEnergy
from phasepy.dendrite.variable.update._field import UpdateFeild
from phasepy.dendrite.variable.init._field import InitField

#********** Constant Value **********

class Base():
    def __init__(self) -> None:
        self.__whole_val: WholeVal = WholeVal(class_name=self.__class__.__name__)

    def main(self) -> None:
        """
        Start simularion

        The parent **main** owns the following routines

        - Monitoring of initial conditions
        - Declaration of Variables
        - Initialization of field variables
        - Saving Initial Conditions

        See Also
        --------
        If you did not set key (input_path and output_path)
        
        ```python
        IndexError "< " + key + " > is not yet defined." 
        ```
        """
        print("")
        print("********** Initialization of magnetic domain and metal structure **********")

        # Monitoring of initial conditions
        print("Monitoring of initial conditions -> ", end="")
        sys.stdout.flush()
        self.__check_counter()
        print("Done")

        # Declaration of Variables(Very heavy because of jit)
        print("Declaration of Variables(Very heavy because of jit) -> ", end="")
        sys.stdout.flush()
        self.__whole_val.set()
        print("Done")

        # Initialization of field variables
        print("Initialization of field variables -> ", end="")
        sys.stdout.flush()
        self._init_field()
        print("Done")

        # Saving Initial Conditions
        print("Saving Initial Conditions -> ", end="")
        sys.stdout.flush()
        self._save(step=0)
        print("Done")


    def set_output_path(self, output_path: str) -> None:
        """
        Specify PATH to output simulation results

        Parameter
        ---------
        output_path: str
            PATH to output simulation results
            (Relative PATH is also possible)
        
        Example
        -------
        1. Create a directory if necessary
        >>> os.mkdir("result_1")

        2. Specify output PATH
        >>> instance.set_output_path(output_path="result_1")
            1) Success
            Nothing happens.
            2) Failure
            FileNotFoundError "< result_1 > is not exist."
        """
        PathTools.set_path(path_val=self.__whole_val.path_val, set_path=output_path, key1=SetPathKey.MAIN, key2=SetPathKey.OUTPUT)

    def set_input_path(self, input_path: str) -> None:
        """
        Specify PATH to input file

        Parameter
        ---------
        input_path: str
            PATH to input file
            (Relative PATH is also possible)
        
        Example
        -------
        >>> instance.set_output_path(input_path="~./setting.yaml")
            1) Success
            Nothing happens.
            2) Failure
            FileNotFoundError "< ~./setting.yaml > is not exist."
        """
        PathTools.set_path(path_val=self.__whole_val.path_val, set_path=input_path, key1=SetPathKey.MAIN, key2=SetPathKey.INPUT)

    def _save(self, step: int) -> None:
        if step == 0:
            SaveTools.first_routine(path_val=self.__whole_val.path_val, outimg_list=OutputDir.OUTIMG_LIST, outarr_list=self.__whole_val.outarr_list)
        SaveTools.save_img(path_val=self.__whole_val.path_val, simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val,
                    cell_val=self.__whole_val.cell_val, outimg_list=OutputDir.OUTIMG_LIST, step=step)
        SaveTools.save_arr(path_val=self.__whole_val.path_val, cell_val=self.__whole_val.cell_val, outarr_list=self.whole_val.outarr_list, step=step)

    def _calc_energy(self) -> None:
        PhaseEnergy.Chemical.calc_drive(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        PhaseEnergy.Gradient.calc_drive(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        PhaseEnergy.ThermalFluct.calc_drive(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        PhaseEnergy.Chemical.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        PhaseEnergy.Gradient.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)    

    def _update_field(self) -> None:
        UpdateFeild.tem_f(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        UpdateFeild.phase_f(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)

    def _init_field(self) -> None:
        if self.__class__.__name__ == SimulationModelKey.DENDRITE.ROUND_CENTER[SimulationModelKey.CLASS_NAME]:
            InitField.Phase.round_center(simu_val=self.__whole_val.simu_val, cell_val=self.__whole_val.cell_val, model_val=self.__whole_val.model_val)
            InitField.Temperture.round_center(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Energy calculations in the initial field
        self._calc_energy()

    def __check_counter(self) -> None:
        #Counter.warning(path_val=self.__whole_val.path_val, key1=SetPathKey.MAIN)
        Counter.error(path_val=self.__whole_val.path_val, key1=SetPathKey.MAIN)

    @property
    def whole_val(self) -> WholeVal:
        """
        Getter of various internal variables
        """
        return self.__whole_val