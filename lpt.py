from lantz.visa import SerialVisaDriver
from time import sleep

class ParallelPort(SerialVisaDriver):
    def __init__(self, resource_name):
        super().__init__(resource_name)

if __name__ == '__main__':
    lpt = ParallelPort('ASRL10::INSTR')
    lpt.initialize()
    print('Sending 0')
    lpt.raw_send('\x00')
    time.sleep(2)
    print('Sending 1')
    lpt.raw_send('\xff')
    time.sleep(2)
    print('Sending 0')
    lpt.raw_send('\x00')
    time.sleep(2)
    print('Sending 1')
    lpt.raw_send('\xff')
