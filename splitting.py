import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import utils as ut

def main(argv):
    data_frame = pd.read_csv(argv[0], low_memory=False)
    # split the data
    cols = [col for col in data_frame.columns if col != 'demand']
    # dropping the 'demand' column
    data = data_frame[cols]
    # assigning the fare_amount column as target
    target = data_frame['demand']
    # split data set into train and test sets
    data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.30, random_state=10)
    ut.save_filtered_file('train1', data_train, header=False)
    ut.save_filtered_file('test1', data_test, header=False)
    ut.save_filtered_file('target_train1', target_train, header=False)
    ut.save_filtered_file('target_test1', target_test, header=False)

    pass




if __name__ == '__main__':
    main(sys.argv[1:])