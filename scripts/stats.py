import os
import sys
import glob
import h5py
import numpy as np
from multiprocessing import Pool
from astropy.table import Table

if len(sys.argv) != 2:
    print("Usage: python {0} directory".format(sys.argv[0]))
    sys.exit(0)
else:
    directory = sys.argv[1]

def find_time(filename):
    try:
        frt = h5py.File(filename, 'r')
        cpu_time = frt.attrs['cpu_time']
        frt['Peeled']['group_00001']['seds']
        frt.close()
    except Exception:
        return -1.
    else:
        return cpu_time

p = Pool()

grids = []
total = []
success = []
total_time = []

for grid in glob.glob(os.path.join(directory, 's??????-----')):

    print("Listing models for {:s}".format(grid))

    # List models
    models = []
    for gridlet in glob.glob(os.path.join(grid, 'output', '??')):
        models += glob.glob(os.path.join(gridlet, '*.rtout'))

    models = [model for model in models if '_sed' not in model]

    if len(models) == 0:
        continue

    print("Finding times for {:s}".format(grid))

    times = p.map(find_time, models)

    times = np.array(times)

    grids.append(os.path.basename(grid))
    total.append(len(times))
    success.append(int(np.sum(times > 0.)))
    total_time.append(np.sum(times) / 3600.)

t = Table()
t['grids'] = grids
t['total'] = total
t['success'] = success
t['success_rate'] = np.array(success, dtype=float) / total * 100.
t['success_rate'].format = "%6.2f"
t['total_time'] = total_time
t['total_time'].format = "%.2f"
print(t)
