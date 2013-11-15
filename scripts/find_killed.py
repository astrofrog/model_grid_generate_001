import os
import glob
import h5py
import numpy as np
from multiprocessing import Pool

def find_killed(filename):

    ktot = 0

    try:
        frt = h5py.File(filename, 'r')
    except:
        return -1

    for iter in range(1, 11):
        try:
            k1 = frt['iteration_{0:05d}'.format(iter)].attrs['killed_photons_geo']
            k2 = frt['iteration_{0:05d}'.format(iter)].attrs['killed_photons_int']
        except:
            break
        else:
            ktot = k1 + k2

    return ktot

p = Pool()

for grid in glob.glob('grids/s??????-----'):

    print("Listing models for {:s}".format(grid))

    # List models
    models = []
    for gridlet in glob.glob(os.path.join(grid, 'output', '??')):
        models += glob.glob(os.path.join(gridlet, '*.rtout'))

    if len(models) == 0:
        continue

    print("Finding number of killed photons for {:s}".format(grid))

    killed = p.map(find_killed, models)

    f = open(grid.replace('grids', 'killed') + '.killed', 'w')
    for i in range(len(models)):
        f.write("{:s} {:d}\n".format(models[i], killed[i]))
    f.close()
    
