#-- encoding: utf-8 --
from HP54616B import HP54616B
import numpy as np
from lantz import Q_

oscilloscope_resource = 'GPIB0::14::INSTR'

osc = HP54616B(oscilloscope_resource)
osc.initialize()
t, ch1, ch2 = osc.data([1,2], True)

from matplotlib import pyplot as plt
fig = plt.figure()
fig.add_subplot(2,2,1)
plt.plot(t, ch1)
fig.add_subplot(2,2,2)
plt.plot(t, ch2)
fig.add_subplot(2,2,3)
plt.plot(ch1, ch2)
plt.show()

