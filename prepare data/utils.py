import pandas as pd
import numpy as np
import holidays
import sys
import os
import matplotlib.pyplot as plt
from collections import Counter


def clean_null_values(data_frame):
    """
    clean any rows and cols with missing data
    :param data_frame:
    :return:
    """
    half_count = len(data_frame) / 2
    # axis = 1 indicates remove of cols, and axis = 0 indicates remove of rows
    data_frame = data_frame.dropna(thresh=half_count, axis=1)  # Drop any column with more than 50% missing values
    # drop any row with null values
    data_frame = data_frame.dropna(axis=0, how='any')
    return data_frame


def add_fetures(data_frame, date_time_col_name):
    """
    add features to data frame
    :param data_frame: given data frame
    :param date_time_col_name: date col name
    :return: new df
    """
    # adding cols
    data_frame[date_time_col_name] = data_frame[date_time_col_name].apply(pd.Timestamp)
    data_frame['weekday'] = data_frame[date_time_col_name].dt.weekday
    data_frame['day'] = data_frame[date_time_col_name].dt.day
    data_frame['month'] = data_frame[date_time_col_name].dt.month
    data_frame['year'] = data_frame[date_time_col_name].dt.year
    data_frame['hour'] = data_frame[date_time_col_name].dt.hour
    # casting to dateTime format
    data_frame[date_time_col_name] = pd.to_datetime(data_frame[date_time_col_name])
    # adding is_weekend feature
    data_frame['is_weekend'] = data_frame.apply(add_is_weekend_col, axis=1)
    # adding is_holiday feature
    data_frame['is_holiday'] = data_frame.apply(add_is_holiday_col, axis=1)
    # adding demand col
    demand_per_time_interval = Demand_per_time_interval(data_frame, timestamp_col='date_time', region_col='Base')
    data_frame['demand'] = data_frame.apply(demand_per_time_interval.add_demand_col, axis=1)
    return  data_frame

def save_file(file_name, data_frame, header=True):
    """
    save given csv file
    :param file_name: file name to be saved
    :param data_frame: given data frame to be saved
    :param header: boolean
    :return:
    """
    # save the data_frame into csv file
    file_name = os.path.splitext(file_name)[0]
    data_frame.to_csv(file_name + ".csv", mode='w',index=False,header=header)

def create_dir(dir_name):
    """
    create dir
    :param dir_name: dir name
    """
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def add_is_weekend_col(row):
    """
    add is weekend col
    :param row: given row
    :return: weekday param
    """
    return int(row['weekday'] in [6,7,1])

def add_is_holiday_col(row):
    """
    add is holiday col
    :param row: given row
    :return: date_time param
    """
    date = row['date_time'].date()
    usa_holidays = holidays.US(years=int(row['year']))
    return int(date in usa_holidays)

def plot_correlations(data_frame):
    """
    plot correlations between features
    :param data_frame:
    """
    correlations = data_frame.corr()
    # plot correlation matrix
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, 9, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    columnNames = list(data_frame.head(0))
    ax.set_xticklabels(columnNames)
    ax.set_yticklabels(columnNames)
    plt.show()

def drop_irrelevant_cols(data_frame,drop_list):
    """
    drop irrelevant cols
    :param data_frame: given df
    :param drop_list: givan cols to be removed
    :return: new df
    """
    # drop irrelevant columns
    data_frame = data_frame.drop(drop_list, axis=1)
    return data_frame

def remove_rows_with_zero_fare_amount(data_frame):
    """
    remove rows with zero fare amount
    :param data_frame: given df
    :return: new df
    """
    data_frame = data_frame[data_frame.fare_amount != 0]
    return data_frame

class Demand_per_time_interval(object):
    def __init__(self, data_frame, timestamp_col, region_col):
        """
        constructor
        :param data_frame: data
        :param timestamp_col: time column
        """
        self.time_interval_dict = Counter()
        self.timestamp_col = timestamp_col
        self.region_col = region_col
        self.explore_demand_per_time_interval(data_frame)

    def explore_demand_per_time_interval(self, data_frame):
        """
        this function adds 1 to the demand of each relevant timestamp according to row data
        :param data_frame: data
        """
        for index, row in data_frame.iterrows():
            timestamp = row[self.timestamp_col]
            start, end = self.map_time_to_time_interval(timestamp.time())
            self.time_interval_dict[(str(row[self.region_col]), str(timestamp.date()), start, end)] += 1

    def get_10_minutes_interval(self, minutes):
        """
        get start and end time of interval
        :param minutes:
        :return:
        """
        start = int(minutes) // 10 * 10
        end = start + 9
        return start, end

    def map_time_to_time_interval(self, time):
        """
        get time interval edges
        :param time: given time
        :return: time interval edges
        """
        hour = time.hour
        start_min, end_min = self.get_10_minutes_interval(time.minute)
        start, end = str(hour) + ":" + str(start_min), str(hour) + ":" + str(end_min)
        return start, end

    def add_demand_col(self, row):
        """
        add demand col to given row
        :param row: given row
        :return: demand value
        """
        time = row[self.timestamp_col].time()
        start, end = self.map_time_to_time_interval(time)
        return self.time_interval_dict[(str(row[self.region_col]),str(row[self.timestamp_col].date()),
                                                                  start, end)]
