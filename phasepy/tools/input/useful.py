"""
Summary
-------
File that manages tools related to externally available input files.

See Also
--------

"""

#********** Import major pakage or module **********
import yaml
import os
import shutil

#********** Import original module **********
from phasepy._const import InputNameKey, InputDataKey, SimulationModelKey
from phasepy._const import PathConst
from ._format import InputFileFmt, StampFormat

#********** Constant Value **********

class InputTools():
    @staticmethod
    def check_param(path: str, description: bool=False, unit: bool=False, model_parameter: bool=True, 
                simulation_parameter: bool=True, material_property: bool=True, output_parameter: bool=True) -> None:
        """
        Check the parameters related to the input file

        Parameter
        ---------
        path: str
            PATH of file of parameters you want to check
        description: bool (default=False)
            Whether to display description
        unit: bool (default=False)
            Whether to display unit
        model_parameter: bool (default=True)
            Whether to display model_parameter
        simulation_parameter (default=True)
            Whether to display simulation_parameter
        material_property (default=True)
            Whether to display material_property
        output_parameter (default=True)
            Whether to display output_parameter
        """
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        if model_parameter == True:
            _Tools.print_param(data=data[InputNameKey.MODEL_PARAMETER], key1=InputNameKey.MODEL_PARAMETER, description=description, unit=unit)
        if simulation_parameter == True:
            _Tools.print_param(data=data[InputNameKey.SIMULATION_PARAMETER], key1=InputNameKey.SIMULATION_PARAMETER, description=description, unit=unit)
        if material_property == True:
            _Tools.print_param(data=data[InputNameKey.MATERIAL_PROPERTY], key1=InputNameKey.MATERIAL_PROPERTY, description=description, unit=unit)
        if output_parameter == True:
            _Tools.print_param(data=data[InputNameKey.OUTPUT_PARAMETER], key1=InputNameKey.OUTPUT_PARAMETER, description=description, unit=unit)

    class MkInputFile():
        @staticmethod
        def outof_package(copy_path: str) -> None:
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

        @staticmethod
        def into_package() -> None:
            """
            You can create format of input-file for various simulations into this package.
            """
            # Dendrite simulation
            value_path = SimulationModelKey.DENDRITE.PATH.VALUE
            model_path = SimulationModelKey.DENDRITE.PATH.MODEL
            for model in [SimulationModelKey.DENDRITE.ROUND_CENTER]:
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

    # ----- Change parameters in the input file -----
    class Change():
        """
        Change parameters in the input file
        """
        @staticmethod
        def model_parameter(origin_path: str, param_name: str, param_val: any ,rewrite_path: str = None) -> None:
            """
            Change variables belonging to < model_parameter >

            Parameter
            ---------
            origin_path: str
                PATH of file before rewriting
            param_name: str
                Target variable name
            param_val: any
                Value to be changed
            rewiite_path: str (default=None)
                PATH of file before rewriting
                    -> If *None*, overwrite the file before rewriting.

            See Also
            --------
            If you want to know about paramater, you should use < InputUsefulTools.see_param() >
            """
            _Tools.change_routine(origin_path=origin_path, param_name=param_name, param_val=param_val, key1=InputNameKey.MODEL_PARAMETER ,rewrite_path=rewrite_path)

        @staticmethod
        def material_property(origin_path: str, param_name: str, param_val: any ,rewrite_path: str = None) -> None:
            """
            Change variables belonging to < material_property >

            Parameter
            ---------
            origin_path: str
                PATH of file before rewriting
            param_name: str
                Target variable name
            param_val: any
                Value to be changed
            rewiite_path: str (default=None)
                PATH of file before rewriting
                    -> If *None*, overwrite the file before rewriting.

            See Also
            --------
            If you want to know about paramater, you should use < InputUsefulTools.see_param() >
            """
            _Tools.change_routine(origin_path=origin_path, param_name=param_name, param_val=param_val, key1=InputNameKey.MATERIAL_PROPERTY ,rewrite_path=rewrite_path)

        @staticmethod
        def simulation_parameter(origin_path: str, param_name: str, param_val: any ,rewrite_path: str = None) -> None:
            """
            Change variables belonging to < simulation_parameter >

            Parameter
            ---------
            origin_path: str
                PATH of file before rewriting
            param_name: str
                Target variable name
            param_val: any
                Value to be changed
            rewiite_path: str (default=None)
                PATH of file before rewriting
                    -> If *None*, overwrite the file before rewriting.

            See Also
            --------
            If you want to know about paramater, you should use < InputUsefulTools.see_param() >
            """
            _Tools.change_routine(origin_path=origin_path, param_name=param_name, param_val=param_val, key1=InputNameKey.SIMULATION_PARAMETER ,rewrite_path=rewrite_path)

        @staticmethod
        def output_parameter(origin_path: str, param_name: str, param_val: bool ,rewrite_path: str = None) -> None:
            """
            Change variables belonging to < output_parameter >

            Parameter
            ---------
            origin_path: str
                PATH of file before rewriting
            param_name: str
                Target variable name
            param_val: bool
                Value to be changed
                    -> If you don't set bool(True or False), occured TypeError
            rewiite_path: str (default=None)
                PATH of file before rewriting
                    -> If *None*, overwrite the file before rewriting.

            See Also
            --------
            If you want to know about paramater, you should use < InputUsefulTools.see_param() >
            """
            if type(param_val) == bool:
                _Tools.change_routine(origin_path=origin_path, param_name=param_name, param_val=param_val, key1=InputNameKey.OUTPUT_PARAMETER ,rewrite_path=rewrite_path)
            else:
                TypeError("< param_val > is allowed only bool type.")


