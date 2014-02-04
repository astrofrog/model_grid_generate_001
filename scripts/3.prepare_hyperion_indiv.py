from __future__ import unicode_literals, division, print_function

import os
import glob
import sys
from multiprocessing import Pool

import numpy as np
np.seterr(all='ignore')

from mysg.hyperion_helper import setup_model
from mysg.models import export_dust_files

if not os.path.exists('d03_5.5_3.0_A_sub.hdf5'):
    export_dust_files('.')

def setup_model_wrapper(parfile):
    setup_model(parfile, parfile.replace('.par', '').replace('/par/', '/input/'))

par_file = sys.argv[1]
if not os.path.exists(par_file):
    raise IOError("File does not exist: " + par_file)

setup_model_wrapper(par_file)
