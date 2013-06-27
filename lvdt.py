from HP54616B.hp54616b import HP54616B
from lantz import Q_
import numpy as np

class LVDT():
    def __init__(self, calibration_file, oscilloscope_resource):
        # LVDT calibration file.
        # First column: position in mm
        # Second column: voltage in V

        self.osc = HP54616B(oscilloscope_resource)
        self.osc.initialize()
        # TODO: acquire the minimum possible number of points to improve speed
        #osc.points = 100

        # Read calibration
        self.calib_data = np.loadtxt(calibration_file, delimiter=',')
        self.calibration = np.polyfit(self.calib_data[:,1],
                                      self.calib_data[:,0], 1)

    def __del__(self):
        self.osc.finalize()

    def read(self):
        """Position registered by the LVDT according to the calibration"""
        voltages = self.osc.average_signal[1].to('V').magnitude
        positions = Q_(np.polyval(self.calibration, voltages), 'mm')
        return np.mean(positions)

    def set(self, position):
        """Alter calibration so that the current physical position matches 
        argument 'position'"""
        self.calibration[1] += (position - self.read()).to('mm').magnitude

if __name__=='__main__':
    calibration_file = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'
    oscilloscope_resource = 'GPIB0::14::INSTR'
    lvdt = LVDT(calibration_file, oscilloscope_resource)
    print(lvdt.calibration)
    lvdt.set(Q_(0,'mm'))
    while True:
        print(lvdt.read())
        input()
