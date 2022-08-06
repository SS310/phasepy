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
  - (Interfacial Fluctuation)
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
<img src="https://latex.codecogs.com/svg.image?\xi\&space;{:}&space;\&space;\textrm{Interfacial\&space;Fluctuation}" alt="fluct" title="fluct">
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
> Definition

**Chemical Energy** is expressed in terms of the energies of the **solid** and **liquid** phases, plus a **penalty** term that is a condition for the non-simultaneous existence of the solid and liquid phases, and can be expressed by the following equation.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?G_{chem}\left&space;(&space;\phi&space;,&space;T&space;\right&space;)=h\left&space;(&space;\phi&space;&space;\right&space;)G_{sol}\left&space;(&space;T&space;&space;\right&space;)&space;&plus;&space;\left&space;[&space;1&space;-&space;h\left&space;(&space;\phi&space;&space;\right&space;)\right&space;]G_{liq}\left&space;(&space;T&space;&space;\right&space;)&plus;Wg\left&space;(&space;\phi&space;&space;\right&space;)" title="G_{chem}\left ( \phi , T \right )=h\left ( \phi \right )G_{sol}\left ( T \right ) + \left [ 1 - h\left ( \phi \right )\right ]G_{liq}\left ( T \right )+Wg\left ( \phi \right )" />
</div>
<br>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?G_{sol}\&space;{:}&space;\&space;\textrm{Chemical\&space;Energy\&space;of\&space;Solid}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?G_{liq}\&space;{:}&space;\&space;\textrm{Chemical\&space;Energy\&space;of\&space;Liquid}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?h\&space;{:}&space;\&space;\textrm{Energy\&space;Destribution\&space;Function}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?g\&space;{:}&space;\&space;\textrm{Double-well\&space;Function}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?W\&space;{:}&space;\&space;\textrm{Energy\&space;Barrier}" alt="ene" title="ene">
</div>
<br>

**Energy-Destribution-Function** is defined as a monotonically increasing function that is compensated for **0 when Φ = 0** and **1 when Φ = 1**, and can be expressed as follows.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?h\left&space;(&space;\phi&space;&space;\right&space;)&space;=&space;\phi&space;^{3}\left&space;(&space;10-15\phi&plus;6\phi^{2}&space;\right&space;)" title="h\left ( \phi \right ) = \phi ^{3}\left ( 10-15\phi+6\phi^{2} \right )" />
</div>
<br>

**Double-well-Function** is a function that is guaranteed to be 0 when Φ = 0,1 and takes maxima between 0~1, and is expressed as follows.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?g\left&space;(&space;\phi&space;&space;\right&space;)&space;=&space;\phi&space;^{2}\left&space;(&space;1-\phi^{2}&space;\right&space;)" title="g\left ( \phi \right ) = \phi ^{2}\left ( 1-\phi^{2} \right )" />
</div>
<br>


> Differential value

From the definition, the derivative of the **Chemical-Energy** is

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;G_{chem}&space;}{\partial&space;\phi&space;}&space;=&space;h^{'}\left&space;(&space;\phi&space;&space;\right&space;)\left&space;(&space;G_{sol}&space;-&space;G_{liq}&space;\right&space;)&space;&plus;&space;Wg^{'}\left&space;(&space;\phi&space;&space;\right&space;)" title="\frac{\partial G_{chem} }{\partial \phi } = h^{'}\left ( \phi \right )\left ( G_{sol} - G_{liq} \right ) + Wg^{'}\left ( \phi \right )" />
</div>
<br>

The following approximate formula is used here.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\left&space;(&space;G_{sol}&space;-&space;G_{liq}&space;\right&space;)&space;=&space;\frac{-L\left&space;(&space;T_{m}&space;-&space;T&space;\right&space;)}{T}" title="\left ( G_{sol} - G_{liq} \right ) = \frac{-L\left ( T_{m} - T \right )}{T}" />
</div>
<br>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?L\&space;{:}&space;\&space;\textrm{Latent\&space;Heat}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?T_{m}\&space;{:}&space;\&space;\textrm{Melting\&space;Point}" alt="ene" title="ene">
</div>
<br>

Using this approximation, the derivative of the **Chemical-Energy** can be calculated. However, the temperature is given by the following thermal diffusion equation.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;T}{\partial&space;t}&space;=&space;\frac{1}{C_{p}}\left&space;[&space;K\triangledown&space;^{2}T&plus;30\phi&space;^{2}\left&space;(&space;1-\phi&space;&space;\right&space;)^{2}L&space;\frac{\phi&space;T}{\partial&space;t}\right&space;]" title="\frac{\partial T}{\partial t} = \frac{1}{C_{p}}\left [ K\triangledown ^{2}T+30\phi ^{2}\left ( 1-\phi \right )^{2}L \frac{\phi T}{\partial t}\right ]" />
</div>
<br>
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?C_{p}\&space;{:}&space;\&space;\textrm{Specific\&space;Heat}" alt="ene" title="ene">
</div>
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?K\&space;{:}&space;\&space;\textrm{Thermal\&space;Conductivity
}" alt="ene" title="ene">
</div>
<br>

#### Gradient Energy
> Definition

