import glob
import os
import shutil

from mysg.models import make_set_dir, sample_set_models
from mysg.util import create_dir


def create_condor_files(directory, set_name):

    create_dir('%s/%s/condor' % (directory, set_name))

    shutil.copy('condor/condor_default_script', '%s/%s/condor/condor_script' % (directory, set_name))

    f = open('%s/%s/condor/dagman.config' % (directory, set_name), 'wb')
    f.write('DAGMAN_MAX_JOBS_SUBMITTED = 1000\n')
    f.close()

    f = open('%s/%s/condor/move.sh' % (directory, set_name), 'wb')
    f.write('#!/bin/sh\n/bin/mv $1.rtout output/\n/bin/mv $1.{out,err} log/\n')
    f.close()

    os.chmod('%s/%s/condor/move.sh' % (directory, set_name), 0744)

    f = open('%s/%s/condor/submit' % (directory, set_name), 'wb')
    f.write('CONFIG condor/dagman.config\n\n')

    for model in glob.glob(os.path.join('%s/%s/par/' % (directory, set_name), '*.par')):
        model_name = os.path.basename(model).replace('.par', '')
        f.write('JOB %s condor/condor_script\n' % model_name)
        f.write('VARS %s Args = "%s"\n' % (model_name, model_name))
        f.write('SCRIPT POST %s ./condor/move.sh %s\n\n' % (model_name, model_name))

    f.close()

create_dir('grids')

f = open('grids.txt', 'rb')

for line in f.readlines():

    grid = line.strip()

    make_set_dir('grids', grid)
    sample_set_models('grids', grid, lambda x: 10 * 2**(max(0, x-9)))
    create_condor_files('grids', grid)
