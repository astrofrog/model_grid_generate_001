from __future__ import unicode_literals, division, print_function

import glob
import os
import shutil
from datetime import datetime

import mysg
import hyperion

from mysg.models import make_set_dir, sample_set_models
from mysg.util import create_dir

VERSION = "1.0.0"


def create_condor_files(directory, set_name):

    create_dir('%s/%s/condor' % (directory, set_name))

    shutil.copy('condor/condor_default_script', '%s/%s/condor/condor_script' % (directory, set_name))

    f = open('%s/%s/condor/dagman.config' % (directory, set_name), 'w')
    f.write('DAGMAN_MAX_JOBS_SUBMITTED = 1000\n')
    f.write('DAGMAN_MAX_JOBS_IDLE = 5000\n')
    f.write('DAGMAN_MAX_SUBMIT_ATTEMPTS = 2\n')
    f.write('DAGMAN_SUBMIT_DELAY = 1\n')
    f.write('DAGMAN_RETRY_SUBMIT_FIRST = False\n')
    f.close()

    f = open('%s/%s/condor/move.sh' % (directory, set_name), 'w')
    f.write('#!/bin/sh\n/bin/mv $1.rtout output/\n/bin/mv $1.{out,err} log/\n')
    f.close()

    os.chmod('%s/%s/condor/move.sh' % (directory, set_name), 0o744)

    f = open('%s/%s/condor/submit' % (directory, set_name), 'w')
    f.write('CONFIG condor/dagman.config\n\n')

    for model in glob.glob(os.path.join('%s/%s/par/' % (directory, set_name), '*/*.par')):
        model_name = os.path.basename(model).replace('.par', '')
        f.write('JOB %s condor/condor_script\n' % model_name)
        f.write('VARS %s Args = "%s"\n' % (model_name, model_name))
        f.write('SCRIPT POST %s ./condor/move.sh %s\n\n' % (model_name, model_name))

    f.close()


def create_odyssey_files(directory, set_name):

    create_dir('%s/%s/odyssey' % (directory, set_name))
    create_dir('%s/%s/odyssey/pbs' % (directory, set_name))

    template = open('odyssey/template.pbs', 'r').read()

    fsubmit = open('%s/%s/odyssey/submit.sh' % (directory, set_name), 'w')
    fsubmit.write("#!/bin/bash\n\n")

    for model in glob.glob(os.path.join('%s/%s/par/' % (directory, set_name), '*/*.par')):

        model_name = os.path.basename(model).replace('.par', '')

        fpbs = open('%s/%s/odyssey/pbs/%s.pbs' % (directory, set_name, model_name), 'w')
        fpbs.write(template.replace('MODEL_NAME', model_name).replace('SET_NAME', set_name))
        fpbs.close()

        fsubmit.write('bsub < %s/%s/odyssey/pbs/%s.pbs\n' % (directory, set_name, model_name))

    fsubmit.close()


def create_anthill_files(directory, set_name):

    create_dir('%s/%s/anthill' % (directory, set_name))
    create_dir('%s/%s/anthill/qsub' % (directory, set_name))

    template = open('anthill/template.qsub', 'r').read()

    fsubmit = open('%s/%s/anthill/submit.sh' % (directory, set_name), 'w')
    fsubmit.write("#!/bin/bash\n\n")

    for model in glob.glob(os.path.join('%s/%s/par/' % (directory, set_name), '*/*.par')):

        model_name = os.path.basename(model).replace('.par', '')
        short_name = model_name[:2].lower()

        qsub_dir = '%s/%s/anthill/qsub/%s' % (directory, set_name, short_name)
        if not os.path.exists(qsub_dir):
            os.mkdir(qsub_dir)

        log_dir = '%s/%s/log/%s' % (directory, set_name, short_name)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        fqsub = open('%s/%s/anthill/qsub/%s/%s.qsub' % (directory, set_name, short_name, model_name), 'w')
        fqsub.write(template.replace('MODEL_NAME', short_name + '/' + model_name).replace('SET_NAME', set_name).replace('GRIDS_NAME', directory))
        fqsub.close()

        fsubmit.write('qsub < %s/%s/anthill/qsub/%s/%s.qsub\n' % (directory, set_name, short_name, model_name))

    fsubmit.close()


grids_dir = 'grids-' + VERSION

create_dir(grids_dir)

# Write out meta-data
f = open(os.path.join(grids_dir, 'INFO'), 'wb')
f.write("date = {0}\n".format(datetime.now().isoformat()))
f.write("grid_version = {0}\n".format(VERSION))
f.write("hyperion_version = {0}\n".format(hyperion.__version__))
f.write("mysg_version = {0}\n".format(mysg.__version__))
f.close()

for line in open('grids.txt', 'r'):

    grid = line.strip()

    make_set_dir(grids_dir, grid)

    # Number of models for test run (including 0.1 version)
    # sample_set_models(grids_dir, grid, lambda x: 50 * 2 ** (max(0, x - 9)))

    # Number of models for full run:
    sample_set_models(grids_dir, grid, lambda x: 10000 * 2 ** (max(0, x - 9)))

    # create_condor_files(grids_dir, grid)
    # create_odyssey_files(grids_dir, grid)
    create_anthill_files(grids_dir, grid)
