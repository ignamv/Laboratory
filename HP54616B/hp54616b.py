# -*- coding: utf-8 -*-
"""
    HP54616B
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Implements the drivers to control an oscilloscope.

    :copyright: 2013 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.

    Source: Agilent Oscilloscope Programmer's Guide
"""

import numpy as np

from lantz.visa import GPIBVisaDriver
from lantz import Feat, DictFeat, Q_, Action


class HP54616B(GPIBVisaDriver):
    """Hewlett Packard 54616B two-channel digital storage oscilloscope
    """

    ENCODING = 'ascii'
    RECV_TERMINATION = '\n'
    SEND_TERMINATION = '\n'
    RECV_CHUNK = -1

    # Value returned by MEASURE commands when a measurement can't be made
    # (for example, part of the waveform is outside the display)
    error_value = 9.9e37
    channels = range(1, 3)

    @Feat()
    def idn(self):
        """Instrument type and software version

        Return a string with the format
            HEWLETT-PACKARD,<model>, 0, X<NL>
        <model> ::= the model number of the instrument
        X ::= the software revision of the instrument.
        """
        return self.query('*IDN?')

    @Feat()
    def setup(self):
        """Binary string with the current state of the instrument.

        The setup can be saved and later returned to the instrument by setting
        this feat.
        """
        self.send(':SYSTEM:SETUP?')
        return self.read_block()

    @setup.setter
    def setup(self, value):
        self.send(b':SYSTem:SETUP ' + value)

    valid_points = [100, 200, 250, 400, 500, 800, 1000, 2000, 2500, 4000, 5000]
    @Feat(values=dict(zip(valid_points,valid_points)))
    def points(self):
        """Number of waveform points to be transferred on acquisition. Valid
        values are {:s}
        """.format(', '.join(str(k) for k in self.valid_points))
        return int(self.query(':WAVEFORM:POINTS?'))

    @points.setter
    def points(self, value):
        self.send(':WAVEFORM:POINTS {:d}'.format(value))

    @Feat(values={'normal': 'NORM', 'delayed': 'DEL', 'xy': 'XY',
                  'roll': 'ROLL'})
    def timebase_mode(self):
        """Current time base mode.

        Select one of four time base modes:

        NORMAL - The Normal time base mode is the main time base. It is the
        default time base mode after the *RST reset command.

        DELayed - In the Delayed time base mode the range and delay commands
        set the values in the delayed time base instead of the main (Normal)
        time base. No waveform data is available through the interface bus.
        Measurements will be made in the delayed time base if possible,
        otherwise the measurements will be made in the main time base.

        XY - In the XY mode, the RANGe, DELay, REFerence, and VERNier commands
        are not available. No measurement or waveform data are available.

        ROLL - In the ROLL mode, data moves continuously across the display
        from left to right. The oscilloscope runs continuously and is
        untriggered. The time REFerence selection changes from LEFT | CENTer to
        CENTer | RIGHt. No waveform data is available through the interface
        bus.
        """
        return self.query(':TIMEBASE:MODE?')

    @timebase_mode.setter
    def timebase_mode(self, value):
        self.send(':TIMEBASE:MODE ' + value)

    # TODO: raise exception when return value is 9.9e37
    @DictFeat(units='V', keys=channels)
    def average_signal(self, channel):
        self.run()
        self.send(':MEASURE:SOURCE CHANNEL{:d}'.format(channel))
        return float(self.query(':MEASURE:VAVERAGE?'))

    def run(self):
        self.send(':RUN')

    @Feat(units='s')
    def timebase_delay(self):
        """Time base delay.

        This delay is the internal time between the trigger event and the
        onscreen delay reference point. The delay reference point is one
        division from the left edge of the display
        """
        return float(self.query('TIMEBASE:DELAY?'))

    @timebase_delay.setter
    def timebase_delay(self, value):
        self.send(':TIMEBASE:DELAY {:.3f}'.format(value))

    @Feat(units='s', limits=(10e-9, 50))
    def timebase_range(self):
        """Full-scale horizontal time in seconds.

        The horizontal range is 10 x the time per division setting. When the
        delayed time base is selected, the RANGe command will set the
        full-scale horizontal time of the delayed time base.
        """
        return self.query(':TIMEBASE:RANGE?')

    @timebase_range.setter
    def timebase_range(self, value):
        self.send('TIMEBASE:RANGE {:f}'.format(value))

    @Feat(values=dict(channel1='CHANNEL1',
                      channel2='CHANNEL2',
                      external='EXTERNAL',
                      line='LINE'))
    def trigger_source(self):
        return self.query('TRIGGER:SOURCE?')

    @trigger_source.setter
    def trigger_source(self, source):
        self.send('TRIGGER:SOURCE ' + source)

    trigger_modes = ['autlevel', 'auto', 'normal', 'single', 'tv']
    @Feat(values=dict(zip(trigger_modes, trigger_modes)))
    def trigger_mode(self):
        return self.query('TRIGGER:MODE?')

    @Feat(limits=(0,100))
    def complete_percent(self):
        """Minimum percentage of time buckets filled before the acquisition is considered complete"""
        return self.query('ACQUIRE:COMPLETE?')

    @complete_percent.setter
    def complete_percent(self, percentage):
        self.send('ACQUIRE:COMPLETE {}'.format(percentage))

    @trigger_mode.setter
    def trigger_mode(self, mode):
        self.send('TRIGGER:MODE ' + mode)

    @Feat(units='V')
    def trigger_level(self):
        return self.query('TRIGGER:LEVEL?')

    @trigger_level.setter
    def trigger_level(self, level):
        self.send('TRIGGER:LEVEL {}'.format(level))

    def stop(self):
        self.send('STOP')

    def run(self):
        self.send('RUN')

    @DictFeat(units='V', keys=channels, limits=(16e-3, 40))
    def range(self, key):
        """Full-scale vertical scale of the channel
        """
        return self.query(':CHANNEL{:d}:RANGE?'.format(key))

    @range.setter
    def range(self, key, value):
        self.send(':CHANNEL{:d}:RANGE {:f}'.format(key, value))

    @DictFeat(units='V', keys=channels)
    def offset(self, key):
        """Voltage represented at the center of the screen for the channel.

        The range of legal values vary with the value set by the channel range.
        If you set the offset to a value outside of the legal range, the offset
        value is automatically set to the nearest legal value.
        """
        return self.query(':CHANNEL{:d}:OFFSET?'.format(key))

    @offset.setter
    def offset(self, key, value):
        self.send(':CHANNEL{:d}:OFFSET {:f}'.format(key, value))

    @DictFeat(keys=channels, values={True: 'ON', False: 'OFF'})
    def visible(self, key):
        """Channel's visibility on screen
        """
        return self.query(':STATUS? CHANNEL{:d}'.format(key))

    @visible.setter
    def visible(self, key, value):
        if value:
            self.send(':VIEW CHANNEL{:d}'.format(key))
        else:
            self.send(':BLANK CHANNEL{:d}'.format(key))

    @Feat(values={True: 'ON', False: 'OFF'})
    def vectors(self):
        """Enable vectors (connect-the-dots feature).
        """
        return self.query(':DISPLAY:CONNECT?')

    @vectors.setter
    def vectors(self, value):
        self.send(':DISPLAY:CONNECT ' + value)

    def digitize(self, channels):
        if not all(channel in self.channels for channel in channels):
            raise Exception('Invalid channel')
        for channel in channels:
            self.send(':SHOW CHANNEL{:d}'.format(channel))
        self.timebase_mode = 'normal'
        # Disable vectors to acquire more samples
        self.vectors = False
        self.send(':DIGITIZE ' + ','.join('CHANNEL{:d}'.format(channel)
                                            for channel in channels))
    def data(self, channels, existing_data=False):
        """Acquire data from the specified channels.

        Returns [t, v1, ..., vn]
        t is the time in seconds.
        vi is the i-th channel's voltage in volts.
        Each element of the array is a numpy array wrapped with Pint units.
        """
        if not all(channel in self.channels for channel in channels):
            raise Exception('Invalid channel')
        if len(channels) == 0:
            return
        if not existing_data:
            self.digitize(channels)
        ret = []
        for channel in channels:
            self.send(':WAVEFORM:SOURCE CHANNEL{:d}'.format(channel))
            preamble = self.parse_query(':WAVEFORM:PREAMBLE?', format=
                    '{format:+d},{type:+d},{points:+d},{count:+d},'
                    '{xincrement:+E},{xorigin:+E},{xreference:+d},'
                    '{yincrement:+E},{yorigin:+E},{yreference:+d}')
            # <format> ::= 0 for ASCii format, 1 for BYTE format, 2 for WORD
            # format; an integer in NR1 format
            # <type>  ::= 0 for AVERage type, 1 for NORMal type, 2 for PEAK
            # detect type; an integer in NR1 format
            # <count>  ::= 1, always 1 and is present for compatibility; an
            # integer in NR1 format
            self.send(':WAVEFORM:DATA?')
            samples = np.fromstring(
                          self.read_block(),
                          [np.uint16, np.uint8, np.uint16][preamble['format']],
                          -1,
                          [',', '', ''][preamble['format']]
                      ).astype(np.double)
            ret.append(Q_((samples - preamble['yreference'])
                          * preamble['yincrement'] + preamble['yorigin'], 'V'))
        # Trust that all the channels have the same x settings
        ret.insert(0, Q_((np.arange(len(samples)) - preamble['xreference'])
                         * preamble['xincrement'] + preamble['xorigin'], 's'))
        return ret

