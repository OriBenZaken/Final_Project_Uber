import pandas as pd
import numpy as np
import holidays

def main():
    pd.set_option('max_columns', 120)
    pd.set_option('max_colwidth', 5000)

    # read the csv using panda.
    data_frame = pd.read_csv('data.csv', low_memory=False)

    half_count = len(data_frame) / 2
    # axis = 1 indicates remove of cols, and axis = 0 indicates remove of rows
    data_frame = data_frame.dropna(thresh=half_count, axis=1) # Drop any column with more than 50% missing values
    # Drop any row with null values
    data_frame = data_frame.dropna(axis=0, how='any')


    # drop irrelevant columns
    drop_list = ['store_and_fwd_flag']
    data_frame = data_frame.drop(drop_list,axis=1)

    # adding cols
    data_frame['pickup_datetime'] = data_frame['pickup_datetime'].apply(pd.Timestamp)
    data_frame['weekday'] = data_frame['pickup_datetime'].dt.weekday
    data_frame['day'] = data_frame['pickup_datetime'].dt.day
    data_frame['month'] = data_frame['pickup_datetime'].dt.month
    data_frame['year'] = data_frame['pickup_datetime'].dt.year
    data_frame['hour'] = data_frame['pickup_datetime'].dt.hour
    # casting to dateTime format
    data_frame['pickup_datetime'] = pd.to_datetime(data_frame['pickup_datetime'])
    # adding is_weekend feature
    data_frame['is_weekend'] = data_frame.apply(add_is_weekend_col, axis=1)
    # adding is_holiday feature
    data_frame['is_holiday'] = data_frame.apply(add_is_holiday_col, axis=1)

    print(data_frame.head())

def add_is_weekend_col(row):
    return int(row['weekday'] in [6,7,1])

def add_is_holiday_col(row):
    date = row['pickup_datetime'].date()
    usa_holidays = holidays.US(years=int(row['year']), state='NY')
    return int(date in usa_holidays)

if __name__ == '__main__':
    main()