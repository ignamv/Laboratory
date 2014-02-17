import datetime
import numpy as np
import os
import re
import time

from lantz import Q_
from esp300 import ESP300
from HP54616B import HP54616B

# Configuration
axis = 3
lvdt_channel = 1
pmt_channel = 2
oscilloscope_resource = 'GPIB0::14::INSTR'
positioner_resource = 'GPIB0::3::INSTR'
output_directory = 'C:\\ignacio\\mediciones\\slowscan'
output_prefix = 'scan'
output_suffix = '.txt'
progress_indications = 10
measurement_delay = Q_(100,'ms')
measurement_delay.ito('s')
max_scale_changes = 4
# Before running this script, set the home position to where the two path
# lengths coincide
sweep_start = Q_(-300,'um')
sweep_end = Q_(-70,'um')
sweep_points = 30

# Find the number of the last run
try:
    file_regex = output_prefix+r'(\d\d\d\d)'+output_suffix
    matches = (re.match(file_regex, filename) 
               for filename in os.listdir(output_directory))
    run_index = 1 + max(int(match.group(1))
                        for match in matches if match is not None)
except ValueError:
    run_index = 1

filename = os.path.join(output_directory, (output_prefix+'{:04d}'
                                           +output_suffix).format(run_index))

# Initialize instruments
positioner = ESP300(positioner_resource)
positioner.initialize()
oscilloscope = HP54616B(oscilloscope_resource)
oscilloscope.initialize()

# From CMA-12PP manual
positioner.maximum_velocity[axis] = Q_(400,'um/s')
positioner.target_velocity[axis] = positioner.maximum_velocity[axis]/2

oscilloscope.trigger_source = 'line'
# TODO: set channel and horizontal scales

print('Sweeping from {:!s} to {:!s} in {:d} points'.format(
            sweep_start, sweep_end, sweep_points))
positions = np.linspace(sweep_start, sweep_end, sweep_points).to('um')

print('Saving to ' + filename)
output = open(filename, 'w')
headers = dict(velocity=positioner.target_velocity[axis],
               axis=positioner.ID[axis] + ' on ' + str(axis))
output.write(''.join('# {} = {}\n'.format(key, val) 
                     for key,val in headers.items()))
output.write('#Position [um],PMT [V], LVDT [V]\n')

start_time = datetime.datetime.now()
indicator_separation = len(positions) / progress_indications
for i,pos in enumerate(positions):
    positioner.target_position[axis] = pos
    positioner.wait_motion_done()
    time.sleep(measurement_delay.magnitude)
    output.write('{:e}'.format(pos.magnitude))
    for channel in [pmt_channel, lvdt_channel]:
        for ttry in range(max_scale_changes):
            avg = oscilloscope.average_signal[channel]
            if avg.magnitude != oscilloscope.error_value:
                break
            # Signal is outside the display, change scale
            oscilloscope.scale[channel] *= 0.7
            time.sleep(measurement_delay.magnitude)
        if ttry == max_scale_changes:
            raise Exception("Can't find signal in channel {}".format(channel))
        output.write(',{:e}'.format(avg.to('V').magnitude))
    output.write('\n')
    if i*progress_indications % len(positions) == 0:
        print('Progress: {:d}/{:d}'.format(i,len(positions)))
duration = datetime.datetime.now() - start_time
duration_string = 'Elapsed {:f} seconds'.format(duration.total_seconds()) 
print(duration_string)
output.write('# ' + duration_string)
