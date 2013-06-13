from HP54616B.hp54616b import HP54616B
from esp300 import ESP300
import numpy as np
from lantz import Q_

# LVDT calibration file.
# First column: position in mm
# Second column: voltage in V
calibration_file = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'
axis = 1

osc = HP54616B('GPIB0::14::INSTR')
osc.initialize()
# TODO: acquire the minimum possible number of points
#osc.points = 100

positioner = ESP300('GPIB0::3::INSTR')
positioner.initialize()
# From CMA-12PP manual
positioner.maximum_velocity[axis] = Q_(400,'um/s')
positioner.target_velocity[axis] = positioner.maximum_velocity[axis]/2

# Read calibration
calib_data = np.loadtxt(calibration_file, delimiter=',')
calibration = np.polyfit(calib_data[1], calib_data[0], 1)

def read_lvdt():
    """Position registered by the LVDT according to the calibration"""
    voltages = osc.data([1])[1].to('V').magnitude
    positions = Q_(np.polyval(calibration, voltages), 'mm')
    return np.mean(positions)

base = read_lvdt()
# Change calibration so this is the origin of coordinates
calibration[1] -= base.to('mm').magnitude
positioner.position[axis] = Q_(0,'mm')

displacement = Q_(5,'s') * positioner.target_velocity[axis]
print('LVDT: {:!s}'.format(read_lvdt().to('mm')))
print('Positioner: {:!s}'.format(positioner.position[axis].to('mm')))
print('Moving {:!s}'.format(displacement.to('mm')))
positioner.move(axis, displacement)
positioner.wait_motion_done()
print('LVDT: {:!s}'.format(read_lvdt().to('mm')))
print('Positioner: {:!s}'.format(positioner.position[axis].to('mm')))
print('Moving {:!s}'.format(-displacement.to('mm')))
positioner.move(axis, -displacement)
positioner.wait_motion_done()
print('LVDT: {:!s}'.format(read_lvdt().to('mm')))
print('Positioner: {:!s}'.format(positioner.position[axis].to('mm')))

osc.finalize()
positioner.finalize()
