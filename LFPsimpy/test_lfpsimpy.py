from LFPsimpy import LfpElectrode as LE
from neuron import h,gui

# soma = h.Section(name='soma')
# soma.insert('pas')
# soma.insert('hh')
#
# ic = h.IClamp(0.5, sec=soma)
# ic.delay = 2
# ic.dur = 0.1
# ic.amp = 0.1

h.newPlotV()


from LFPsimpy import LfpElectrode as LE
le = LE(-100,50,0)
from matplotlib import pyplot as plt
plt.plot(le.times,le.values); plt.show()