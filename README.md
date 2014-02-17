Measurement and analysis scripts for an optics measurement setup
================================================================

This is a set of Python scripts written to automate measurements in an optics
experiment and then analyze the results. They were made as part of a
year-long undergraduate research experience at [LEC](http://lec2.df.uba.ar/), where
I worked on adapting an [autocorrelator](https://en.wikipedia.org/wiki/Optical_autocorrelation) 
to enable measurements on low-intensity light coming from a
[photonic crystal fiber](https://en.wikipedia.org/wiki/Photonic_crystal_fiber).

Measurement scripts
-------------------

The actual measurement and analysis scripts are in the autocorrelator/ and 
positioner/ directories, along with several short scripts in the root directory 
for various tasks. Although they are written for my specific experiment and
mechanical setup, they might serve as a guide to others working on a similar
problem.

Instrument drivers
------------------

Such automated measurements require simultaneous control of several
instruments such as oscilloscopes, function generators and motor controllers.
In order to develop a mantainable code base, I used the [Lantz](http://lantz.readthedocs.org/en/latest/)
library to develop Python drivers for each instrument. These drivers are 
completely decoupled from my experiment and may be used and extended by others:

* HP54616B: HP 54616B Digital Storage Oscilloscope (includes a simple user
  interface for interactive use)
* Agilent34405.py: Agilent 34405 5 1/2 digit multimeter
* esp300.py: Newport ESP300 motion controller
* hp33120a.py: HP 33120A function generator
* picotestg5100.py: Picotest G5100 function generator
* sr540.py: Stanford Research SR540 lock-in amplifier

Simulation and analysis
-----------------------

The simulac directory has code for simulating autocorrelations of pulses with a
given envelope. It is also possible to apply 
[MOSAIC](http://www.phys.unm.edu/~opsci/sbahae/research/mosaic/index.htm)
to simulated or measured autocorrelations and detect their envelope for width
or chirp estimation.

