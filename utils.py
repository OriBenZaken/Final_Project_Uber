import pandas as pd
import numpy as np
import holidays
import sys
import os
import utils as ut


def clean_null_values(data_frame):
    half_count = len(data_frame) / 2
    # axis = 1 indicates remove of cols, and axis = 0 indicates remove of rows
    data_frame = data_frame.dropna(thresh=half_count, axis=1)  # Drop any column with more than 50% missing values
    # drop any row with null values
    data_frame = data_frame.dropna(axis=0, how='any')
    return data_frame

def drop_irrelevant_cols(data_frame,drop_list):
    # drop irrelevant columns
    data_frame = data_frame.drop(drop_list, axis=1)
    return data_frame
def remove_rows_with_zero_fare_amount(data_frame):
    liz = data_frame.fare_amount
    data_frame = data_frame[data_frame.fare_amount != 0]
    #data_frame[str(data_frame['fare_amount'])!=0]
    return data_frame
def add_fetures(data_frame):
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
    return  data_frame

def save_filtered_file(file_name, data_frame):
    # save the data_frame into csv file
    file_name = os.path.splitext(file_name)[0]
    data_frame.to_csv(file_name + "_filtered.csv", mode='w')

def add_is_weekend_col(row):
    return int(row['weekday'] in [6,7,1])

def add_is_holiday_col(row):
    date = row['pickup_datetime'].date()
    usa_holidays = holidays.US(years=int(row['year']), state='NY')
    return int(date in usa_holidays)