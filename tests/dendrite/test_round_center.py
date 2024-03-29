
import os
import numpy as np

from phasepy.dendrite.main.tests._round_center import RoundCenter
from phasepy.tools.input._input import InputTools
from phasepy._const import PathConst, InputNameKey, InputDataKey

round_center = RoundCenter()
round_center.test_set()

def test_set_model_param():
    """
    Is the reading of file contents working properly?
    """
    file_path = os.path.join(PathConst.DENDRITE.DATA, "Center", "format.yaml")
    data: dict = InputTools.open_yaml(file_path=file_path)

    model_parameter: dict = data[InputNameKey.MODEL_PARAMETER]
    for key, value in model_parameter.items():
        assert value[InputDataKey.VALUE] == getattr(round_center.whole_val.model_val, key), key + " have a problem!"
        
def test_set_simulation_param():
    """
    Is the reading of file contents working properly?
    """
    file_path = os.path.join(PathConst.DENDRITE.DATA, "Center", "format.yaml")
    data: dict = InputTools.open_yaml(file_path=file_path)

    simulation_parameter: dict = data[InputNameKey.SIMULATION_PARAMETER]
    for key, value in simulation_parameter.items():
        assert value[InputDataKey.VALUE] == getattr(round_center.whole_val.simu_val, key), key + " have a problem!"

def test_set_property_param():
    """
    Is the reading of file contents working properly?
    """
    file_path = os.path.join(PathConst.DENDRITE.DATA, "Center", "format.yaml")
    data: dict = InputTools.open_yaml(file_path=file_path)

    material_property: dict = data[InputNameKey.MATERIAL_PROPERTY]
    for key, value in material_property.items():
        assert value[InputDataKey.VALUE] == getattr(round_center.whole_val.prop_val, key), key + " have a problem!"


def test_model_param_after_main():
    for item in dir(round_center.whole_val.model_val):
        if not "__" in item:
            round_center.test_set()
            before = getattr(round_center.whole_val.model_val, item)
            round_center.test_main()
            after = getattr(round_center.whole_val.model_val, item)
            
            assert before == after, item + " have a problem!"

def test_property_param_after_main():
    for item in dir(round_center.whole_val.prop_val):
        if not "__" in item:
            round_center.test_set()
            before = getattr(round_center.whole_val.prop_val, item)
            round_center.test_main()
            after = getattr(round_center.whole_val.prop_val, item)
            
            assert before == after, item + " have a problem!"

def test_cell_param_after_update_phase():
    for item in dir(round_center.whole_val.cell_val):
        if not ("__" in item or "numba" in item):
            if item != "phase_f":
                round_center.test_set()
                before = np.copy(getattr(round_center.whole_val.cell_val, item))
                round_center.test_update_phase()
                after = np.copy(getattr(round_center.whole_val.cell_val, item))
                if type(before) == np.ndarray:
                    assert before.any() == after.any(), item + " have a problem!"
                else:
                    assert before == after, item + " have a problem!"

def test_cell_param_after_update_tem():
    for item in dir(round_center.whole_val.cell_val):
        if not ("__" in item or "numba" in item):
            if item != "tem_f":
                round_center.test_set()
                round_center.test_update_phase()
                before = np.copy(getattr(round_center.whole_val.cell_val, item))
                round_center.test_update_tem()
                after = np.copy(getattr(round_center.whole_val.cell_val, item))
                if type(before) == np.ndarray:
                    assert before.any() == after.any(), item + " have a problem!"
                else:
                    assert before == after, item + " have a problem!"

def test_cell_param_after_calc_chem_drive():
    for item in dir(round_center.whole_val.cell_val):
        if not ("__" in item or "numba" in item):
            if item != "chem_drive":
                round_center.test_set()
                round_center.test_update_phase()
                round_center.test_update_tem()
                before = np.copy(getattr(round_center.whole_val.cell_val, item))
                round_center.test_calc_chem_drive()
                after = np.copy(getattr(round_center.whole_val.cell_val, item))
                if type(before) == np.ndarray:
                    assert before.any() == after.any(), item + " have a problem!"
                else:
                    assert before == after, item + " have a problem!"

def test_cell_param_after_calc_grad_drive():
    for item in dir(round_center.whole_val.cell_val):
        if not ("__" in item or "numba" in item):
            if item != "grad_drive":
                round_center.test_set()
                round_center.test_update_phase()
                round_center.test_update_tem()
                before = np.copy(getattr(round_center.whole_val.cell_val, item))
                round_center.test_calc_grad_drive()
                after = np.copy(getattr(round_center.whole_val.cell_val, item))
                if type(before) == np.ndarray:
                    assert before.any() == after.any(), item + " have a problem!"
                else:
                    assert before == after, item + " have a problem!"

def test_cell_param_after_calc_fluct_drive():
    for item in dir(round_center.whole_val.cell_val):
        if not ("__" in item or "numba" in item):
            if item != "tem_fluct":
                round_center.test_set()
                round_center.test_update_phase()
                round_center.test_update_tem()
                before = np.copy(getattr(round_center.whole_val.cell_val, item))
                round_center.test_calc_fluct_drive()
                after = np.copy(getattr(round_center.whole_val.cell_val, item))
                if type(before) == np.ndarray:
                    assert before.any() == after.any(), item + " have a problem!"
                else:
                    assert before == after, item + " have a problem!"

def test_cell_param_after_calc_chem_energy():
    for item in dir(round_center.whole_val.cell_val):
        if not ("__" in item or "numba" in item):
            if item != "chem_energy":
                round_center.test_set()
                round_center.test_update_phase()
                round_center.test_update_tem()
                before = np.copy(getattr(round_center.whole_val.cell_val, item))
                round_center.test_calc_chem_energy()
                after = np.copy(getattr(round_center.whole_val.cell_val, item))
                if type(before) == np.ndarray:
                    assert before.any() == after.any(), item + " have a problem!"
                else:
                    assert before == after, item + " have a problem!"

def test_cell_param_after_calc_grad_energy():
    for item in dir(round_center.whole_val.cell_val):
        if not ("__" in item or "numba" in item):
            if item != "grad_energy":
                round_center.test_set()
                round_center.test_update_phase()
                round_center.test_update_tem()
                before = np.copy(getattr(round_center.whole_val.cell_val, item))
                round_center.test_calc_grad_energy()
                after = np.copy(getattr(round_center.whole_val.cell_val, item))
                if type(before) == np.ndarray:
                    assert before.any() == after.any(), item + " have a problem!"
                else:
                    assert before == after, item + " have a problem!"