from os import listdir
from os.path import isfile, join
import sys
import pandas as pd
import utils as ut

def main(argv):
    dir_name = argv[0]

    files_list = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
    data_frame_list = [pd.read_csv(f, low_memory=False) for f in files_list]
    unified_data_frame = pd.concat(data_frame_list)
    ut.save_filtered_file("unified.csv",unified_data_frame)


if __name__ == '__main__':
    main(sys.argv[1:])