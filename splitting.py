import sys
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import utils as ut
from sklearn.utils import resample
from os.path import isfile, join


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", help="Filtered data file")
    parser.add_argument("-resample", help="Number of examples to resample", default=0)
    parser.add_argument("-target_dir", help="target dir of files to be saved in", default="model_data")

    args = parser.parse_args()
    data_frame = pd.read_csv(args.data_file, low_memory=False)
    # split the data
    cols = [col for col in data_frame.columns if col != 'demand']
    # dropping the 'demand' column
    data = data_frame[cols]
    # assigning the fare_amount column as target
    target = data_frame['demand']
    # operate resample to get important rows
    if args.resample != 0:
        data, target = resample(data, target, n_samples=args.resample, random_state=0)
    # split data set into train and test sets
    data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.30, random_state=10)
    ut.create_dir(args.target_dir)
    ut.save_file(join(args.target_dir, 'train'), data_train, header=False)
    ut.save_file(join(args.target_dir, 'test'), data_test, header=False)
    ut.save_file(join(args.target_dir, 'target_train'), target_train, header=False)
    ut.save_file(join(args.target_dir, 'target_test'), target_test, header=False)


if __name__ == '__main__':
    main()