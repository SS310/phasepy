"""
Summary
-------
Main constant value is written in this file.

See Also
--------

"""

#********** Import major pakage or module **********
import math
import os

#********** Class **********


#***** Math constant *****

class MathConst():
    """
    Math constant
    """
    PI: float = math.pi
    """pi ( 3.14... )"""
    R_GAS: float= 8.3145
    """Gas constant"""
    WHITE_NUM: int = 255
    """MAX 8-bit data using white area for image"""
    MU0: float = 4.0*PI*1e-7
    """Permeability of vacuum"""

#***** Constant about directry or file name *****
class DirNam():
    INFO = ".info"
    """Information directry"""

class PathConst():
    PACKAGE = os.path.abspath(os.path.dirname(__file__))
    """PATH of this package"""
    
    __DENDRITE = "dendrite"
    __MARTENSITE = "martensite"
    __FSMA = "fsma"

    class __ModelPath():
        def __init__(self, model: str, PAKCAGE: str) -> None:
            self.DATA = os.path.join(PAKCAGE, model , "data")
            """PATH of format file for dendrite simulation"""
            self.VALUE = os.path.join(PAKCAGE, model, "variable", "define", "_var.py")
            """PATH of variable definition file for dendrite simulation"""
            self.MODEL = os.path.join(PAKCAGE, model, "variable", "define", "_model.py")
            """PATH of variable definition file for dendrite simulation"""

    DENDRITE = __ModelPath(model=__DENDRITE, PAKCAGE=PACKAGE)
    """PATH for dendrite simulation"""
    MARTENSITE = __ModelPath(model=__MARTENSITE, PAKCAGE=PACKAGE)
    """PATH for martensite simulation"""
    FSMA = __ModelPath(model=__FSMA, PAKCAGE=PACKAGE)
    """PATH for martensite simulation"""


#***** Constant about dictionary key*****
class SetPathKey():
    MAIN = "main"
    """Key of counter"""
    OUTPUT = "output_path"
    """Key of output-path"""
    INPUT = "input_path"
    """Key of input-path"""

class InputDataKey():
    DESCRIPTION = "description"
    """Key of variable description"""
    TYPE = "type"
    """Key of variable type"""
    UNIT = "unit"
    """Key of variable unit"""
    VALUE = "value"
    """Key of variable value"""

class InputNameKey():
    """
    Constants related to the name of the setting definition used in the dict type
    """
    SIMULATION_PARAMETER = "simulation_parameter"
    """Key of simulation parameter"""
    OUTPUT_PARAMETER = "output_parameter"
    """Key of output parameter"""
    MATERIAL_PROPERTY = "material_property"
    """Key of material property"""
    MODEL_PARAMETER = "model_parameter"
    """Key of model prameter"""
    

class SimulationModelKey():
    """
    Key of All simulation model
    """
    CLASS_NAME = "class_name"
    """Key of class name for each simulation model"""
    DESCRIPTION = "description"
    """Key of description for each simulation model"""

    class __Dendrite():
        """
        Key of dendrite simulation model
        """
        def __init__(self, CLASS_NAME: str, DESCRIPTION: str) -> None:
            """
            Key of dendrite simulation model
            """
            self.PATH = PathConst.DENDRITE
            """PATH for dendrite simulation"""
            self.CENTER = {
                CLASS_NAME: "Center",
                DESCRIPTION: "This is a basic model in which a circular initial nucleus is generated in the center."
            }
    
    class __Fsma():
        """
        Key of fsma simulation model
        """
        def __init__(self, CLASS_NAME: str, DESCRIPTION: str) -> None:
            """
            Key of fsma simulation model
            """   
            self.PATH = PathConst.FSMA
            """PATH for fsma simulation"""


    class __Martensite():
        """
        Key of martensite simulation model
        """
        def __init__(self, CLASS_NAME: str, DESCRIPTION: str) -> None:
            """
            Key of martensite simulation model
            """   
            self.PATH = PathConst.MARTENSITE
            """PATH for martensite simulation"""
    
    DENDRITE = __Dendrite(CLASS_NAME=CLASS_NAME, DESCRIPTION=DESCRIPTION)
    """Key of dendrite simulation model """
    MARTENSITE = __Martensite(CLASS_NAME=CLASS_NAME, DESCRIPTION=DESCRIPTION)
    """Key of dendrite simulation model """
    FSMA = __Fsma(CLASS_NAME=CLASS_NAME, DESCRIPTION=DESCRIPTION)
    """Key of dendrite simulation model """