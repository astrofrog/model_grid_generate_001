import os
import glob
import sys
from multiprocessing import Pool

import numpy as np
np.seterr(all='ignore')

from mysg.hyperion import setup_model
from mysg.models import export_dust_files

export_dust_files()

def setup_model_wrapper(parfile):
    sys.stdout = open(parfile.replace('.par', '_setup.log').replace('/par/', '/log/'), 'wb')
    return setup_model(parfile, parfile.replace('.par', '').replace('/par/', '/input/'))
    sys.stdout = sys.__stdout__

# Create a process pool
p = Pool(processes=16)

# Find all parfiles to process
parfiles = glob.glob(os.path.join('grids/*/par/', '*.par'))

# Create all Hyperion input files
p.map(setup_model_wrapper, parfiles)
