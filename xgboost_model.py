import xgboost

from sklearn import tree
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn import linear_model

def main(train_file, train_target_file, test_file, test_target_file):
    train_df = np.loadtxt(train_file, delimiter=',')
    train_target_df =  np.loadtxt(train_target_file, delimiter=',')
    test_df =  np.loadtxt(test_file, delimiter=',')
    test_target_df =  np.loadtxt(test_target_file, delimiter=',')
    model = xgboost.XGBRegressor(colsample_bytree=0.4,
                                 gamma=0,
                                 learning_rate=0.07,
                                 max_depth=3,
                                 min_child_weight=1.5,
                                 n_estimators=10000,
                                 reg_alpha=0.75,
                                 reg_lambda=0.45,
                                 subsample=0.6,
                                 seed=42)
    model.fit(train_df, train_target_df)
    y_list, y_hat_list = run_test(test_df, test_target_df, model)
    print("Mean absolute error: {}".format(get_mean_absolute_error(y_list, y_hat_list)))
    print("Average relative error: {}".format(get_average_relative_error(y_list, y_hat_list)))

def run_test(test_df, test_target_df, model):
    y_list = []
    y_hat_list = []
    for example, target in zip(test_df, test_target_df):
        pred = model.predict([example])
        y_list.append(target)
        y_hat_list.append(pred)
        print("Real value: {}, Predicted value: {}".format(target, pred))
    return y_list,y_hat_list

def get_mean_absolute_error(y_list, y_hat_list):
    return mean_absolute_error(y_list, y_hat_list)

def get_average_relative_error(y_list, y_hat_list):
    sum = 0
    for y, y_hat in zip(y_list,y_hat_list):
        if (y > y_hat):
            relative_error = (1 - float(y_hat)/float(y)) * 100
        else:
            relative_error = (1 - float(y)/float(y_hat)) * 100
        sum += relative_error
    average_relative_error = float(sum)/len(y_list)
    return average_relative_error





if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Missing arguments!")
        sys.exit(1)
    main(*sys.argv[1:])