# phasepy
- **phasepy** is a package for running various simulations using the phase field method.
- The phase-field method follows the following Time-Dependent-Ginzburg-Landau(TDGL) equation.

> TDGL equation

<div align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;\phi}{\partial&space;t}&space;=&space;-&space;M_{\phi}\&space;\frac{\partial&space;G_{sys}}{\partial&space;\phi}" alt="tdgl" title="tdgl">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?G_{sys}\&space;{:}&space;\&space;\textrm{Free\&space;Energy}" alt="ene" title="ene">
</div>
<br>

## Simulation Content

### 1. Dendrite Simulation

Theory is [here](./doc/theory/dendrite.md)

> Governing equation

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;\phi}{\partial&space;t}&space;=&space;-&space;M_{\phi}&space;\left&space;(&space;\frac{\partial&space;G_{sys}}{\partial&space;\phi}&space;&plus;&space;\xi\right&space;)" alt="tdgl" title="tdgl">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?G_{sys}\&space;{:}&space;\&space;\textrm{Free\&space;Energy}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?\xi\&space;{:}&space;\&space;\textrm{Interfacial\&space;Fluctuation}" alt="fluct" title="fluct">
</div>
<br>

> 1-1. RoundCenterModel
 
Tutorial is [here](./doc/tutorial/dendrite/round_center.ipynb)

- This model simulates the generation of a **round** initial nucleus from the center
- Available for **ver.0.1.0** or later.

||||||
|-|-|-|-|-|
|![D_RC_0](./data/dendrite/round_center/data_0.png)|![D_RC_2000](./data/dendrite/round_center/data_2000.png)|![D_RC_5000](./data/dendrite/round_center/data_5000.png)|![D_RC_10000](./data/dendrite/round_center/data_10000.png)|![D_RC_20000](./data/dendrite/round_center/data_20000.png)|

### Martensite Simulation

Planned Development...

### FSMA Simulation

Planned Development...