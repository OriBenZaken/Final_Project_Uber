from sklearn.utils import resample
import pandas as pd
import utils as ut
data_frame_x = pd.read_csv("train1short.csv", low_memory=False)
data_frame_y = pd.read_csv("train1_target_short.csv", low_memory=False)

x,y = resample(data_frame_x, data_frame_y, n_samples=10, random_state=0)

ut.save_file("x.csv", x)
ut.save_file("y.csv", y)
