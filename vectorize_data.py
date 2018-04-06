import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer as TF

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
    tf = TF()
    header_text_train = tf.fit_transform(count_vect.fit_transform(x_train["header_text"])).toarray()
    header_text_test = tf.transform(count_vect.transform(x_test["header_text"])).toarray()
    header_text_train,header_text_test = pd.DataFrame(header_text_train), pd.DataFrame(header_text_test)

    count_vect = CountVectorizer()
    tf = TF()
    summary_text_train = tf.fit_transform(count_vect.fit_transform(x_train["summary_text"])).toarray()
    summary_text_test = tf.transform(count_vect.transform(x_test["summary_text"])).toarray()
    summary_text_train,summary_text_test = pd.DataFrame(summary_text_train),pd.DataFrame(summary_text_test)

    count_vect = CountVectorizer()
    tf = TF()
    body_text_train = tf.fit_transform(count_vect.fit_transform(x_train["body_text"])).toarray()
    body_text_test = tf.transform(count_vect.transform(x_test["body_text"])).toarray()
    body_text_train,body_text_test = pd.DataFrame(body_text_train),pd.DataFrame(body_text_test)

    x_train = header_text_train.\
             join(summary_text_train,lsuffix='_head', rsuffix='_summary').\
             join(body_text_train,lsuffix='_headsum',rsuffix='_body')
             #.\join(x_train[["firstSource_name"]],lsuffix='_text',rsuffix='_source')

    x_test = header_text_test.\
             join(summary_text_test,lsuffix='_head', rsuffix='_summary').\
             join(body_text_test,lsuffix='_headsum',rsuffix='_body')
             #.\join(x_test[["firstSource_name"]],lsuffix='_text',rsuffix='_source')

    print x_train.shape
    print x_test.shape
    return summary_text_train, summary_text_test

def master_function():
    df = read_data()
    df = df[df.momentum.notnull()]
    df = df.fillna("")
    x_train, x_test, y_train, y_test = split_data(df)
    x_train, x_test = vectorize(x_train, x_test)

    return x_train, x_test, y_train, y_test


if __name__ == "__main__":
    master_function()
