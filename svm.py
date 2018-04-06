from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC

def run_model():
    twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
    twenty_test = fetch_20newsgroups(subset='test', shuffle=True)

    count_vect = CountVectorizer()
    x_train = count_vect.fit_transform(twenty_train.data)
    print len(twenty_train.data), x_train.shape
    x_test = count_vect.transform(twenty_test.data)

    # print len(twenty_train.target)
    # print len(twenty_test.target)

    # clf = SVC()
    # clf.fit(x_train, twenty_train.target)
    # print clf.score(x_test, twenty_test.target)

if __name__ == "__main__":
    run_model()
