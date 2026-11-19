import os
import sys
import glob

if len(sys.argv) != 3:
    print("Usage: python {0} grid_directory trash_directory".format(sys.argv[0]))
    sys.exit(0)
else:
    directory = sys.argv[1]
    trash = sys.argv[2]

for grid in glob.glob(os.path.join(directory, 's??????-----')):

    # Make trash sub-folder
    grid_trash = os.path.join(trash, os.path.basename(grid))

    for gridlet in glob.glob(os.path.join(grid, 'log', '??')):

        for out_file in glob.glob(os.path.join(gridlet, '*_sed.out')):
            out_file_moved = os.path.join(grid_trash, os.path.basename(out_file.replace('_sed.out', '.out')))
            if os.path.exists(out_file_moved):
                os.rename(out_file_moved, out_file.replace('_sed.out', '.out'))
                os.rename(out_file, out_file_moved.replace('.out', '_sed.out'))

        for err_file in glob.glob(os.path.join(gridlet, '*_sed.err')):
            err_file_moved = os.path.join(grid_trash, os.path.basename(err_file.replace('_sed.err', '.err')))
            if os.path.exists(err_file_moved):
                os.rename(err_file_moved, err_file.replace('_sed.err', '.err'))
                os.rename(err_file, err_file_moved.replace('.err', '_sed.err'))

    for gridlet in glob.glob(os.path.join(grid, 'anthill', 'qsub', '??')):

        for qsub_file in glob.glob(os.path.join(gridlet, '*_sed.qsub')):
            qsub_file_moved = os.path.join(grid_trash, os.path.basename(qsub_file.replace('_sed.qsub', '.qsub')))
            if os.path.exists(qsub_file_moved):
                os.rename(qsub_file_moved, qsub_file.replace('_sed.qsub', '.qsub'))
                os.rename(qsub_file, qsub_file_moved.replace('.qsub', '_sed.qsub'))
