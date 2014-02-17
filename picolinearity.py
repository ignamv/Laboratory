#-- encoding: utf-8 --
from HP54616B import HP54616B
import numpy as np
from lantz import Q_
from os import listdir

calibration_file = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'
oscilloscope_resource = 'GPIB0::14::INSTR'
output_directory = 'C:\\ignacio\\mediciones\\picomotor'

# Find the number of the last test run
try:
    testrun_index = 1 + max(int(filename[7:10]) for filename 
            in listdir(output_directory) if filename[:7]=='testrun')
except Exception as e:
    testrun_index = 1

osc = HP54616B(oscilloscope_resource)
osc.initialize()
osc.stop()
osc.complete_percent = 0
osc.trigger_mode = 'single'
print('Prende el generador')
input()
osc.run()
print('Decime cuando termine')
input()
osc.stop()
t, ch1, ch2 = osc.data([1,2])

from matplotlib import pyplot as plt

plt.plot(t,ch1,label='Channel 1')
plt.plot(t,ch2,label='Channel 2')
plt.legend()
plt.show()
