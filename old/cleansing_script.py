import holidays
import numpy as np
import os
import pandas as pd
import sys

import green_cleansing as green
import yellow_cleansing as yellow
from cleansing import utils as ut


def main(argv):
    # read the csv using panda.
    data_frame = pd.read_csv(argv[0], low_memory=False)
    data_type = argv[1]
    if data_type == "yellow":
        yellow.yellow_clean(argv[0],data_frame)
    elif data_type == "green":
        green.green_clean(argv[0],data_frame)





if __name__ == '__main__':
    main(sys.argv[1:])