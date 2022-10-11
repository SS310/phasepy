"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import sys

#********** Import orizinal module **********
from phasepy.fsma.variable.define._whole import WholeVal
from phasepy.tools._path import PathTools, Counter
from phasepy._const import SetPathKey, SimulationModelKey
from phasepy.fsma._const import OutputDir, FsmaSetPathKey
from phasepy.tools._save import SaveTools
from phasepy.fsma.variable.update._strain import Strain
from phasepy.fsma.variable.update._energy import PhaseEnergy, MagneEnergy
from phasepy.fsma.variable.update._field import UpdateField
from phasepy.fsma.variable.init._field import InitField

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
        ```
        """
        print("")
        print("********** Initialization of magnetic domain and metal structure **********")

        # Monitoring of initial conditions
        print("Monitoring of initial conditions")
        sys.stdout.flush()
        self.__check_counter()
        print("-----> Done")

        # Declaration of Variables(Very heavy because of jit)
        print("Declaration of Variables(Very heavy because of jit) -> ", end="")
        sys.stdout.flush()
        self.__whole_val.set()
        print("Done")

        # Initialization of field variables
        print("Initialization of field variables...",)
        sys.stdout.flush()
        self._init_field()
        print("-> Done")

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
        >>> instance.set_input_path(input_path="~./setting.yaml")
            1) Success
            Nothing happens.
            2) Failure
            FileNotFoundError "< ~./setting.yaml > is not exist."
        """
        PathTools.set_path(path_val=self.__whole_val.path_val, set_path=input_path, key1=SetPathKey.MAIN, key2=SetPathKey.INPUT)

    def set_phase_path(self, phase_path: str) -> None:
        """
        Specify PATH to initial metal domain

        Parameter
        ---------
        phase_path: str
            PATH to input file
            (Relative PATH is also possible, requrie <png> or <npy>)
        
        Example
        -------
        >>> instance.set_phase_path(phase_path="~./ooo.npy")
            1) Success
            Nothing happens.
            2) Failure
            FileNotFoundError "< ~./ooo.npy > is not exist."
        """
        PathTools.set_path(path_val=self.__whole_val.path_val, set_path=phase_path, key1=SetPathKey.SUB, key2=FsmaSetPathKey.PHASE_PATH)

    def set_magne_path(self, magne_path: str) -> None:
        """
        Specify PATH to initial magnetic domain

        Parameter
        ---------
        magne_path: str
            PATH to input file
            (Relative PATH is also possible, requrie <png> or <npy>)
        
        Example
        -------
        >>> instance.set_phase_path(magne_path="~./ooo.npy")
            1) Success
            Nothing happens.
            2) Failure
            FileNotFoundError "< ~./ooo.npy > is not exist."
        """
        PathTools.set_path(path_val=self.__whole_val.path_val, set_path=magne_path, key1=SetPathKey.SUB, key2=FsmaSetPathKey.MAGNE_PATH)

    def _save(self, step: int) -> None:
        if step == 0:
            SaveTools.first_routine(path_val=self.__whole_val.path_val, outimg_list=OutputDir.OUTIMG_LIST, outarr_list=self.__whole_val.outarr_list)
        SaveTools.save_img(path_val=self.__whole_val.path_val, simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val,
                    cell_val=self.__whole_val.cell_val, outimg_list=OutputDir.OUTIMG_LIST, step=step)
        SaveTools.save_arr(path_val=self.__whole_val.path_val, cell_val=self.__whole_val.cell_val, outarr_list=self.whole_val.outarr_list, step=step)

    def _calc_strain(self) -> None:
        Strain.calc_ep_eigen(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        Strain.calc_ep_eigen_four(cell_val=self.__whole_val.cell_val)
        Strain.calc_ep_hetero_four(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        Strain.calc_ep_hetero(cell_val=self.__whole_val.cell_val)
        Strain.calc_ep_ex(prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        Strain.calc_ep_eigen_ave(cell_val=self.__whole_val.cell_val)

    def _calc_energy(self) -> None:
        # ----------------------------------------
        # Calculate driving force of metal domain
        # Chemical energy
        PhaseEnergy.Chemical.calc_drive(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Gradient energy
        PhaseEnergy.Gradient.calc_drive(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Elastic Energy
        PhaseEnergy.Elastic.calc_drive(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # ----------------------------------------
        # Calculate energy of metal domain
        # Chemical energy
        PhaseEnergy.Chemical.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Gradient energy
        PhaseEnergy.Gradient.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Elastic Energy
        PhaseEnergy.Elastic.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)

        # ----------------------------------------
        # Calculate magnetic field of magnetic domain
        # Magnetostatic energy
        MagneEnergy.MagnetoStatic.calc_h(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Magnetoelastic
        MagneEnergy.MagnetoElastic.calc_h(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Exchange energy
        MagneEnergy.Exchange.calc_h(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Anisotropy energy
        MagneEnergy.Anisotropy.calc_h(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # ----------------------------------------
        # Calculate magnetic field of magnetic domain
        # Magnetostatic energy
        MagneEnergy.MagnetoStatic.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Magnetoelastic
        MagneEnergy.MagnetoElastic.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Exchange energy
        MagneEnergy.Exchange.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Anisotropy energy
        MagneEnergy.Anisotropy.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        # Zeeman energy
        MagneEnergy.Zeeman.calc_energy(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)


    def _update_field(self) -> None:
        UpdateField.phase_f(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)
        UpdateField.magne_f(simu_val=self.__whole_val.simu_val, prop_val=self.__whole_val.prop_val, cell_val=self.__whole_val.cell_val)

    def _init_field(self) -> None:
        if self.__class__.__name__ == SimulationModelKey.FSMA.TOWARD_STABLE[SimulationModelKey.CLASS_NAME]:
            InitField.Phase.toward_center(path_val=self.__whole_val.path_val ,simu_val=self.__whole_val.simu_val, cell_val=self.__whole_val.cell_val)
            InitField.Magne.toward_center(path_val=self.__whole_val.path_val ,simu_val=self.__whole_val.simu_val, cell_val=self.__whole_val.cell_val)
        
        # Strain calculations in the initial field
        self._calc_strain()
        # Energy calculations in the initial field
        self._calc_energy()

    def __check_counter(self) -> None:
        Counter.warning(path_val=self.__whole_val.path_val, key1=SetPathKey.SUB)
        Counter.error(path_val=self.__whole_val.path_val, key1=SetPathKey.MAIN)

    @property
    def whole_val(self) -> WholeVal:
        """
        Getter of various internal variables
        """
        return self.__whole_val