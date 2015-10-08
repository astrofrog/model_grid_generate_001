import os
import sys
import glob

import numpy as np
from astropy.table import Table
from hyperion.model import Model, ModelOutput
from hyperion.util.constants import au


def quantity_table(model_out):

    m = ModelOutput(model_out)
    g = m.get_quantities()

    t = Table()

    # Radius

    t['radius'] = g.r_wall[1:]  # radius at the outer wall of each cell

    # Density

    density = g['density'][0].array[0]

    t['density_min'] = np.min(density, axis=0)
    t['density_mean'] = np.mean(density, axis=0)
    t['density_max'] = np.max(density, axis=0)

    # Temperature

    temperature = g['temperature'][0].array[0]

    t['temperature_min'] = np.nanmin(temperature, axis=0)
    t['temperature_mean'] = np.mean(temperature, axis=0)
    t['temperature_max'] = np.nanmax(temperature, axis=0)

    return t


def setup_sed(model_out):

    # Read in model, and derive table of radial temperatures/densities
    m = Model.read(model_out, only_initial=False)
    t = quantity_table(model_out)

    # Find radius at which all temperatures are below 11K and all densities are
    # below 1.1e-23, which we will treat as the background.

    temp = np.nonzero(t['temperature_max'] > 11.)[0]
    dens = np.nonzero(t['density_max'] > 1.1e-23)[0]

    if len(temp) > 0:
        imax_temp = temp[-1]
    else:
        imax_temp = 0

    if len(dens) > 0:
        imax_dens = dens[-1]
    else:
        imax_dens = 0

    largest_radius = t['radius'][max(imax_temp, imax_dens)]

    # We now re-set the image parameters

    n_ap = m.peeled_output[0].n_ap
    ap_min = m.peeled_output[0].ap_min
    ap_max = m.peeled_output[0].ap_max

    m.peeled_output[0].set_depth(-largest_radius, largest_radius)
    m.peeled_output[0].set_aperture_range(20, ap_min, largest_radius)

    # We disable temperature iterations and re-set the number of photons
    m.set_n_initial_iterations(0)
    m.n_photons.clear()
    m.set_n_photons(imaging=1e6, raytracing_sources=10000, raytracing_dust=1e6)

    # When we read in the model above, the link to the dust file is lost, so we
    # replace the dust object by the filename to avoid making the size of
    # input/output files too large.
    m.dust = ['d03_5.5_3.0_A_sub.hdf5']

    m.write(model_out.replace('output', 'input').replace('.rtout', '_sed.rtin'), overwrite=True, copy=False)


model_out = sys.argv[1]
if not os.path.exists(model_out):
    raise IOError("File does not exist: " + model_out)

setup_sed(model_out)