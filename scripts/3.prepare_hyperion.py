from __future__ import unicode_literals, division, print_function

import os
import glob
import sys
from multiprocessing import Pool

import numpy as np
np.seterr(all='ignore')

from mysg.hyperion import setup_model
from mysg.models import export_dust_files

export_dust_files('.')

for grids in glob.glob(os.path.join('grids/', '*')):
    if not os.path.exists('%s/d03_5.5_3.0_A.hdf5' % grids):
        os.symlink('../../d03_5.5_3.0_A.hdf5', '%s/d03_5.5_3.0_A.hdf5' % grids)

def setup_model_wrapper(parfile):
    sys.stdout = open(parfile.replace('.par', '_setup.log').replace('/par/', '/log/'), 'wb')
    try:
        setup_model(parfile, parfile.replace('.par', '').replace('/par/', '/input/'))
        sys.stdout = sys.__stdout__
        return True
    except:
        sys.stdout = sys.__stdout__
        return False

# Create a process pool
p = Pool(processes=16)

# Find all parfiles to process
parfiles = glob.glob(os.path.join('grids/*/par/', '*.par'))

# Create all Hyperion input files
results = p.map(setup_model_wrapper, parfiles)

for ip in range(len(parfiles)):
    if not results[ip]:
        print("%s failed" % parfiles[ip])
