import pandas as pd
import numpy as np
pd.set_option('max_columns', 120)
pd.set_option('max_colwidth', 5000)

# read the csv using panda.
data_frame = pd.read_csv('data.csv', low_memory=False)

half_count = len(data_frame) / 2
data_frame = data_frame.dropna(thresh=half_count, axis=1) # Drop any column with more than 50% missing values

# drop irrelevant columns
drop_list = ['store_and_fwd_flag']
data_frame = data_frame.drop(drop_list,axis=1)




print "liz"
# import matplotlib.pyplot as plt
# import seaborn as sns
# %matplotlib inline
# plt.rcParams['figure.figsize'] = (12,8)


#with open("data.csv") as data:

