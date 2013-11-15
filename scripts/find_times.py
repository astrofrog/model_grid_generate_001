import os
import glob
import h5py
import numpy as np
from multiprocessing import Pool

def find_time(filename):
    try:
        frt = h5py.File(filename, 'r')
        cpu_time = frt.attrs['cpu_time']
        frt.close()
    except:
        return 0.
    else:
        return cpu_time

p = Pool()

for grid in glob.glob('grids/s??????-----'):

    print("Listing models for {:s}".format(grid))

    # List models
    models = []
    for gridlet in glob.glob(os.path.join(grid, 'output', '??')):
        models += glob.glob(os.path.join(gridlet, '*.rtout'))

    if len(models) == 0:
        continue

    print("Finding times for {:s}".format(grid))

    times = p.map(find_time, models)

    f = open(grid.replace('grids', 'times') + '.times', 'w')
    for i in range(len(models)):
        f.write("{:s} {:.3f}\n".format(models[i], times[i]))
    f.close()
    
