import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def master_function():
    df = read_data()
    df["momentum"] = df["momentum"].fillna(0)
    df = df.fillna("")
    x_train, x_test, y_train, y_test = split_data(df)
    x_train, x_test = vectorize(x_train, x_test)

def read_data(fn = "./data/opoint.csv"):
    df = pd.read_csv(fn, sep = ',')
    return df

def split_data(df):
    x = df.iloc[:,:-1]
    y = df['momentum']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    return x_train, x_test, y_train, y_test

def vectorize(x_train, x_test):
    count_vect = CountVectorizer()
    header_text_train = count_vect.fit_transform(x_train["header_text"])
    header_text_test = count_vect.transform(x_test["header_text"])

    print (header_text_train.shape)

    # count_vect = CountVectorizer()
    # summary_text_train = count_vect.fit_transform(x_train["summary_text"])
    # summary_text_test = count_vect.transform(x_test["summary_text"])
    #
    # count_vect = CountVectorizer()
    # body_text_train = count_vect.fit_transform(x_train["body_text"])
    # body_text_test = count_vect.transform(x_test["body_text"])
    #
    # x_train = header_text_train.join(summary_text_train).join(body_text_train).join(x_train["firstSource_name"])
    # x_test = header_text_test.join(summary_text_test).join(body_text_test).join(x_test["firstSource_name"])

    return x_train, x_test

if __name__ == "__main__":
    master_function()
