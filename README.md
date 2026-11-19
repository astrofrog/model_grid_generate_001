# A modular set of synthetic spectral energy distributions for young stellar objects

## Info

These are the scripts used to set up the model grid published in
[Robitaille (2017)](https://doi.org/10.1051/0004-6361/201425486).

Version 1.1 of the model grid was published on Zenodo, with the SEDs at

https://doi.org/10.5281/zenodo.166732

and the Hyperion files at

https://doi.org/10.5281/zenodo.572233

## Using

The scripts in this directory require the
[mysg](https://github.com/astrofrog/mysg) package which is common to all grids
in this project. The package is not on PyPI and should be installed with e.g.:

    pip install git+https://github.com/astrofrog/mysg.git

The published v1.1 grid was computed with mysg 1.1. The dust file included in
that version had an albedo and scattering matrix that had been computed with
a version of the Mie code that had a bug (the extinction is within 1% of the
correct one), and this has been fixed in later versions of mysg, which get
the dust properties from the
[hyperion-dust](https://github.com/hyperion-rt/hyperion-dust) package. The
command above therefore installs a version of mysg with the corrected dust,
which will not give the same SEDs as the published grid. To install the
version of mysg used for the published grid instead, which only works with
Python 2, use:

    pip install git+https://github.com/astrofrog/mysg.git@v1.1.0

To set up the grids:

    python scripts/1.list_grids.py
    python scripts/2.setup_grids.py

This writes one job script per model, and the jobs are then submitted with
e.g. `submit_all.sh`. Each job runs `scripts/3.prepare_hyperion_indiv.py` to
write the Hyperion input file for the model, then runs Hyperion to compute
the temperatures.

The SEDs are computed in a second step, once the first one has completed:

    python scripts/2.setup_grids_sed.py

This again writes one job script per model. Each job runs
`scripts/3.prepare_hyperion_indiv_sed.py`, which reads the output of the first
step, removes the sublimated dust and sets the apertures, then runs Hyperion
to compute the SEDs.

For models in which the SED step takes too long to run, the SEDs can be
computed without scattering instead, using:

    python scripts/2.setup_grids_sed_noscat.py

and the jobs written by this run
`scripts/3.prepare_hyperion_indiv_sed_noscat.py`.

The list of model sets that were run for the published grid is given in
`grids_all.txt`.
