import numpy as np
np.seterr(all='ignore')
import os
import glob
from mysg.hyperion import setup_model

for parfile in glob.glob(os.path.join('grids/*/par/', '*.par')):
    print parfile
    setup_model(parfile, parfile.replace('.par', '').replace('/par/','/input/'))
