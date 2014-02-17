from HP54616B.hp54616b import HP54616B
from hp33120a import HP33120A
from lantz import Q_

osc_resource = 'GPIB0::14::INSTR'
gen_resource = 'GPIB0::8::INSTR'
lvdt_channel = 2

osc = HP54616B(osc_resource)
osc.initialize()

gen = HP33120A(gen_resource)
gen.initialize()
gen.amplitude = Q_(80,'mV')
scan_freq = gen.frequency

osc.trigger_source = 'external'
osc.trigger_level = Q_(1,'V')
osc.trigger_mode = 'normal'
osc.timebase_delay = Q_(0,'s')
osc.timebase_range = 1/scan_freq
