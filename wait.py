from esp300 import ESP300

with ESP300('GPIB0::3::INSTR') as inst:
    print(inst.wait())

