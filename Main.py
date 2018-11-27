import pandas as pd
import numpy as np
pd.set_option('max_columns', 120)
pd.set_option('max_colwidth', 5000)

# skip row 1 so pandas can parse the data properly.
df = pd.read_csv('data.csv', low_memory=False)
print(len(df.columns))
print(df.columns)

half_count = len(df) / 2
df = df.dropna(thresh=half_count, axis=1) # Drop any column with more than 50% missing values
print(len(df.columns))
print(df.columns)

pass

# import matplotlib.pyplot as plt
# import seaborn as sns
# %matplotlib inline
# plt.rcParams['figure.figsize'] = (12,8)


#with open("data.csv") as data:

