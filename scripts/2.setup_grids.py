import glob
import os
from datetime import datetime

import mysg
import hyperion

from mysg.models import make_set_dir, sample_set_models
from mysg.util import create_dir

VERSION = "1.1"
UPDATE = False


def create_anthill_files(directory, set_name):

    if not os.path.exists('%s/%s/anthill' % (directory, set_name)):
        os.mkdir('%s/%s/anthill' % (directory, set_name))

    if not os.path.exists('%s/%s/anthill/qsub' % (directory, set_name)):
        os.mkdir('%s/%s/anthill/qsub' % (directory, set_name))

    with open('anthill/template.qsub') as f:
        template = f.read()

    with open('%s/%s/anthill/submit.sh' % (directory, set_name), 'w') as fsubmit:

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

            output_name = "%s/%s/output/%s/%s.rtout" % (directory, set_name, short_name, model_name)
            qsub_name = '%s/%s/anthill/qsub/%s/%s.qsub' % (directory, set_name, short_name, model_name)

            if not os.path.exists(output_name):

                with open(qsub_name, 'w') as fqsub:
                    fqsub.write(template.replace('MODEL_NAME', model_name).replace('SET_NAME', set_name).replace('GRIDS_NAME', directory).replace('SHORT_NAME', short_name))

                fsubmit.write('qsub < %s/%s/anthill/qsub/%s/%s.qsub\n' % (directory, set_name, short_name, model_name))


grids_dir = 'grids-' + VERSION

if not UPDATE:
    create_dir(grids_dir)

# Write out meta-data
info_name = os.path.join(grids_dir, 'INFO')
if os.path.exists(info_name):
    suffix = 1
    while os.path.exists(info_name + '.' + str(suffix)):
        suffix += 1
    info_name = info_name + '.' + str(suffix)

with open(info_name, 'w') as f:
    f.write("date = {0}\n".format(datetime.now().isoformat()))
    f.write("grid_version = {0}\n".format(VERSION))
    f.write("hyperion_version = {0}\n".format(hyperion.__version__))
    f.write("mysg_version = {0}\n".format(mysg.__version__))

with open('grids.txt') as f:
    grids = [line.strip() for line in f]

for grid in grids:

    if not UPDATE:
        make_set_dir(grids_dir, grid)

    # Number of models for test run (including 0.1 version)
    # sample_set_models(grids_dir, grid, lambda x: 50 * 2 ** (max(0, x - 9)))

    # Number of models for full run:
    if not UPDATE:
        sample_set_models(grids_dir, grid, lambda x: 10000 * 2 ** (max(0, x - 9)))

    create_anthill_files(grids_dir, grid)
