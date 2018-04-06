from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVR
from vectorize_data import master_function as get_data
def run_model():
    x_train, x_test, y_train, y_test = get_data()
    clf = SVR()
    clf.fit(x_train, y_train)
    print clf.score(x_test, y_test)

if __name__ == "__main__":
    run_model()
