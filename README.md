# LEAF: Low-Voltage Energy Aggregation Framework

LEAF models the voltage and phase dynamics of a low inertia inverter based Microgrid
in islanded operation. In such case, the network is less robust to disturbances due to the lack of associated
inertia within an inverter. In islanded operation, the assumption of a stiff grid is no longer valid
due to the voltage and phase adjustment based on conventional droop control have a resulting effect on the power
flows throughout the network where voltage and frequency stability of the network may be compromised. Other approaches neglect the network dynamics when 
there are power imbalances in the system and how each node is affected and if the resulting increase in demand can be met with the
available power generation. This paper uses the fact that the phase dynamics of coupled inverters that
employ droop control closely resemble the phase dynamics proposed by the Kuramoto model. Using this
model allows the network stability to be analyzed under the true nonlinear operation

## Cloning the Repo
```
pip3 install virtualenv
virtualenv venv
source ./venv/bin/activate
which python
python --version
pip install -r requirements.txt
```