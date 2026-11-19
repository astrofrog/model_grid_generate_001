import os
import glob

import numpy as np

import matplotlib.pyplot as plt

for grid in glob.glob('times/*.times'):

    times = np.loadtxt(grid, usecols=[1])

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.hist(times / 3600., range=[0., 20.], bins=100, log=True)
    fig.savefig(os.path.basename(grid).split('.')[0] + '.png')
    ax.set_xlim(0., 20.)
    ax.set_xlabel('time (hr)')
    ax.set_ylabel('number of models')
    ax.axvline(np.mean(times) / 3600.)
    print(grid, np.sum(times) / 3600., np.mean(times) / 3600.)
    plt.close(fig)
