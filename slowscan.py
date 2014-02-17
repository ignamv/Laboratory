from HP54616B.hp54616b import HP54616B
from hp33120a import HP33120A
from lantz import Q_

osc_resource = 'GPIB0::14::INSTR'
gen_resource = 'GPIB0::8::INSTR'
lvdt_channel = 2
lvdt_range = [Q_(-225,'mV'),Q_(158,'mV')]

osc = HP54616B(osc_resource)
osc.initialize()

gen = HP33120A(gen_resource)
gen.initialize()
gen.amplitude = Q_(0,'V')
scan_freq = gen.frequency

osc.trigger_source = 'channel{}'.format(lvdt_channel)
osc.trigger_level = lvdt_range[1]
osc.trigger_mode = 'single'
osc.timebase_delay = Q_(5,'s')
osc.timebase_range = 1/scan_freq
