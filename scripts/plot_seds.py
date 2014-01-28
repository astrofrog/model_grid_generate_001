from __future__ import unicode_literals, division, print_function

import glob
import os
import numpy as np

import matplotlib
matplotlib.use('Agg')

from hyperion.model import ModelOutput
from hyperion.util.constants import au
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12,16))

NX = 5
NY = 10

for grid in glob.glob(os.path.join('grids-0.1.4-test','s*-')):

    grid_name = os.path.basename(grid)
    print(grid_name)
    c = 0
    page = 1
    for model in glob.glob(os.path.join(grid, 'output', '*', '*.rtout')):
        print(model)
        try:
            m = ModelOutput(model)
            sed = m.get_sed(distance=300*au, aperture=-1)
        except:
            continue
        c += 1
        if c > NX * NY:
            print("HERE", c, page)
            fig.savefig('{grid_name}_page{page:03d}.pdf'.format(grid_name=grid_name, page=page))
            fig.clf()
            page += 1
            c = 1

        ax = fig.add_subplot(NY, NX, c)

        for incl in range(sed.val.shape[0]):
            x = incl / 16.
            ax.loglog(sed.wav, sed.val[incl,:], color=(x, 0., 1-x))

        ax.set_ylim(np.max(sed.val) / 1e6, np.max(sed.val) * 4.)
        ax.set_xticklabels('')
        ax.set_yticklabels('')
        ax.set_title(os.path.basename(model).replace('.rtout', ''), size=5)

    fig.savefig('{grid_name}_page{page:03d}.pdf'.format(grid_name=grid_name, page=page))
    fig.clf()

