import pandas as pd
#import the necessary module
from sklearn.model_selection import train_test_split

data_frame = pd.read_csv('data_filtered.csv', low_memory=False)

# split the data

# select columns other than 'Opportunity Number','Opportunity Result'
cols = [col for col in data_frame.columns if col is not 'fare_amount']

# dropping the 'fare_amount' column
data = data_frame[cols]

# assigning the fare_amount column as target
target = data_frame['fare_amount']
# split data set into train and test sets
data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.30, random_state=10)