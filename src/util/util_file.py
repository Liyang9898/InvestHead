import os
import glob


def get_all_csv_file_in_folder(folder):
#     path = 'c:\\'
    extension = 'csv'
    os.chdir(folder)
    filenames = glob.glob('*.{}'.format(extension))
    files = []
    for f in filenames:
        files.append(folder+f)
    return files

