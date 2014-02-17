#--encoding: utf-8 --
import numpy as np
from matplotlib import pyplot as plt

calibration_file = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'

calib_data = np.loadtxt(calibration_file, delimiter=',')
# Ajuste lineal para distancia en funcion de tensión
calibration = np.polyfit(calib_data[:,1],
                         calib_data[:,0],
                         1)

# Grafico ajuste vs mediciones
plt.xlabel('Voltage [V]')
plt.ylabel('Distance [mm]')
plt.plot(calib_data[:,1],calib_data[:,0], '-x', label='Measured')
fit = np.polyval(calibration, calib_data[:,1])
plt.plot(calib_data[:,1],fit, '-x', label='Fit')
plt.legend()
plt.show()

print(calibration)
