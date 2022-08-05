# Theory for dendrite simulation
-----

### Agenda

- Governing equation
- Energy
  - Chemical Energy
    - Definition
    - Differential value
  - Gradient Energy
    - Definition
    - Differential value
  - (Thermal Fluctuation)
    - Definition
-----


### Governing equation

> Time-Dpend-Ginzburg-Landau equation

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;\phi}{\partial&space;t}&space;=&space;-&space;M_{\phi}&space;\left&space;(&space;\frac{\partial&space;G_{sys}}{\partial&space;\phi}&space;&plus;&space;\xi\right&space;)" alt="tdgl" title="tdgl">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?G_{sys}\&space;{:}&space;\&space;\textrm{Free\&space;Energy}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?\xi\&space;{:}&space;\&space;\textrm{Thermal\&space;Fluctuation}" alt="fluct" title="fluct">
</div>
<br>

- The above equation can be expanded with appropriate time increments Δt to describe the change of the phenomenon over time
- The phase field variable Φ represents the solid phase and is expressed as 0~1. That is, the liquid phase is represented by (1-Φ).
- To find Φ after Δt, it is necessary to calculate Φ = Φ + ΔΦ using ΔΦ obtained by multiplying both sides by Δt.
- In other words, it is very important to find the derivative terms of the energy on the left-hand side, and these are explained below

> Free Energy

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?G_{sys}=G_{chem}&space;&plus;&space;G_{grad}" title="G_{sys}=G_{chem} + G_{grad}" />
</div>
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?G_{chem}\&space;{:}&space;\&space;\textrm{Chemical\&space;Energy}" alt="ene" title="ene">
</div>
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?G_{grad}\&space;{:}&space;\&space;\textrm{Gradient\&space;Energy}" alt="ene" title="ene">
</div>
<br>

-----

### Energy

#### Chemical Energy

##### Definition

##### Differential value



#### Chemical Energy

##### Definition

##### Differential value



##### Thermal Fluctuation

##### Difinition
