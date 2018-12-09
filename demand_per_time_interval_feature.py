#import utils as ut
import pandas as pd
import time
from datetime import datetime
from collections import Counter

class Demand_per_time_interval(object):
    def __init__(self, data_frame, timestamp_col):
        self.time_interval_dict = Counter()
        self.timestamp_col = timestamp_col
        self.explore_demand_per_time_interval(data_frame)

    def explore_demand_per_time_interval(self, data_frame):
        for row in data_frame[self.timestamp_col]:
            start, end = self.map_time_to_time_interval(row.time())
            self.time_interval_dict[(str(row.date()), start, end)] += 1

    def get_10_minutes_interval(self, minutes):
        start = int(minutes) // 10 * 10
        end = start + 9
        return start, end

    def map_time_to_time_interval(self, time):
        hour = time.hour
        start_min, end_min = self.get_10_minutes_interval(time.minute)
        start, end = str(hour) + ":" + str(start_min), str(hour) + ":" + str(end_min)
        return start, end

    def add_demand_col(self, row):
        time = row[self.timestamp_col].time()
        start, end = self.map_time_to_time_interval(time)
        return self.time_interval_dict[(str(row[self.timestamp_col].date()), start, end)]

# read the csv using panda.
data_frame = pd.read_csv("sample.csv", low_memory=False)
# drop any row with null values
data_frame = data_frame.dropna(axis=0, how='any')
data_frame['Date/Time'] = pd.to_datetime(data_frame['Date/Time'])
demand_per_time_interval = Demand_per_time_interval(data_frame, timestamp_col='Date/Time')
data_frame['demand'] = data_frame.apply(demand_per_time_interval.add_demand_col, axis=1)
print(data_frame.head())
