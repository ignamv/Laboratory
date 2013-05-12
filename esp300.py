# -*- coding: utf-8 -*-
"""
    ESP300
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Implements the drivers to control a motor controller

    :copyright: 2013 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.

    Source: ESP300 Motion Controller User's Manual
"""

from lantz import Feat, DictFeat, Action
from lantz.visa import GPIBVisaDriver


class ESP300(GPIBVisaDriver):
    """ESP300 Motion Controller/Driver
    """

    ENCODING = 'ascii'
    RECV_TERMINATION = '\r\n'
    SEND_TERMINATION = '\n'
    RECV_CHUNK = -1

    axes = range(1, 4)

    def initialize(self):
        super().initialize()
        # Set all axes to micrometers
        for axis in self.axes:
            self.send('{:d}SN3'.format(axis))

    @Action()
    def stop(self):
        """Stop all axes
        """
        self.send('ST')

    @DictFeat(keys=axes)
    def ID(self, axis):
        """Positioner model and serial number
        """
        return self.query('{:d}ID?'.format(axis))

    @DictFeat(units='um', keys=axes)
    def position(self, axis):
        """Actual position
        """
        return float(self.query('{:d}TP'.format(axis)))

    @DictFeat(units='um', keys=axes)
    def target_position(self, axis):
        """Desired position
        """
        return float(self.query('{:d}DP?'.format(axis)))

    @target_position.setter
    def target_position(self, axis, position):
        self.send('{:d}PA{:f}'.format(axis, position))

    @DictFeat(units='um/s', keys=axes)
    def velocity(self, axis):
        """Actual velocity
        """
        return float(self.query('{:d}TV'.format(axis)))

    @DictFeat(units='um/s', keys=axes)
    def target_velocity(self, axis):
        """Desired velocity
        """
        return float(self.query('{:d}VA?'.format(axis)))

    @target_velocity.setter
    def target_velocity(self, axis, velocity):
        self.send('{:d}VA{:f}'.format(axis, velocity))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='Send debug output to screen',
                        action='store_true')
    args = parser.parse_args()
    from lantz.log import LOGGER, DEBUG
    LOGGER.setLevel(DEBUG)
    import logging
    fh = logging.FileHandler('esp300.log', mode='w')
    formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    fh.setLevel(DEBUG)
    LOGGER.addHandler(fh)
    if args.debug:
        from lantz.log import log_to_screen
        log_to_screen(DEBUG)
    from lantz import Q_
    from time import sleep
    with ESP300('GPIB0::3::INSTR') as inst:
        for axis in inst.axes:
            print('Axis {:d}'.format(axis))
            print('ID: ' + inst.ID[axis])
            print('Position: {:f}'.format(inst.position[axis]))
            print('Target Position: {:f}'.format(inst.target_position[axis]))
            print('Velocity: {:f}'.format(inst.velocity[axis]))
        print('Position: {:f}'.format(inst.position[1]))
        print('Moving 1um')
        inst.target_position[1] = inst.position[1] + Q_(1, 'um')
        sleep(1)
        print('Stopping')
        inst.stop()
        print('Position: {:f}'.format(inst.position[1]))
