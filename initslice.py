import sys
if '-mpi' in sys.argv:
    from mpi4py import MPI

from olfactorybulb.model import OlfactoryBulb as OB

if '-paramset' in sys.argv:
    paramset = sys.argv[sys.argv.index("-paramset")+1]
    ob = OB(paramset)

else:
    ob = OB()
