#--encoding: utf-8 --

from lantz import Feat, DictFeat, Action, Q_
from lantz.visa import USBVisaDriver


class Agilent34405(USBVisaDriver):
    """Lantz driver for the Agilent 34405 5 1/2 digit multimeter"""

    def initialize(self):
        super().initialize()
        self.magnitude = None

    @Feat
    def id(self):
        return self.query('*IDN?')

    def configure(self, magnitude, _range='AUTO', resolution='DEF'):
        # TODO: implement current, frequency and other measurements
        if magnitude != 'VOLTAGE:DC':
            raise NotImplemented
        self.send('CONFIGURE:VOLTAGE:DC {},{}'.format(_range, resolution))
        self.magnitude = 'VOLTAGE:DC'

    @Feat(units='V')
    def voltageDC(self):
        if self.magnitude != 'VOLTAGE:DC':
            self.configure('VOLTAGE:DC')
        return self.query('READ?')

if __name__ == '__main__':
    dmm = Agilent34405('USB0::0x0957::0x0618::tw46300037::0::INSTR')
    dmm.initialize()
    print('ID: {}'.format(dmm.id))
    dmm.configure('VOLTAGE:DC', '100mV')
    import numpy as np
    import os
    import re
    import time
    NSAMPLES = 800
    samples = np.empty((NSAMPLES))
    output_directory = 'C:\\ignacio\\mediciones\\multimetro'
    output_prefix = 'regularidad'
    output_suffix = '.txt'
    # Find the number of the last run
    try:
        file_regex = output_prefix+r'(\d\d\d\d)'+output_suffix
        matches = (re.match(file_regex, filename) 
                   for filename in os.listdir(output_directory))
        run_index = 1 + max(int(match.group(1))
                            for match in matches if match is not None)
    except ValueError:
        run_index = 1

    filename = os.path.join(output_directory,
                            (output_prefix+'{:04d}'.format(run_index)
                             +output_suffix))
    output = open(filename, 'w')
    output.write('# Medición de regularidad de sampleo del multímetro\n')
    output.write('# Entrada es rampa de 1Hz, tensión indica t mod 1s\n')
    start = time.clock()
    for i in range(NSAMPLES):
        output.write('{:e}\t{:e}\n'.format(dmm.voltageDC.to('V').magnitude,
                                           time.clock()-start))
        #if (i*20) % NSAMPLES == 0:
            #print('{}/{}'.format(i,NSAMPLES))
