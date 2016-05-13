import os
import sys
import glob
import h5py
import numpy as np
from multiprocessing import Pool

if len(sys.argv) != 2:
    print "Usage: python {0} directory".format(sys.argv[0])
    sys.exit(0)
else:
    directory = sys.argv[1]

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

for grid in glob.glob(os.path.join(directory, 's??????-----')):

    print("Listing models for {:s}".format(grid))

    # List models
    models = []
    for gridlet in glob.glob(os.path.join(grid, 'output', '??')):
        models += glob.glob(os.path.join(gridlet, '*_sed.rtout'))

    if len(models) == 0:
        continue

    print("Finding times for {:s}".format(grid))

    times = p.map(find_time, models)

    f = open(grid.replace(directory, 'times/') + '.times', 'w')
    for i in range(len(models)):
        f.write("{:s} {:.3f}\n".format(models[i], times[i]))
    f.close()
    
