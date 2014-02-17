from picotestg5100 import PicotestG5100
from lantz import Q_
from ctypes import windll
from time import sleep

class Picomotor(object):
    def __init__(self, channel, port = 0x378):
        """Picomotor handler

        port: parallel port I/O address
        channel: 0 to 2, picomotor driver output"""
        self.channel = channel
        self.port = port
        self.lib = windll.io
        self.gen = PicotestG5100('USB0::5710::5100::tw00009115::0::INSTR')
        self.gen.initialize()
        self.gen.burst_mode = 'triggered'
        self.gen.function = 'square'
        self.gen.frequency = Q_(1.,'kHz')
        self.gen.trigger_source = 'bus'
        self.gen.offset = Q_(2.5,'V')
        self.gen.amplitude = Q_(5,'V')
        self.stopContinuous()
        self.gen.output = True

    def __del__(self):
        self.gen.output = False

    def moveContinuous(self, direction):
        directionBit = 8*direction
        self.lib.PortOut(self.port, directionBit << self.channel)
        self.gen.burst = False

    def stopContinuous(self):
        self.gen.burst_cycles = 1
        self.gen.burst = True
        
    def move(self, delta):
        """Strobe stepX while holding the requested direction
        direction: 0 for CCW, 1 for CW
        """
        # Adapter pinout:
        # D0: stepA
        # D1: stepB
        # D2: stepC
        # D3: stepA
        # D4: stepB
        # D5: stepC
        if delta == 0:
            return
        nsteps = int(abs(delta))
        direction = [0,1][delta>0]
        directionBit = 8*direction
        self.lib.PortOut(self.port, directionBit << self.channel)
        self.gen.burst = True
        self.gen.burst_cycles = nsteps
        self.gen.trigger()

if __name__ == '__main__':
    from PyQt4.QtGui import QApplication, QWidget,  QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel
    from PyQt4.QtCore import Qt
    from os import sys
    picomotor = Picomotor(1)
    pasos = [-10000, -1000, -100, 100, 1000, 10000]
    app = QApplication(sys.argv)
    # TODO: hacer interfase mas linda en QT designer
    ventana = QWidget()
    ventana.setLayout(QVBoxLayout())
    label = QLabel('CCW\tCW')
    label.setAlignment(Qt.AlignHCenter)
    ventana.layout().addWidget(label)
    pasos_fijos = QHBoxLayout()
    for paso in pasos:
        bot = QPushButton(str(paso))
        class closure():
            def __init__(self,paso):
                self.paso = paso
            def __call__(self):
                print('Moviendo {}'.format(self.paso))
                picomotor.move(self.paso)
        bot.clicked.connect(closure(paso))
        pasos_fijos.addWidget(bot)
    ventana.layout().addLayout(pasos_fijos)
    manual = QHBoxLayout()
    entrada_pasos = QLineEdit('250')
    manual.addWidget(entrada_pasos)
    dar_pasos = QPushButton('Mover')
    def dar_pasos_clicked():
        pasos = int(entrada_pasos.text())
        print('Moviendo {}'.format(pasos))
        picomotor.move(pasos)
    dar_pasos.clicked.connect(dar_pasos_clicked)
    manual.addWidget(dar_pasos)
    ventana.layout().addLayout(manual)
    ventana.show()
    exit(app.exec_())

