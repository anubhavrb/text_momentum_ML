import sys
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVR
from vectorize_data import get_data
from sklearn.linear_model import LinearRegression as LR
from sklearn.ensemble import AdaBoostRegressor as ADA
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.ensemble import GradientBoostingRegressor as GB
from sklearn.ensemble import BaggingRegressor as BAG
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

def run_model(data_choice, feature_count):
    x_train, x_test, y_train, y_test = get_data(feature_count,data_choice)
    clf = DecisionTreeRegressor()
    clf.fit(x_train, y_train)
    print clf.score(x_test, y_test)

if __name__ == "__main__":
    run_model(int(sys.argv[1]), int(sys.argv[2]))
