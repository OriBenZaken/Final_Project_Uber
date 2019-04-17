% pyspark
from sklearn.ensemble import RandomForestRegressor
import sys
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib
from sklearn import svm, datasets
from spark_sklearn import GridSearchCV


def main():
    absolute_path = "/data/model_data/"
    train_df = np.loadtxt(absolute_path + "train.csv", delimiter=',')
    train_target_df = np.loadtxt(absolute_path + "target_train.csv", delimiter=',')
    test_df = np.loadtxt(absolute_path + "test.csv", delimiter=',')
    test_target_df = np.loadtxt(absolute_path + "target_test.csv", delimiter=',')
    regr = RandomForestRegressor(random_state=0, n_estimators=1000, min_samples_leaf=1)  # best model so far!
    # pyspark
    regr_rf_cv = GridSearchCV(sc=spark.sparkContext,
                              estimator=regr,
                              n_jobs=20,
                              cv=5,
                              verbose=5,
                              param_grid={})
    regr_rf_cv.fit(train_df, train_target_df)
    # regr = regr.fit(train_df, train_target_df)
    y_list, y_hat_list = run_test(test_df, test_target_df, regr_rf_cv)
    print("Mean absolute error: {}".format(get_mean_absolute_error(y_list, y_hat_list)))
    print("Average relative error: {}".format(get_average_relative_error(y_list, y_hat_list)))
    save_model(regr_rf_cv.best_estimator_, "rf_uber_model", "/data/saved_model/")
    load_model("/data/saved_model/rf_uber_model.pkl", testExample=(test_df[0], test_target_df[0]))


def save_model(model, model_name, path):
    with open(path + model_name + ".pkl", 'wb') as f:
        joblib.dump(model, f, compress=1)
        print("Model was saved in: " + path + model_name + ".pkl")


def load_model(model_path, testExample=None):
    with open(model_path, 'rb') as f:
        loaded_model = joblib.load(f)
        if testExample:
            test_saved_model(loaded_model, testExample)


def test_saved_model(model, testExample):
    pred = model.predict([testExample[0]])
    print("Testing saved model:: Real value: {}, Predicted value: {}".format(testExample[1], pred))


def run_test(test_df, test_target_df, model):
    y_list = []
    y_hat_list = []
    for example, target in zip(test_df, test_target_df):
        pred = model.predict([example])
        y_list.append(target)
        y_hat_list.append(pred)
        # print("Real value: {}, Predicted value: {}".format(target, pred))
    return y_list, y_hat_list


def get_mean_absolute_error(y_list, y_hat_list):
    return mean_absolute_error(y_list, y_hat_list)


def get_average_relative_error(y_list, y_hat_list):
    sum = 0
    for y, y_hat in zip(y_list, y_hat_list):
        if (y > y_hat):
            relative_error = (1 - float(y_hat) / float(y)) * 100
        else:
            relative_error = (1 - float(y) / float(y_hat)) * 100
        sum += relative_error
    average_relative_error = float(sum) / len(y_list)
    return average_relative_error


main()