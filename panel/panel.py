# -- encoding: utf-8 --
from PyQt4.uic import loadUiType
from PyQt4.QtGui import QApplication, QFileDialog
from PyQt4.QtCore import pyqtSlot
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg 

from HP54616B.hp54616b import HP54616B
from hp33120a import HP33120A
from picomotor import Picomotor
from lantz import Q_

osc_resource = 'GPIB0::14::INSTR'
gen_resource = 'GPIB0::8::INSTR'
lvdt_channel = 2
lvdt_calibration = 'C:\\ignacio\\mediciones\\lvdt\\calibracion lvdt.csv'
# Edges of AC sweep
lvdt_range = [Q_(-141,'mV'),Q_(140,'mV')]

FormClass, BaseClass = loadUiType('gui.ui')

class Panel(FormClass, BaseClass):
    """User interface for common tasks while using the autocorrelator"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.figure = plt.figure(tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(1,1,1)
        self.groupOsciloscopio.layout().addWidget(self.canvas)

        self.osc = HP54616B(osc_resource)
        self.osc.initialize()
        print(self.osc.idn)

        self.calib_data = np.loadtxt(lvdt_calibration, delimiter=',')
        self.calibration = np.polyfit(self.calib_data[:,1],
                                      self.calib_data[:,0], 1)
        self.fastgen = HP33120A(gen_resource)
        self.fastgen.initialize()

        self.pico = Picomotor(1)

    def lvdt_voltage(self):
        return self.osc.average_signal[lvdt_channel]

    def goto_lvdt(self, position):
        """Move picomotor to the specified LVDT position or voltage"""
        try:
            target = position.to('V')
        except Exception as e:
            position.ito('mm')
            target = Q_((position.magnitude-
                          self.calibration[1])/self.calibration[0],'V')
        direction = target > self.lvdt_voltage()
        print('dir: {}'.format(direction))
        self.pico.moveContinuous(1*direction)
        for i in range(10):
            self.osc.digitize([2])
            print('to {}, at {}'.format(target,self.lvdt_voltage()))
            if (target > self.lvdt_voltage()) != direction:
                # Overshoot
                break
            sleep(.01)
        print('done')
        self.pico.stopContinuous()

    @pyqtSlot()
    def on_adquirir_clicked(self):
        self.osc.stop()
        self.osc.trigger_mode = 'single'
        self.osc.timebase_range = Q_(20,'s')
        print(self.osc.timebase_range)
        print(Q_(1e-3,'s')*self.picoSteps.value())
        self.osc.timebase_delay = self.osc.timebase_range / 2
        self.osc.offset[lvdt_channel] = (lvdt_range[0]+lvdt_range[1])/2
        self.osc.range[lvdt_channel] = Q_(500,'mV')
        self.osc.run()

    @pyqtSlot()
    def on_graficar_clicked(self):
        t, pmt, lvdt = self.osc.data([1,2], existing_data=True)
        self.t = t.to('s').magnitude
        self.pmt = pmt.to('V').magnitude
        lvdt = lvdt.to('V').magnitude
        position = Q_(np.polyval(self.calibration, lvdt),'mm')
        self.tau = (2*position/Q_(3e8,'m/s')).to('fs')
        self.axes.clear()
        self.axes.plot(self.t, self.pmt)
        self.canvas.draw()

    @pyqtSlot()
    def on_guardar_clicked(self):
        filename = QFileDialog.getSaveFileName(self,
                   'Guardar autocorrelación', '', '*.csv')
        np.savetxt(filename, np.column_stack((self.t, self.pmt, self.tau)))

    @pyqtSlot()
    def on_picoMoveSteps_clicked(self):
        self.pico.move(int(self.picoSteps.text()))

    @pyqtSlot()
    def on_barrido_clicked(self):
        self.goto_lvdt(lvdt_range[0])

    @pyqtSlot()
    def on_targetGo_clicked(self):
        print('h')
        self.goto_lvdt(Q_(float(self.target.text()),'mV'))

    @pyqtSlot()
    def on_lvdtGet_clicked(self):
        lvdt_voltage = self.osc.average_signal[lvdt_channel]
        if np.abs(lvdt_voltage.magnitude-self.osc.error_value) \
                / self.osc.error_value < .01:
            self.lvdtPosition.setText('Error')
        else:
            position = Q_(np.polyval(self.calibration,
                                      lvdt_voltage.magnitude), 'mm')
            self.lvdtPosition.setText('{}\n{}'.format(lvdt_voltage,position))

    @pyqtSlot()
    def on_picoCw_pressed(self):
        self.pico.moveContinuous(1)

    @pyqtSlot()
    def on_picoCw_released(self):
        self.pico.stopContinuous()

    @pyqtSlot()
    def on_picoCcw_pressed(self):
        self.pico.moveContinuous(0)

    @pyqtSlot()
    def on_picoCcw_released(self):
        self.pico.stopContinuous()

if __name__ == '__main__':
    from os import sys
    app = QApplication(sys.argv)
    window = Panel()
    window.show()
    exit(app.exec_())

