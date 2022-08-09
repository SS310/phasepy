"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import os

#********** Import original module **********
from phasepy.dendrite.main.round_center import RoundCenter
from phasepy._const import PathConst
from phasepy.dendrite.variable.update._energy import PhaseEnergy
from phasepy.dendrite.variable.update._field import UpdateFeild
from phasepy.dendrite.variable.init._field import InitField

#********** Constant Value **********

#********** Class **********

class RoundCenter(RoundCenter):
    def __init__(self) -> None:
        super().__init__()

    def test_set(self):
        """
        """
        input_path = os.path.join(PathConst.DENDRITE.DATA, "RoundCenter", "format.yaml")
        self.set_input_path(input_path=input_path)
        self.whole_val.set()

    def test_main(self):
        self._init_field()
        self._calc_energy()
        self._update_field()

    def test_update_phase(self):
        InitField.Phase.round_center(simu_val=self.whole_val.simu_val, cell_val=self.whole_val.cell_val, model_val=self.whole_val.model_val)

    def test_update_tem(self):
        InitField.Temperture.center(simu_val=self.whole_val.simu_val, prop_val=self.whole_val.prop_val, cell_val=self.whole_val.cell_val)

    def test_calc_chem_drive(self):
        PhaseEnergy.Chemical.calc_drive(simu_val=self.whole_val.simu_val, prop_val=self.whole_val.prop_val, cell_val=self.whole_val.cell_val)
    
    def test_calc_grad_drive(self):
        PhaseEnergy.Gradient.calc_drive(simu_val=self.whole_val.simu_val, prop_val=self.whole_val.prop_val, cell_val=self.whole_val.cell_val)
  
    def test_calc_fluct_drive(self):
        PhaseEnergy.ThermalFluct.calc_drive(simu_val=self.whole_val.simu_val, prop_val=self.whole_val.prop_val, cell_val=self.whole_val.cell_val)

    def test_calc_chem_energy(self):
        PhaseEnergy.Chemical.calc_energy(simu_val=self.whole_val.simu_val, prop_val=self.whole_val.prop_val, cell_val=self.whole_val.cell_val)

    def test_calc_grad_energy(self):
        PhaseEnergy.Gradient.calc_energy(simu_val=self.whole_val.simu_val, prop_val=self.whole_val.prop_val, cell_val=self.whole_val.cell_val)