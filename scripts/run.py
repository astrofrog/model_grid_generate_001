import glob
import os

for model in glob.glob(os.path.join('grids/*/input/', '*.rtin')):
    os.system('mpirun -n 8 hyperion_sph_mpi %s %s' % (model, model.replace('rtin', 'rtout').replace('input', 'output')))
