import argparse
import numpy as np
from lantz import Q_
from HP54616B import HP54616B

# Plot PMT and LVDT data from a slow scan measurement

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

fd = open(args.filename, 'r')

headers = {}
while fd.read(2) == '# ':
    key, val = fd.readline()[:-1].split('=')
    headers[key] = val
fd.close()

data = np.loadtxt(args.filename, delimiter=',')
position = Q_(data[:,0],'um')
pmt = Q_(data[:,1],'V')
lvdt = Q_(data[:,2],'V')
valid = (( pmt.magnitude != HP54616B.error_value) * 
         (lvdt.magnitude != HP54616B.error_value))
pmt = pmt[valid]
lvdt = lvdt[valid]
position = position[valid]
print('{} invalid points'.format(len(valid)-sum(valid)))

from matplotlib import pyplot as plt
plt.plot(position, pmt)
plt.plot(position, lvdt)
plt.show()
plt.savefig(args.filename+'.pdf')
