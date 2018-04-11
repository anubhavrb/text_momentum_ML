import sys
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVR
from vectorize_data import get_data
from sklearn.linear_model import Ridge
from sklearn.ensemble import AdaBoostRegressor as ADA
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.ensemble import GradientBoostingRegressor as GB
from sklearn.ensemble import BaggingRegressor as BAG
from sklearn.tree import DecisionTreeRegressor as DT
from sklearn.neighbors import KNeighborsRegressor as KNN
from sklearn.model_selection import RandomizedSearchCV

def run_model(data_choice, feature_count):
    x_train, x_test, y_train, y_test = get_data(feature_count,data_choice)
    clf = RF()
    clf.fit(x_train, y_train)
    return  x_train.shape[-1],clf.score(x_test, y_test)

def tune_params(feature_count):
    X_train, X_test, y_train, y_test = get_data(feature_count,2)

    # model params
    params = {"criterion" : ["mse", "mae"], # use entropy
              "splitter" : ["best", "random"],
              "max_depth" : range(2,21),
              "min_samples_split" : range(2,21),
              "min_samples_leaf" : range(1,21),
              "min_impurity_decrease" : [0.0, 0.05, 0.1, 0.15, 0.2, 0.25]}

    # run randomized search
    n_iter_search = 60
    clf = RandomizedSearchCV(DT(), param_distributions=params,
                                       n_iter=n_iter_search, n_jobs = -1)
    clf.fit(X_train, y_train)
    r2 = clf.score(X_test,y_test)

    print "\tBest result from Tunning: %d features, score of %.5f" % (X_train.shape[-1],r2)
    print clf.best_params_

if __name__ == "__main__":
    tune_params(1000)
