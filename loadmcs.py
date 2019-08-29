import sys; 
sys.path.append('/home/justas/Repositories/BlenderNEURON/'); 
from prev_ob_models.Birgiolas2020.isolated_cells import *; 

mc1 = MC1();
mc2 = MC2();
mc3 = MC3();
mc4 = MC4();
mc5 = MC5();

gc1 = GC1()
gc2 = GC2()
gc3 = GC3()
gc4 = GC4()
gc5 = GC5()

tc1 = TC1()
tc2 = TC2()
tc3 = TC3()
tc4 = TC4()
tc5 = TC5()
#del mc1

from blenderneuron import neuronstart;
from neuron import h,gui
