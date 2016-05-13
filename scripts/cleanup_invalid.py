import os
import sys
import glob
import h5py
import numpy as np

from astropy.utils.console import ProgressBar
from astropy.table import Table

if len(sys.argv) != 3:
    print "Usage: python {0} grid_directory trash_directory".format(sys.argv[0])
    sys.exit(0)
else:
    directory = sys.argv[1]
    trash = sys.argv[2]

if not os.path.exists(trash):
    os.mkdir(trash)

t = Table.read('account_summary.fits')

times = t['ru_wallclock'].astype(float)

rerun = t[times < 100]

print(times)
print(np.sum(times < 100))
print(np.sum(times < 1000))
print(len(times))

rerun_jobs = [name[1:] for name in rerun['jobname']]

print(rerun_jobs)

for grid in glob.glob(os.path.join(directory, 's??????-----')):

    # Make trash sub-folder
    grid_trash = os.path.join(trash, os.path.basename(grid))
    if not os.path.exists(grid_trash):
        os.mkdir(grid_trash)

    for output_set in ProgressBar(glob.glob(os.path.join(grid, 'log', '??'))):
        for out_file in glob.glob(os.path.join(output_set, '*.out')):
            name = os.path.basename(out_file).replace('.out', '')
            if name in rerun_jobs:
                qsub_file = out_file.replace('log', 'anthill/qsub').replace('.out', '.qsub')
                output_file = out_file.replace('log', 'output').replace('.out', '.rtout')
                err_file = out_file.replace('.out', '.err')
                input_file = out_file.replace('log', 'input').replace('.out', '.rtin')
                for filename in (input_file, output_file, out_file, err_file, qsub_file):
                    try:
                        os.rename(filename, os.path.join(grid_trash, os.path.basename(filename)))
                    except OSError:
                        pass

                
                

            
