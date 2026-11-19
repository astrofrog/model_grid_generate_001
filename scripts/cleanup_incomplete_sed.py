import os
import sys
import glob

import h5py

if len(sys.argv) != 3:
    print("Usage: python {0} grid_directory trash_directory".format(sys.argv[0]))
    sys.exit(0)
else:
    directory = sys.argv[1]
    trash = sys.argv[2]

if not os.path.exists(trash):
    os.mkdir(trash)

for grid in glob.glob(os.path.join(directory, 's??????-----')):

    print("Processing {0}...".format(grid))

    # Make trash sub-folder
    grid_trash = os.path.join(trash, os.path.basename(grid))
    if not os.path.exists(grid_trash):
        os.mkdir(grid_trash)

    for gridlet in glob.glob(os.path.join(grid, 'output', '??')):
        for output_file in glob.glob(os.path.join(gridlet, '*_sed.rtout')):

            try:
                frt = h5py.File(output_file, 'r')
                frt.attrs['cpu_time']
                frt['Peeled']['group_00001']['seds']
                frt.close()
            except Exception:
                pass
            else:
                continue

            qsub_file = output_file.replace('output', 'anthill/qsub').replace('.rtout', '.qsub')
            out_file = output_file.replace('output', 'log').replace('.rtout', '.out')
            err_file = output_file.replace('output', 'log').replace('.rtout', '.err')
            input_file = output_file.replace('output', 'input').replace('.rtout', '.rtin')
            for filename in (input_file, output_file, out_file, err_file, qsub_file):
                # try:
                os.rename(filename, os.path.join(grid_trash, os.path.basename(filename)))
                # except OSError:
                # pass
