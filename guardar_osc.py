from HP54616B import HP54616B

oscilloscope_resource = 'GPIB0::14::INSTR'
osc = HP54616B(oscilloscope_resource)
osc.initialize()

print(
print(osc.data([2]))
