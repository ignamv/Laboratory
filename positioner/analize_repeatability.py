#--encoding: utf-8 --
import numpy as np
import os
from matplotlib import pyplot as plt
from os import listdir

"""Analyze output of repetibilidad.py
"""
output_directory = 'C:\\ignacio\\mediciones\\posicionador\\repetibilidad'

if len(os.sys.argv) == 2:
    filename = os.sys.argv[1]
else:
    filename = output_directory + '\\' + sorted(filename for filename in 
               listdir(output_directory) if len(filename)==10
               and filename[:3]=='run' and filename[6:]=='.csv')[-1]
               
print('Analysing ' + filename)
# Prefix all generated graphs with this string
prefix = filename[:filename.rfind('.')] + '_'

fd = open(filename, 'r', encoding='utf-8')
filedata = {}
while fd.read(2) == '# ':
    key, val = fd.readline()[:-1].split('=')
    filedata[key] = val
print(filedata)
# I can't unread the last two characters, so re-open the file
fd.close()
cycles = int(filedata['cycles'])

register = np.dtype([('positioner', np.float), ('lvdt', np.float)])
data = np.loadtxt(filename, delimiter=',', dtype=register)
data = np.sort(data, order='positioner')
positioner, indices = np.unique(data['positioner'], return_inverse=True)
lvdt_avg = np.empty(len(positioner))
lvdt_std = np.empty(len(positioner))

for i, position in enumerate(positioner):
    lvdt_avg[i] = np.mean(data['lvdt'][indices==i])
    lvdt_std[i] = np.std(data['lvdt'][indices==i])

plt.plot(positioner, lvdt_std, 'x')
plt.xlabel('Posicionador [mm]')
plt.ylabel('Desviación estandard LVDT [mm]')
plt.savefig(prefix+'stdev.pdf')
plt.figure()
plt.plot(positioner, lvdt_avg, 'x')
plt.xlabel('Posicionador [mm]')
plt.ylabel('Promedio LVDT [mm]')
plt.savefig(prefix+'avg.pdf')
