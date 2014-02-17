#--encoding: utf-8 --
from PyQt4.QtCore import pyqtSignal, QThread
from esp300 import ESP300
from sr510 import SR510

def Autocorrelator(QThread):
    sweep_done = pyqtSignal()
    step_done = pyqtSignal()
    def __init__(self, lockin_resource, motion_control_resource, axis = 1,
                 displacement = Q_(80,'nm'), integration_time = Q_(1,'ms')):
        """Create a controller for the autocorrelator

        lockin_resource: GPIB resource name for the lock-in amplifier
        motion_control_resource: GPIB resource name for the motion controller
        axis: number of the axis which moves the corner cube
        displacement: distance to move the corner cube in each step
        integration_time: delay between moving and taking the lock-in reading
        """
        self.lockin = SR510(lockin_resource)
        self.lockin.initialize()
        self.integration_time = integration_time
        self.motionc = ESP300(motion_control_resource)
        self.motionc.initialize()
        self.axis = axis
        self.state = ACStates.idle

    ACStates = Enum('idle',
                    'homing',
                    'stepping',
                    'integrating')

    def run(self):
        self.state = ACStates.homing
        self.home()
        self.motionc.wait_motion_done()
        for step in range(self.nsteps):
            self.state = ACStates.stepping
            self.motionc.target_position[self.axis] = self.displacement + \
                self.motionc.position[self.axis]
            # Don't bother polling the motion controller until it's reached 
            # the destination
            self.msleep(self.displacement/self.motionc.target_velocity[self.axis]
            

    def start_sweep(self):
        """Start a sweep in a new thread"""
        self.sweep_thread = SweepThread(self)


    def pause_sweep(self):

    def stop_sweep(self):

