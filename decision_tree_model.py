from sklearn.ensemble import RandomForestRegressor
import sys
import numpy as np
from sklearn.metrics import mean_absolute_error
from joblib import dump, load

def main(train_file, train_target_file, test_file, test_target_file):
    train_df = np.loadtxt(train_file, delimiter=',')
    train_target_df =  np.loadtxt(train_target_file, delimiter=',')
    test_df =  np.loadtxt(test_file, delimiter=',')
    test_target_df =  np.loadtxt(test_target_file, delimiter=',')
    regr = RandomForestRegressor(random_state=0, n_estimators=500, min_samples_leaf= 5) #best model so far!

    regr = regr.fit(train_df, train_target_df)
    y_list, y_hat_list = run_test(test_df, test_target_df, regr)
    print("Mean absolute error: {}".format(get_mean_absolute_error(y_list, y_hat_list)))
    print("Average relative error: {}".format(get_average_relative_error(y_list, y_hat_list)))


def save_model(model_name, model):
    dump(model, model_name + '.joblib')

def load_model(model_name):
    return load(model_name + '.joblib')


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