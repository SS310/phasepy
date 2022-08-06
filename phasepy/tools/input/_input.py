"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
from numba import typed, types
import yaml
import os
import shutil

#********** Import original module **********
from phasepy._const import InputDataKey, InputNameKey, SimulationModelKey
from phasepy._const import PathConst
from ._format import InputFileFmt, StampFormat

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

class FmtFile():
    @staticmethod
    def mk_inenv():
        # Dendrite simulation
        value_path = SimulationModelKey.DENDRITE.PATH.VALUE
        model_path = SimulationModelKey.DENDRITE.PATH.MODEL
        for model in [SimulationModelKey.DENDRITE.CENTER]:
            input_file_fmt = InputFileFmt(model=model)
            stamp_format = StampFormat(model=model)

            simu_val = {InputNameKey.SIMULATION_PARAMETER:_Tools.mk_setting_dict(file_path=value_path, stamp=stamp_format.SIMULATE)}
            prop_val = {InputNameKey.MATERIAL_PROPERTY:_Tools.mk_setting_dict(file_path=value_path, stamp=stamp_format.MATERIAL)}
            cell_val = {InputNameKey.OUTPUT_PARAMETER:_Tools.mk_setting_dict(file_path=value_path, stamp=stamp_format.OUTPUT)}
            model_val = {InputNameKey.MODEL_PARAMETER:_Tools.mk_setting_dict(file_path=model_path, stamp=stamp_format.MODEL)}
            
            format_dir = os.path.join(SimulationModelKey.DENDRITE.PATH.DATA, model[SimulationModelKey.CLASS_NAME])
            if os.path.exists(format_dir) == False:
                os.mkdir(format_dir)
            fmt_path = os.path.join(format_dir, "format.yaml")

            _Tools.mk_fmtfile(fmt_path=fmt_path, input_file_fmt=input_file_fmt,
                                simu_val=simu_val, prop_val=prop_val, cell_val=cell_val, model_val=model_val)
    
    @staticmethod
    def mk_yourenv(copy_path: str):
        """
        You can create format of input-file for various simulations in your environment.

        Parameter
        ---------
        copy_path: str
            Specify PATH to copy format of input data in your environment.

        Example
        -------
        >>> fsmapy.input.mk_format(copy_path=copy_path)
        "Create a < " + os.path.abspath(copy_path) + " > ? / <y/n>"
            1. typing "y" and enter.
                1) Success
                >>> fsmapy.input.mk_format(copy_path=copy_path)
                "Successfull created < " + os.path.abspath(copy_path) + " >"
                2) Failure (File exist error)
                >>> fsmapy.input.mk_format(copy_path=copy_path)
                FileExistsError: [WinError 183] Cannot create a file when that file already exists: [path to the file or folder in question]

            2. Other than "y"
            "Creation interrupted."
        """
        copy_path = os.path.abspath(copy_path)
        print("Create a < " + copy_path + " > ? / <y/n>")
        if input() == "y":
            for fmt_path in [PathConst.DENDRITE.DATA, PathConst.MARTENSITE.DATA, PathConst.FSMA.DATA]:
                _Tools.copy_fmtfile(fmt_path=fmt_path, copy_path=copy_path)
            print("Successfull created format files in < " + copy_path + " >")
        else:
            print("Creation interrupted.")

class _Tools():
    @staticmethod
    def mk_fmtfile(fmt_path: str, input_file_fmt: InputFileFmt,
                    simu_val, prop_val, cell_val, model_val):
        with open(fmt_path, "w") as f:
            for item in input_file_fmt.FIRST:
                f.write(item)
            for item in input_file_fmt.EXAMPLE:
                f.write(item)

            for item in input_file_fmt.MODEL:
                f.write(item)
            yaml.dump(model_val, f, default_flow_style=False)

            for item in input_file_fmt.SIMULATE:
                f.write(item)
            yaml.dump(simu_val, f, default_flow_style=False)

            for item in input_file_fmt.MATERIAL:
                f.write(item)
            yaml.dump(prop_val, f, default_flow_style=False)

            for item in input_file_fmt.OUTPUT:
                f.write(item)
            yaml.dump(cell_val, f, default_flow_style=False)

    @staticmethod
    def mk_setting_dict(file_path: str, stamp: list) -> dict:
        data = {}
        cnt1 = 0
        cnt2 = 0
        with open(file_path, "r") as f:
            for item in f.readlines():
                if stamp[0] in item:
                    cnt1 = 1
                elif stamp[1] in item:
                    cnt1 = 0
                else:
                    if cnt1 == 1:
                        if cnt2 == 0:
                            name = item.split(".")[1].split(":")[0].strip(" ")
                            type = item.split(":")[1].split("=")[0].strip(" ")
                            cnt2 = 1
                        elif cnt2 == 1:
                            description = item.split('"""')[1]
                            default = item.split('default=')[1].split(',')[0].strip(" ")
                            unit = item.split('unit=')[1].strip(" ").strip("\n")
                            if unit == "bool":
                                type = "bool"
                                if default == "True":
                                    default = True
                                elif default == "False":
                                    default = False
                                else:
                                    default = False
                            elif "f" in type:
                                #pass
                                default = float(default)
                            elif "i" in type:
                                #pass
                                default = int(default)
                            data[name]={
                                InputDataKey.TYPE:type,
                                InputDataKey.DESCRIPTION:description,
                                InputDataKey.UNIT:unit,
                                InputDataKey.VALUE:default,
                            }
                            cnt2 = 0      
        return data

    @staticmethod
    def copy_fmtfile(fmt_path: str, copy_path: str):
        module_nam = os.path.basename(os.path.split(fmt_path)[0])
        copy_path = os.path.join(copy_path, module_nam)
        # copy format of input data in your environment
        shutil.copytree(fmt_path, copy_path)