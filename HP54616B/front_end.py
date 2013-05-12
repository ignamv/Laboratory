import logging
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
from matplotlib.figure import Figure
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QGroupBox,QPushButton,QSpinBox,QCheckBox
import numpy as np

from lantz.ui.qtwidgets import connect_feat, connect_driver

from hp54616b import HP54616B
from main_window import Ui_main_window
from channel_controls import Ui_channel_controls

logger = logging.getLogger('HP54616BFrontEnd')

class HP54616BFrontEnd(QWidget):
    def __init__(self,resource_name,parent=None):
        super().__init__(parent)
        self.inst = HP54616B(resource_name)
        self.inst.initialize()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.plot)

        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        connect_driver(self,self.inst)
        self.channelControls = []
        for channel in self.inst.channels:
            chan = QGroupBox()
            self.channelControls.append(chan)
            chan.n = channel
            Ui_channel_controls().setupUi(chan)
            chan.setTitle('Channel {:d}'.format(channel))
            connect_feat(chan.findChild((QWidget,),'range'), self.inst,
                    'range',channel)
            connect_feat(chan.findChild((QWidget,),'offset'), self.inst,
                    'offset',channel)
            connect_feat(chan.findChild((QWidget,),'visible'), self.inst,
                    'visible',channel)
            self.ui.controlBox.addWidget(chan)

        self.figure = Figure()
        self.figureCanvas = FigureCanvasQTAgg(self.figure)
        self.ui.plotBox.addWidget(self.figureCanvas)
        self.axes = self.figure.add_subplot(111)
        self.ui.plot.clicked.connect(self.plot)
        self.ui.refreshAuto.clicked.connect(self.refreshConfig)
        self.plotDelay = self.findChild((QWidget,),'refreshDelay')

    def plot(self):
        self.axes.cla()
        channels = [chanBox.n for chanBox in self.channelControls
                    if chanBox.findChild((QCheckBox,),'visible').isChecked()]
        logger.info('Plotting channels '+','.join(str(c) for c in channels))
        data = self.inst.data(channels)
        for i in range(len(channels)):
            self.axes.plot(data[0],data[i+1])
        self.figureCanvas.draw()
        if self.ui.refreshAuto.isChecked():
            self.timer.setInterval(self.plotDelay.value())
            self.timer.start()

    def refreshConfig(self,checkState):
        if checkState == 2:
            self.timer.start()
        
    def __del__(self):
        self.inst.finalize()

if __name__=='__main__':
    logger.setLevel(logging.DEBUG)
    from os import sys
    app = QApplication(sys.argv)
    v = HP54616BFrontEnd('GPIB0::14::INSTR')
    v.show()
    exit(app.exec_())


