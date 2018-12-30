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

    #regr = tree.DecisionTreeRegressor()
    regr = RandomForestRegressor(random_state=0, n_estimators=100)
    #regr = svm.SVR(gamma='scale', C=1.0, epsilon=0.2)
    #regr = linear_model.Lasso(alpha=0.1) # alpha is regularization const

    y_list = []
    y_hat_list = []
    regr = regr.fit(train_df, train_target_df)
    for example, target in zip(test_df, test_target_df):
        pred = regr.predict([example])
        y_list.append(target)
        y_hat_list.append(pred)
        print("Real value: {}, Predicted value: {}".format(target, pred))
    print str(mean_absolute_error(y_list,y_hat_list))

    pass


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Missing arguments!")
        sys.exit(1)
    main(*sys.argv[1:])