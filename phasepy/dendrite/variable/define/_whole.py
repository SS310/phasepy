"""
Summary
-------


See Also
--------

"""

#********** Import major pakage or module **********

#********** Import orizinal module **********
from phasepy.tools._array import InitArray
from ._path import PathVal
from ._var import SimuVal, PropVal, CellVal
from ._model import *
from phasepy.tools.input._input import InputTools
from phasepy._const import InputNameKey, InputDataKey, SimulationModelKey
from phasepy.tools._save import mk_outarr_list
from numba import typed


#********** Constant Value **********

#********** Class **********

class WholeVal():
    def __init__(self, class_name: str) -> None:
        self.path_val: PathVal = PathVal()
        self.__class_name: str = class_name

    def set(self):
        self.__input_data: dict = InputTools.open_yaml(file_path=self.path_val.input_path)
        
        simulation_parameter: typed.Dict = InputTools.mk_jit_dict(input_data=self.__input_data, key=InputNameKey.SIMULATION_PARAMETER)
        material_property: typed.Dict = InputTools.mk_jit_dict(input_data=self.__input_data, key=InputNameKey.MATERIAL_PROPERTY)
        output_parameter: dict = self.input_data[InputNameKey.OUTPUT_PARAMETER]
        model_parametr: typed.Dict = InputTools.mk_jit_dict(input_data=self.__input_data, key=InputNameKey.MODEL_PARAMETER)
        
        xmax = self.__input_data[InputNameKey.SIMULATION_PARAMETER]["xmax"][InputDataKey.VALUE]
        ymax = self.__input_data[InputNameKey.SIMULATION_PARAMETER]["ymax"][InputDataKey.VALUE]
        
        init_array: InitArray = InitArray(xmax=xmax, ymax=ymax)
        self.__outarr_list: list = mk_outarr_list(output_parameter=output_parameter)

        self.simu_val: SimuVal = SimuVal(simulation_parameter=simulation_parameter, i4_xy=init_array.i4_xy, f4_xy=init_array.f4_xy)
        self.prop_val: PropVal = PropVal(material_property=material_property, xsize=self.simu_val.xsize, ysize=self.simu_val.ysize)
        self.cell_val: CellVal = CellVal(xmax=self.simu_val.xmax, ymax=self.simu_val.ymax)

        if self.__class_name == SimulationModelKey.DENDRITE.ROUND_CENTER[SimulationModelKey.CLASS_NAME]:
            self.model_val = CenterModel(model_parameter=model_parametr)

    @property
    def outarr_list(self):
        return self.__outarr_list

    @property
    def input_data(self):
        return self.__input_data
