import glob
import os

for model in glob.glob(os.path.join('models/*/input/', '*.rtin')):
    print model
    os.system('mpirun -n 8 hyperion_sph_mpi %s %s' % (model, model.replace('rtin', 'rtout').replace('input', 'output')))
    break