**Gradient-Energy** is expressed using the derivative with respect to the position of the phase field variable Φ as follows.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?G_{grad}\left&space;(&space;\phi&space;&space;\right&space;)&space;=&space;\frac{1}{2}\varepsilon&space;&space;^{2}\left|\triangledown&space;\phi&space;\right|^{2}" title="G_{grad}\left ( \phi \right ) = \frac{1}{2}\varepsilon ^{2}\left|\triangledown \phi \right|^{2}" />
</div>
<br>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?\varepsilon\&space;{:}&space;\&space;\textrm{Gradient-Energy\&space;Cofficient}" alt="ene" title="ene">
</div>
<br>

**Gradient-Energy-Coefficient** has a directional dependence, where the energy increases or decreases with respect to the θ direction, and is expressed as follow.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\varepsilon&space;\left&space;(&space;\theta&space;&space;&space;\right&space;)&space;=&space;\varepsilon_{0}\left\{&space;1&space;&plus;&space;\zeta&space;cos\left&space;[&space;k\left&space;(&space;\theta&space;-&space;\theta_{0}&space;\right&space;)&space;\right&space;]\right\}" title="\varepsilon \left ( \theta \right ) = \varepsilon_{0}\left\{ 1 + \zeta cos\left [ k\left ( \theta - \theta_{0} \right ) \right ]\right\}" />
</div>
<br>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?\zeta\&space;{:}&space;\&space;\textrm{Anisotropic \&space;Strength}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?k\&space;{:}&space;\&space;\textrm{Frequency}" alt="ene" title="ene">
</div>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?\theta_{0}\&space;{:}&space;\&space;\textrm{Angle\&space;of\&space;Anisotropy}" alt="ene" title="ene">
</div>
<br>

> Differential value

From the definition, the derivative of the **Gradient-Energy** is

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\frac{\partial&space;G_{grad}}{\partial&space;\phi}&space;=&space;-\varepsilon&space;^{2}\left&space;(&space;\frac{\partial^{2}&space;\phi}{\partial&space;x^{2}}&space;&plus;&space;\frac{\partial^{2}&space;\phi}{\partial&space;y^{2}}&space;\right&space;)&space;-&space;\varepsilon&space;\varepsilon&space;^{'}\left&space;[&space;\left&space;(&space;\frac{\partial^{2}&space;\phi}{\partial&space;x^{2}}&space;&plus;&space;\frac{\partial^{2}&space;\phi}{\partial&space;y^{2}}&space;\right&space;)sin2\theta&space;&plus;&space;2\frac{\partial^{2}&space;\phi}{\partial&space;x\partial&space;y}cos2\theta&space;\right&space;]&space;&plus;&space;\frac{1}{2}\left&space;(&space;\varepsilon&space;^{'2}-&space;\varepsilon&space;^{''}&space;\right&space;)\left&space;[&space;2\frac{\partial^{2}&space;\phi}{\partial&space;x\partial&space;y}sin2\theta-\left&space;(&space;\frac{\partial^{2}&space;\phi}{\partial&space;x^{2}}&space;&plus;&space;\frac{\partial^{2}&space;\phi}{\partial&space;y^{2}}&space;\right&space;)-\left&space;(&space;\frac{\partial^{2}&space;\phi}{\partial&space;y^{2}}&space;&plus;&space;\frac{\partial^{2}&space;\phi}{\partial&space;x^{2}}&space;\right&space;)cos2\theta&space;\right&space;]" title="\frac{\partial G_{grad}}{\partial \phi} = -\varepsilon ^{2}\left ( \frac{\partial^{2} \phi}{\partial x^{2}} + \frac{\partial^{2} \phi}{\partial y^{2}} \right ) - \varepsilon \varepsilon ^{'}\left [ \left ( \frac{\partial^{2} \phi}{\partial x^{2}} + \frac{\partial^{2} \phi}{\partial y^{2}} \right )sin2\theta + 2\frac{\partial^{2} \phi}{\partial x\partial y}cos2\theta \right ] + \frac{1}{2}\left ( \varepsilon ^{'2}- \varepsilon ^{''} \right )\left [ 2\frac{\partial^{2} \phi}{\partial x\partial y}sin2\theta-\left ( \frac{\partial^{2} \phi}{\partial x^{2}} + \frac{\partial^{2} \phi}{\partial y^{2}} \right )-\left ( \frac{\partial^{2} \phi}{\partial y^{2}} + \frac{\partial^{2} \phi}{\partial x^{2}} \right )cos2\theta \right ]" />
</div>
<br>

#### Interfacial Fluctuation
> Difinition

From a physical point of view, the **Interfacial-Fluctuation** is proportional to the energy barrier and is expressed as follows, with a minimum value of **0 at Φ = 0,1** and a **maximum value at Φ = 0.5**.

<br>
<div align="center">
<img src="https://latex.codecogs.com/svg.image?\xi&space;=&space;4W\phi&space;\left&space;(&space;1-\phi&space;&space;\right&space;)&space;\chi&space;" title="\xi = 4W\phi \left ( 1-\phi \right ) \chi " />
</div>
<br>
<div align="right">
<img src="https://latex.codecogs.com/svg.image?\chi\&space;{:}&space;\&space;\textrm{Random\&space;Number}" alt="ene" title="ene">
</div>
<br>