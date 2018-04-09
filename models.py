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

def run_model():
    x_train, x_test, y_train, y_test = get_data(10000)
    clf = KNeighborsRegressor()
    clf.fit(x_train, y_train)
    print clf.score(x_test, y_test)

if __name__ == "__main__":
    run_model()