#********** Internal class **********

class _Tools():
    @staticmethod
    def print_param(data: dict, key1: str, description: bool, unit: bool) -> None:
        print("---------- " + key1 + " ----------")
        for key in data.keys():
            print(key + " : ", end="")
            if description == True:
                print("[ " + data[key][InputDataKey.DESCRIPTION] + " ]", end="")
            if unit == True:
                print(", " + data[key][InputDataKey.UNIT], end="")
            print(" : " + str(data[key][InputDataKey.VALUE]))
            

    @staticmethod
    def change_routine(origin_path: str, param_name: str, param_val: any ,key1: str, rewrite_path: str = None) -> None:
        # If the rewritten file name is not specified
        if rewrite_path == None:
            rewrite_path = origin_path

        # Read information before rewriting
        (data, cmt) = _Tools.read_data(origin_path=origin_path)

        # Rewriting information
        data = _Tools.change_value(param_name=param_name, param_val=param_val, key1=key1)

        # Save according to rewrite information
        _Tools.rewrite_data(rewrite_path=rewrite_path, cmt=cmt, data=data)

    @staticmethod
    def change_value(data: dict, param_name: str, param_val: any, key1: str) -> dict:
        # Rewriting information
        if data[key1].get(param_name) == None:
            raise KeyError("The specified key < " + param_name + " > does not exist.")
        else:
            data[key1][param_name][InputDataKey.VALUE] = param_val

        return data

    @staticmethod
    def read_data(origin_path: str) -> tuple:
        # Read dict information before rewriting
        with open(origin_path, "r") as f:
            data = yaml.safe_load(f)

        # Read txt information before rewriting
        with open(origin_path, "r") as f:
            cmt = []
            cnt = 1
            for line in f.readlines():
                if line[0] == "#":
                    if cnt == 1:
                        cmt.append(line)
                    else:
                        cmt.append(0)
                        cmt.append(line)
                        cnt = 1
                else:
                    cnt = 0
            return (data, cmt)

    @staticmethod
    def rewrite_data(rewrite_path: str, cmt: list, data: dict) -> tuple:
        cnt = 0
        # Read information before rewriting
        with open(rewrite_path, "w") as f:
            for txt in cmt:
                if txt == 0:
                    if cnt == 0:
                        yaml.dump({InputNameKey.MODEL_PARAMETER:data[InputNameKey.MODEL_PARAMETER]}, f, default_flow_style=False)
                    elif cnt == 1:
                        yaml.dump({InputNameKey.SIMULATION_PARAMETER:data[InputNameKey.SIMULATION_PARAMETER]}, f, default_flow_style=False)
                    elif cnt == 2:
                        yaml.dump({InputNameKey.MATERIAL_PROPERTY:data[InputNameKey.MATERIAL_PROPERTY]}, f, default_flow_style=False)
                    cnt += 1
                else:
                    f.write(txt)
            yaml.dump({InputNameKey.OUTPUT_PARAMETER:data[InputNameKey.OUTPUT_PARAMETER]}, f, default_flow_style=False)

    @staticmethod
    def copy_fmtfile(fmt_path: str, copy_path: str):
        module_nam = os.path.basename(os.path.split(fmt_path)[0])
        copy_path = os.path.join(copy_path, module_nam)
        # copy format of input data in your environment
        shutil.copytree(fmt_path, copy_path)

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