from __future__ import unicode_literals, division, print_function

import glob
import os
import shutil
from datetime import datetime

import mysg
import hyperion

from mysg.models import make_set_dir, sample_set_models
from mysg.util import create_dir

VERSION = "1.0.1"


def create_anthill_files_sed(directory, set_name):

    if not os.path.exists('%s/%s/anthill' % (directory, set_name)):
        os.mkdir('%s/%s/anthill' % (directory, set_name))

    if not os.path.exists('%s/%s/anthill/qsub' % (directory, set_name)):
        os.mkdir('%s/%s/anthill/qsub' % (directory, set_name))

    template = open('anthill/template_sed.qsub', 'r').read()

    fsubmit = open('%s/%s/anthill/submit_sed.sh' % (directory, set_name), 'w')
    fsubmit.write("#!/bin/bash\n\n")

    for model in glob.glob(os.path.join('%s/%s/output/' % (directory, set_name), '*/????????.rtout')):

        model_name = os.path.basename(model).replace('.rtout', '')
        short_name = model_name[:2].lower()

        qsub_dir = '%s/%s/anthill/qsub/%s' % (directory, set_name, short_name)
        if not os.path.exists(qsub_dir):
            os.mkdir(qsub_dir)

        log_dir = '%s/%s/log/%s' % (directory, set_name, short_name)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        output_name = "%s/%s/output/%s/%s_sed.rtout" % (directory, set_name, short_name, model_name)
        qsub_name = '%s/%s/anthill/qsub/%s/%s_sed.qsub' % (directory, set_name, short_name, model_name)

        # We should only run this if neither the output_file nor the version
        # WITHOUT scattering exists:

        if not os.path.exists(output_name) and not os.path.exists(output_name.replace('sed.rtout', 'sed_noscat.rtout')):

            fqsub = open(qsub_name, 'w')
            fqsub.write(template.replace('MODEL_NAME', model_name).replace('SET_NAME', set_name).replace('GRIDS_NAME', directory).replace('SHORT_NAME', short_name))
            fqsub.close()

            fsubmit.write('qsub < %s/%s/anthill/qsub/%s/%s_sed.qsub\n' % (directory, set_name, short_name, model_name))

    fsubmit.close()


grids_dir = 'grids-' + VERSION

# Write out meta-data
info_name = os.path.join(grids_dir, 'INFO_SED')
if os.path.exists(info_name):
    suffix = 1
    while os.path.exists(info_name + '.' + str(suffix)):
        suffix += 1
    info_name = info_name + '.' + str(suffix)

f = open(info_name, 'wb')
f.write("date = {0}\n".format(datetime.now().isoformat()))
f.write("grid_version = {0}\n".format(VERSION))
f.write("hyperion_version = {0}\n".format(hyperion.__version__))
f.write("mysg_version = {0}\n".format(mysg.__version__))
f.close()

for line in open('grids.txt', 'r'):

    print(line)

    if line[5] != 'm':
        continue

    grid = line.strip()

    create_anthill_files_sed(grids_dir, grid)
