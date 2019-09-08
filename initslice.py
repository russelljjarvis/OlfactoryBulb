import sys
if '-mpi' in sys.argv:
    from mpi4py import MPI

from olfactorybulb.model import OlfactoryBulb as OB

ob = OB('TestSlice')

ob.h.quit()