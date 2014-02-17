from lantz import Feat, DictFeat, Action
from lantz.visa import GPIBVisaDriver

class PicotestG5100(GPIBVisaDriver):
    def initialize(self):
        super().initialize()
        self.send('VOLTAGE:UNIT VPP')
    @Feat()
    def idn(self):
        """Instrument type and software version

        Return a string with the format
            HEWLETT-PACKARD,<model>, 0, X<NL>
        <model> ::= the model number of the instrument
        X ::= the software revision of the instrument.
        """
        return self.query('*IDN?')

    @Action()
    def trigger(self):
        self.send('*TRG')

    @Feat(values={'immediate':'IMM','external':'EXT','bus':'BUS'})
    def trigger_source(self):
        return self.query('TRIGGER:SOURCE?')

    @trigger_source.setter
    def trigger_source(self, source):
        self.send('TRIGGER:SOURCE {}'.format(source))

    @Feat(values={True:'1',False:'0'})
    def burst(self):
        return self.query('BURST:STATE?')

    @burst.setter
    def burst(self, val):
        self.send('BURST:STATE {}'.format(val))

    @Feat(values={'sinusoid':'SIN','square':'SQU','ramp':'RAMP','pulse':'PULS',
                  'user':'USER'})
    def function(self):
        return self.query('function?')

    @function.setter
    def function(self, function):
        self.send('function {}'.format(function))

    @Feat(units='Hz')
    def frequency(self):
        return self.query('FREQUENCY?')

    @frequency.setter
    def frequency(self, f):
        self.send('FREQUENCY {}'.format(f))

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

    @Feat(values={'triggered':'TRIG','gated':'GAT'})
    def burst_mode(self):
        return self.query('BURST:MODE?')

    @burst_mode.setter
    def burst_mode(self, mode):
        self.send('BURST:MODE {}'.format(mode))

    @Feat
    def burst_cycles(self):
        return int(float(self.query('BURST:NCYCLES?')))

    @burst_cycles.setter
    def burst_cycles(self, cycles):
        self.send('BURST:NCYCLES {}'.format(cycles))

    @Feat(values={True:'1', False:'0'})
    def output(self):
        return self.query('OUTPUT?')

    @output.setter
    def output(self, value):
        self.send('OUTPUT {}'.format(value))

if __name__ == '__main__':
    from lantz import Q_
    gen = PicotestG5100('USB0::5710::5100::tw00009115::0::INSTR')
    gen.initialize()
    gen.burst_mode = 'triggered'
    gen.burst_cycles = 10
    gen.function = 'square'
    gen.frequency = Q_(1,'kHz')
    gen.offset = Q_(2.5,'V')
    gen.amplitude = Q_(5,'V')

    print(gen.idn)
    print(gen.function)
    print(gen.frequency)
    print(gen.amplitude)
    print(gen.offset)
    print(gen.output)
    print(gen.burst_mode)
    print(gen.burst_cycles)
    
    while True:
        i = input()
        if i == 'q':
            break
        gen.trigger()
