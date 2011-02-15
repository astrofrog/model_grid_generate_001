import glob
import os
import shutil

from mysg.models import make_set_dir, sample_set_models
from mysg.util import create_dir


def create_condor_files(grid):

    create_dir('%s/condor' % grid)

    shutil.copy('condor/condor_default_script', '%s/condor/condor_script' % grid)

    f = open('%s/condor/dagman.config' % grid, 'wb')
    f.write('DAGMAN_MAX_JOBS_SUBMITTED = 1000\n')
    f.close()

    f = open('%s/condor/move.sh' % grid, 'wb')
    f.write('#!/bin/sh\n/bin/mv $1.rtout output/\n/bin/mv $1.{out,err} log/\n')
    f.close()

    os.chmod('%s/condor/move.sh' % grid, 0744)

    f = open('%s/condor/submit' % grid, 'wb')
    f.write('CONFIG condor/dagman.config\n\n')

    for model in glob.glob(os.path.join('%s/par/' % grid, '*.par')):
        model_name = os.path.basename(model).replace('.par', '')
        f.write('JOB %s condor/condor_script\n' % model_name)
        f.write('VARS %s Args = "%s"\n' % (model_name, model_name))
        f.write('SCRIPT POST %s ./condor/move.sh %s\n\n' % (model_name, model_name))

    f.close()

create_dir('grids')

f = open('grids.txt', 'rb')

for line in f.readlines():

    grid = line.strip()

    make_set_dir(grid, 'ranges.conf')
    sample_set_models(grid, 1)
    create_condor_files('grids/%s' % grid)
