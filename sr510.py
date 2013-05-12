# -*- coding: utf-8 -*-
"""
    SR510
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Implements the drivers to control a lock-in amplifier

    :copyright: 2013 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.

    Source: SR510 Manual
"""

from lantz import Feat
from lantz.visa import GPIBVisaDriver


class SR510(GPIBVisaDriver):
    """SR510 Lock-In Amplifier
    """

    ENCODING = 'ascii'
    RECV_TERMINATION = '\r\n'
    SEND_TERMINATION = '\r\n'

    @Feat(units='Hz')
    def frequency(self):
        """Reference frequency
        """
        return float(self.query('F'))

    @Feat(limits=(-180, 180))
    def phase(self):
        """Phase
        """
        return float(self.query('P'))

    @phase.setter
    def phase(self, value):
        print(self.query('P {:.1f}'.format(value)))

    @Feat(units='V')
    def output(self):
        """Output voltage reading
        """
        return float(self.query('Q'))

    # From SR510 manual page 19
    # Codes for time constants go like 1: 1ms
    #                                  2: 3ms
    #                                  3:10ms
    #                                  4:30ms
    # and so on. This is the list of valid time constants, except the index
    # starts at 0
    pre_time_constants = [1, 3, 10, 30, 100, 300, 1000, 3000,
                          10000, 30000, 100000]
    # Generated using [[1,3][n%2]*10**int(n/2) for n in range(11)]

    @Feat(units='ms', limits=(min(pre_time_constants),
                             max(pre_time_constants)))
    def pre_time_constant(self):
        """Pre time constant.
        Possible values are {}
        If another value is requested, set to the next higher value
        """.format(','.join(str(t) + 'ms' for t in self.pre_time_constants))
        return self.pre_time_constants[int(self.query('T 1')) - 1]

    @pre_time_constant.setter
    def pre_time_constant(self, value):
        try:
            code = self.pre_time_constants.index(value)
        except ValueError:
            # Value not available, set to the next possible value
            code = (index for index, v in self.pre_time_constants
                 if v > value).__next__()
        self.send('T 1,{:d}\r\n'.format(code + 1))

    # Sensitivity codes go from 1 to 24 and correspond to 10nV,20nV,50nV,100nV
    # and so on
    # Code n corresponds to sensitivities[n-1]
    sensitivities = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
                     10000, 20000, 50000, 100000, 200000, 500000,
                     1000000, 2000000, 5000000, 10000000, 20000000, 50000000,
                     100000000, 200000000, 500000000]
    # Generated using [[10,20,50][n%3]*10**int(n/3) for n in range(24)]

    @Feat(units='nV', limits=(min(sensitivities), max(sensitivities)))
    def sensitivity(self):
        """Sensitivity (gain).
        Possible values are {}
        If another value is requested, set to the next lower value
        """.format(','.join(str(s) + 'nV' for s in self.sensitivities))
        return self.sensitivities[int(self.query('G')) - 1]

    @sensitivity.setter
    def sensitivity(self, value):
        try:
            code = self.sensitivities.index(value)
        except ValueError:
            # Value not available, set to the next lower value
            code = len(self.sensitivities) - (index for index, v
                                              in reversed(self.sensitivities)
                                              if v < value).__next__() - 1
        self.send('G {:d}'.format(code + 1))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='Send debug output to screen',
                        action='store_true')
    args = parser.parse_args()
    from lantz.log import LOGGER, DEBUG
    LOGGER.setLevel(DEBUG)
    import logging
    fh = logging.FileHandler('sr510.log', mode='w')
    formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(DEBUG)
    LOGGER.addHandler(fh)
    if args.debug:
        from lantz.log import log_to_screen
        log_to_screen(DEBUG)
    with SR510('GPIB0::28::INSTR') as lockin:
        print('Sensitivity: {}'.format(lockin.sensitivity))
        print('Phase: {}'.format(lockin.phase))
        print('Frequency: {}'.format(lockin.frequency))
        print('Pre Time Constant: {}'.format(lockin.pre_time_constant))
