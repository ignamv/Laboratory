from HP54616B import HP54616B
from PyQt4 import QtGui, QtCore

class vavg_meter(QtGui.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.osc = HP54616B('GPIB0::14::INSTR')
        self.osc.initialize()
        self.setLayout(QtGui.QVBoxLayout())
        self.readouts = [QtGui.QLabel('Waiting for channel {}'.format(channel))
                         for channel in self.osc.channels]
        for readout in self.readouts:
            self.layout().addWidget(readout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.read)
        self.timer.start()

    def read(self):
        for i,ch in enumerate(self.osc.channels):
            self.readouts[i].setText(
                    '<span style="font-size: 45pt;">Ch{}: {}</span>'.format(ch,
                    self.osc.average_signal[ch].to('mV').magnitude))

if __name__ == '__main__':
    import os
    app = QtGui.QApplication(os.sys.argv)
    v = vavg_meter()
    v.show()
    exit(app.exec_())


