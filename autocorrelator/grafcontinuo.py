import numpy as np

lvdt, pmt = np.loadtxt('raw.txt')
from matplotlib import pyplot as plt
#plt.plot(lvdt)
#plt.plot(lvdt,  pmt)
plt.plot( pmt)
plt.show()
