from math import pi
from . import Q_

LIGHT_SPEED = Q_(3e8,'m/s')
wavelength = Q_(830, 'nm')
pulse_width = Q_(40, 'fs')
angular_frequency = 2*pi*LIGHT_SPEED/wavelength

