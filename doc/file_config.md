# About file configuration
This file is written about **file configuration**.

> <h2><strong>File configuration diagram</strong></h2>

-----
ex)
- **Directry** : _Description_
  - File.file : _Description_ <font color="StableBule">(BF)</font>
  - **Directry** : _Description_
    - File.file : _Description_ <font color="Orange">(IN)</font>
    - File.file : _Description_ <font color="LightGray">(AF)</font>

<br>

> Mark

Before development -> <font color="StableBule">(BF)</font>
In development -> <font color="Orange">(IN)</font>
After development -> <font color="LightGray">(AF)</font>

-----

- **phasepy** : _Parent directory._
  - README.md : _README file._ <font color="Orange">(IN)</font>
  - .gitignore : _List of extensions to ignore._ <font color="Orange">(IN)</font>
  - pyproject.toml : _Setup file._ <font color="Orange">(IN)</font>
  - **data** : _Data use to some file._
    - ...
  - **doc** : _Document files are exist._
    - file_config.md : _This file._ <font color="Orange">(IN)</font>
    - rule.md : _Some rules of this project._ <font color="LightGray">(AF)</font>
    - **data** : _Data use to some file._
      - ...
    - **theory** : _Files about theories in kotsupy are exist._
      - dendrite.md : _Theory of dendrite simulation._ <font color="StableBule">(BF)</font>
      - fsma.md : _Theory of fsma simulation._ <font color="StableBule">(BF)</font>
      - martensite.md : _Theory of martensite simulation._ <font color="StableBule">(BF)</font>
      - **data** : _Data used to explain the theory exists._
        - ...
    - **tutorial** : _Tutorial ipynb-files are exist._
      - **dendrite** : _Tutorial of dendrite simulation._
        - description.md : _Description for tutorial of dendrite simulation._ <font color="StableBule">(BF)</font>
        - ...
        - **data** : _Data used to explain the tutorial exists._
          - ...
      - **fsma** : _Tutorial of fsma simulation._
        - description.md : _Description for tutorial of fsma simulation._ <font color="StableBule">(BF)</font>
        - ...
        - **data** : _Data used to explain the tutorial exists._
          - ...
      - **martensite** : _Tutorial of martensite simulation._
        - description.md : _Description for tutorial of martensite simulation._ <font color="StableBule">(BF)</font>
        - ...
        - **data** : _Data used to explain the tutorial exists._
          - ...
   - **phasepy** : _Python pakage._
      - \__init__.py : _Init file of this package._
      - _error.py : _Exception and Error are written._ <font color="Orange">(IN)</font>
      - _const.py : _Constants are written._ <font color="Orange">(IN)</font>
      - **tools** : _Modules of various tools._
        - _array.py : _Tools about array initialization for jitclass._ <font color="LightGray">(AF)</font>
        - _path.py : _Tools about path._ <font color="LightGray">(AF)</font>
        - _save.py: _Tools about save file._ <font color="LightGray">(AF)</font>
        - _val_fmt.py: _Tools about format of variable class._ <font color="LightGray">(AF)</font>
        - _xytools.py: _Tools about calculation of various coordinate systems._ <font color="LightGray">(AF)</font>
        - **input** : _About input file._
          - _input.py : _Tools about input file._ <font color="LightGray">(AF)</font>
          - _format.py : _Description text in the input file._ <font color="LightGray">(AF)</font>
      - **dendrite** : _Modules of dendrite simulation._
        - \__init__.py : _Init file of dendrite module._ <font color="LightGray">(AF)</font>
        - _const.py : _Constants used only within dendrite modules are written._ <font color="LightGray">(AF)</font>
        - **data** : _Format of input file are exists._
          - **Center** : _Format of input file for center model._
            - format.yaml : _Format of input file for center model._
        - **main** : _Main simulation module._
          - _base.py : _Base class of dendrite simulation is written._ <font color="LightGray">(AF)</font>
          - center.py : _Dendrite simulation of nucleation from the center._ <font color="LightGray">(AF)</font>
          - **tests** : _For the unit test modules._
            - _center.py : _Unit test for center model._ <font color="LightGray">(AF)</font>
        - **variable** : _Variable module._
          - **define** : _Definition module._
            - _path.py : _Variable class about path._ <font color="LightGray">(AF)</font>
            - _var.py : _Variable class about common simulation parameter._ <font color="LightGray">(AF)</font>
            - _model.py : _Variable class about each simulation model's parameter._ <font color="StableBule">(BF)</font>
            - _whole.py : _Variable class consolidated all variable class._ <font color="LightGray">(AF)</font>
          - **init** : _Initializing module._
            - _field.py : _Initializing field variables._ <font color="LightGray">(AF)</font>
          - **update** : _Update module_
            - _energy.py : _Update energy._ <font color="LightGray">(AF)</font>
            - _field.py : _Update field variables._ <font color="LightGray">(AF)</font>
      - **fsma** : _Modules of fsma simulation._
        - \__init__.py : _Init file of fsma module._ <font color="StableBule">(BF)</font>
        - _const.py : _Constants used only within fsma modules are written._ <font color="StableBule">(BF)</font>
        - **data** : _Format of input file are exists._
          - ...
        - **main** : _Main simulation module._
          - _base.py : _Base class of dendrite simulation is written._ <font color="StableBule">(BF)</font>
          - stable.py : _Fsma simulation up to stabilization of magnetic domain._ <font color="StableBule">(BF)</font>
            - **tests** : _For the unit test modules._
              - ...
        - **variable** : _Variable module._
          - **define** : _Definition module._
            - _path.py : _Variable class about path._ <font color="StableBule">(BF)</font>
            - _var.py : _Variable class about common simulation parameter._ <font color="StableBule">(BF)</font>
            - _model.py : _Variable class about each simulation model's parameter._ <font color="StableBule">(BF)</font>
            - _whole.py : _Variable class consolidated all variable class._ <font color="StableBule">(BF)</font>
          - **init** : _Initializing module._
            - _filed.py : _Initializing field variables._ <font color="StableBule">(BF)</font>
          - **update** : _Update module._
            - _strain.py : _Update strain._ <font color="StableBule">(BF)</font>
            - _energy.py : _Update energy._ <font color="StableBule">(BF)</font>
            - _field.py : _Update field variables._ <font color="StableBule">(BF)</font>
      - **martensite** : _Modules of martensite simulation._ <font color="StableBule">(BF)</font>
        - \__init__.py : _Init file of martensite module._ <font color="StableBule">(BF)</font>
        - _const.py : _Constants used only within martensite modules are written._ <font color="StableBule">(BF)</font>
        - **data** : _Format of input file are exists._ <font color="StableBule">(BF)</font>
          - ...
        - **main** : _Main simulation module._
          - _base.py : _Base class of dendrite simulation is written._
          - stable.py : _Martensite simulation up to stabilization of structure._
            - **tests** : _For the unit test modules._
              - ...
        - **variable** : _Variable module._
          - **define** : _Definition module._
            - _path.py : _Variable class about path._ <font color="StableBule">(BF)</font>
            - _var.py : _Variable class about common simulation parameter._ <font color="StableBule">(BF)</font>
            - _model.py : _Variable class about each simulation model's parameter._ <font color="StableBule">(BF)</font>
            - _whole.py : _Variable class consolidated all variable class._ <font color="StableBule">(BF)</font>
          - **init** : _Initializing module._
            - _field.py : _Initializing field variables._ <font color="StableBule">(BF)</font>
          - **update** : _Update module_
            - _strain.py : _Update strain._ <font color="StableBule">(BF)</font>
            - _energy.py : _Update energy._ <font color="StableBule">(BF)</font>
            - _field.py : _Update field variables._ <font color="StableBule">(BF)</font>
  - **tests** : _Unit test_
    - **others** : _Unit test related to entire package._
    - **dendrite** : _Unit test related to dendrite simulation._
      - \__init__.py : <font color="LightGray">(AF)</font>
      - test_center.py : _Unit test related to center model._ <font color="LightGray">(AF)</font>
    - **fsma** : _Unit test related to dendrite simulation._
      - \__init__.py : <font color="LightGray">(AF)</font>
    - **martensite** : _Unit test related to dendrite simulation._
      - \__init__.py : <font color="LightGray">(AF)</font>
