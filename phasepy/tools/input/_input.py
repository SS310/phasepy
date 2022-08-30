"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
from numba import typed, types
import yaml

#********** Import original module **********
from phasepy._const import InputDataKey

#********** Constant Value **********

class InputTools():
    @staticmethod
    def open_yaml(file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    @staticmethod
    def mk_jit_dict(input_data: dict, key: str) -> typed.Dict:
        data = typed.Dict.empty(key_type=types.string, value_type=types.f8)
        for key1 in input_data[key].keys():
            data[key1] = input_data[key][key1][InputDataKey.VALUE]
        return data