if __name__ == '__main__':
    import argparse
    from sys import argv
    from os.path import basename
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='Send debug output to screen',
                        action='store_true')
    args = parser.parse_args()
    # Set up logging
    from lantz.log import LOGGER, DEBUG
    LOGGER.setLevel(DEBUG)
    import logging
    fh = logging.FileHandler(basename(argv[0]) + '.log', mode='w')
    formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(DEBUG)
    LOGGER.addHandler(fh)
    if args.debug:
        from lantz.log import log_to_screen
        log_to_screen(DEBUG)
    from matplotlib import pyplot as pl
    with HP54616B('GPIB0::14::INSTR') as osc:
        print('IDN: {}'.format(osc.idn))
        print('Timebase mode: {}'.format(osc.timebase_mode))
        print('Timebase delay: {}'.format(osc.timebase_delay))
        print('Timebase range: {}'.format(osc.timebase_range))
        osc.vectors = False
        print('Vectors: {}'.format(osc.vectors))
        print('Points: {}'.format(osc.points))
        pl.subplots(len(osc.channels), sharex=True)
        for channel in osc.channels:
            print('Channel {:d}'.format(channel))
            print('-Range: {:f}'.format(osc.range[channel]))
            print('-Offset: {:f}'.format(osc.offset[channel]))
            print('-Visible: {}'.format(osc.visible[channel]))
        data = osc.data(osc.channels)
        for channel in osc.channels:
            pl.subplot(len(osc.channels), 1, channel)
            pl.plot(data[0], data[channel])
        pl.show()
