"""
Summary
-------

See Also
----------

"""

#********** Import major pakage or module **********
import os

#********** Import original module **********
from ._var_fmt import PathVal
from phasepy._error import ValueErr

#********** Constant Value **********

class PathTools():
    @staticmethod
    def set_path(path_val: PathVal, set_path: str, key1: str, key2: str, extension: tuple=(False,[])) -> None:
        # Check extension
        if extension[0] == True:
            ValueErr.check_extension(filenam=set_path, correct_extension=extension[1])
        # If path does not exist
        if os.path.exists(os.path.abspath(set_path)) == False:
            raise FileNotFoundError("< " + os.path.abspath(set_path) + " > is not exist.")
        else:
            path_val.__dict__[key2] = set_path
        
        path_val.counter[key1][key2] = True

class Counter():
    @staticmethod
    def error(path_val: PathVal, key1: str):
        for key, value in path_val.counter[key1].items():
            if value == False:
                raise IndexError("< " + key + " > is not yet defined.")

    @staticmethod
    def warning(path_val: PathVal, key1: str):
        for key, value in path_val.counter[key1].items():
            if value == False:
                print("WARNING : < " + key + " > is not yet defined.")