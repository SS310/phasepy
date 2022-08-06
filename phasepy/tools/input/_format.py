"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********

#********** Import original module **********
from phasepy._const import SimulationModelKey

#********** Constant Value **********


class InputFileFmt():
    def __init__(self, model: dict) -> None:
        """
        
        Parameter
        ---------
        model: dict
            Be sure to set from SimulationModelKey in _const.py

        """
        self.FIRST = [
            "# This file can set all parameter of **" + model[SimulationModelKey.CLASS_NAME] + "** model\n", 
            "# " + model[SimulationModelKey.DESCRIPTION] + "\n",
            "# You must set each value to change simulation environment\n", 
        ]
        self.EXAMPLE = [
            "# Setting example\n",
            "# ============================================================\n",
            "# Variable name\n",
            "#  1. Description for variable\n",
            "#  2. Value type\n",
            "#  3. Unit of measurement\n",
            "#  4. Value\n",
            "# ============================================================\n",
            "# ----- Example -----\n",
            "# exam_val:\n",
            "#  description: Example variables\n",
            "#  type: int\n",
            "#  unit: m/s\n",
            "#  value: 1\n",
            "# ============================================================\n",
            "#  !:types.i4=int32, i8=int64, f4=float32, f8=float64\n",
            "#  !:You can use <e+3> as a 10^3(e+3 = 1000, e-2=0.01, ...)\n",
            "#  !:bool type -> false or true\n",
            "# ============================================================\n",
        ]
        self.OUTPUT = [
            "# ============================================================\n",
            "# ============================================================\n",
            "# Determine the which variable you want.\n",
            "# When you want the variable : true, Not : false, \n",
            "# ============================================================\n",
        ]
        self.MATERIAL = [
            "# ============================================================\n",
            "# ============================================================\n",
            "# Please set material property according to above discription.\n",
            "# ============================================================\n",
        ]
        self.SIMULATE = [
            "# ============================================================\n",
            "# ============================================================\n",
            "# Please set material property according to above discription.\n",
            "# ============================================================\n",
        ]
        self.MODEL = [
            "# ============================================================\n",
            "# ============================================================\n",
            "# Please set **" + model[SimulationModelKey.CLASS_NAME] + "** model parameter according to above discription.\n",
            "# ============================================================\n",
        ]

class StampFormat():
    def __init__(self, model: dict) -> None:
        """
        
        Parameter
        ---------
        model: dict
            Be sure to set from SimulationModelKey in _const.py
        """
        self.OUTPUT = ["SETTING-OUTPUT-PARAMETER-START",
                "SETTING-OUTPUT-PARAMETER-FINISH"]
        self.MATERIAL = ["SETTING-MATERIAL-PROPERTY-START",
                "SETTING-MATERIAL-PROPERTY-FINISH"]
        self.SIMULATE = ["SETTING-SIMULATION-PARAMETER-START",
                "SETTING-SIMULATION-PARAMETER-FINISH"]
        self.MODEL = ["SETTING-" + model[SimulationModelKey.CLASS_NAME] +"-START",
                "SETTING-" + model[SimulationModelKey.CLASS_NAME] +"-FINISH"]