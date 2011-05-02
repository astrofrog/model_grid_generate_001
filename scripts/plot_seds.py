import glob
import os

import matplotlib
matplotlib.use('Agg')

from hyperion.model import Model

for filename in glob.glob(os.path.join('grids/*/output/*.rtout')):
    print filename,
    try:
        m = Model(filename.replace('.rtout', ''))
        m.plot_sed(filename='plots/' + os.path.basename(filename.replace('.rtout', '')))
        print ""
    except:
        print "failed"