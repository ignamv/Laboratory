#--encoding: utf-8 --
import logging
import os.path
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
from matplotlib.figure import Figure
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QSpinBox, QCheckBox, QFileDialog
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
        self.timer.timeout.connect(self.refresh)

        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        connect_driver(self,self.inst)
        self.channelControls = []
        for channel in self.inst.channels:
            chan = QGroupBox()
            self.channelControls.append(chan)
            chan.n = channel
            chan_ui = Ui_channel_controls()
            chan_ui.setupUi(chan)
            chan.setTitle('Channel {:d}'.format(channel))
            connect_feat(chan_ui.range, self.inst, 'range', channel)
            connect_feat(chan_ui.offset, self.inst, 'offset', channel)
            connect_feat(chan_ui.visible, self.inst, 'visible', channel)
            self.ui.controlBox.addWidget(chan)

        self.figure = Figure()
        self.figureCanvas = FigureCanvasQTAgg(self.figure)
        self.ui.plotBox.addWidget(self.figureCanvas)
        self.axes = self.figure.add_subplot(111)
        self.ui.plot.clicked.connect(self.refresh)
        self.ui.save.clicked.connect(self.save)
        self.ui.checkMosaic.stateChanged.connect(self.setMosaic)
        self.ui.refreshAuto.clicked.connect(self.refreshConfig)
        self.plotDelay = self.findChild((QWidget,),'refreshDelay')
        self.mosaic = False

    def setMosaic(self, state):
        # TODO: put this somewhere sane
        self.mosaic = (state == 2)

    def refresh(self):
        self.axes.cla()
        channels = [chanBox.n for chanBox in self.channelControls
                    if chanBox.findChild((QCheckBox,),'visible').isChecked()]
        logger.info('Fetching channels '+','.join(str(c) for c in channels))
        worker = dataWorker(self.inst, channels)
        self.thread = QThread()
        worker.moveToThread(self.thread)
        thread.started.connect(worker.fetchData)
        worker.output.connect(self.plot)
        self.thread.start()

    class dataWorker(QObject):
        output = pyqtSignal(np.ndarray, list)
        def __init__(self, instrument, channels):
            super().__init__()
            self.channels = channels
            self.instrument = instrument

        @pyqtSlot
        def fetchData(self):
            self.output.emit(self.instrument.data(self.channels), self.channels)

    @pyqtSlot(np.ndarray, list)
    def plot(self, data, channels):
        self.thread = None
        logger.info('Plotting')
        for i in range(len(channels)):
            if self.mosaic:
                spectrum = np.fft.fft(self.data[i+1])
                # TODO: make this configurable
                # spectrum has peaks on 0, +-w and +-2w
                # cut the first peak so the maximum is in w
                crop = 10
                w = np.argmax(spectrum[crop:len(spectrum)/2])+crop
                print('Central: {}'.format(w))
                print('Nyquist: {}'.format(len(spectrum)/2))
                index = int(w/2)
                spectrum[index:3*index] = 0
                spectrum[-3*index:-index] = 0
                spectrum[3*index:5*index] *= 2
                spectrum[-5*index:-3*index] *= 2
                mosaic = np.abs(np.fft.ifft(spectrum))
                self.axes.plot(self.data[0],-self.data[i+1])
                self.axes.plot(self.data[0],mosaic)
            else:
                self.axes.plot(self.data[0],self.data[i+1])
        self.figureCanvas.draw()
        if self.ui.refreshAuto.isChecked():
            self.timer.setInterval(self.plotDelay.value())
            self.timer.start()

    #FIXME: this method is called twice on every button press
    def save(self):
        filename = QFileDialog.getSaveFileName(self, 'Save screen', 'C:\\',
                'CSV file (*.csv *.txt))')
        logger.info('Saving at ' + filename)
        np.savetxt(filename, [d.magnitude for d in self.data],
                   delimiter=',')

    def refreshConfig(self,checkState):
        if checkState == 2:
            self.timer.start()
        else:
            self.timer.stop()
        
    def closeEvent(self, event):
        self.inst.finalize()


if __name__=='__main__':
    logger.setLevel(logging.DEBUG)
    from os import sys
    app = QApplication(sys.argv)
    app.setOrganizationName('Laboratory')
    app.setApplicationName('HP54616B Frontend')
    v = HP54616BFrontEnd('GPIB0::14::INSTR')
    v.showMaximized()
    exit(app.exec_())


