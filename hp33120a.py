# -*- coding: utf-8 -*-

import numpy as np

from lantz.visa import GPIBVisaDriver
from lantz import Feat, DictFeat, Q_, Action


class HP33120A(GPIBVisaDriver):
    """Lantz driver for HP 33120A function generator"""

    @Feat
    def idn(self):
        return self.query('*IDN?')

    @Feat(units='V')
    def amplitude(self):
        return self.query('VOLTAGE?')

    @amplitude.setter
    def amplitude(self, amp):
        self.send('VOLTAGE {}'.format(amp))

    @Feat(units='V')
    def offset(self):
        return self.query('VOLTAGE:OFFSET?')

    @offset.setter
    def offset(self, off):
        self.send('VOLTAGE:OFFSET {}'.format(off))

    @Feat(units='Hz')
    def frequency(self):
        return self.query('FREQUENCY?')

    @frequency.setter
    def frequency(self, freq):
        self.send('FREQUENCY {}'.format(freq))


if __name__ == '__main__':
    gen = hp33120a('GPIB0::8::INSTR')
    gen.initialize()
    print(gen.idn)
    print(gen.amplitude)
    print(gen.offset)

