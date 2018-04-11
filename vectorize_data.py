import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn.feature_extraction.text import TfidfVectorizer as TF

MOREOVER = "./data/moreover.csv"
OPOINT = "./data/opoint.csv"

def read_data(choice):
    fn = MOREOVER if choice==1 else OPOINT
    df = pd.read_csv(fn, sep = ';')
    return df

def split_data(df):
    y = df['momentum']
    x = df.drop('momentum', axis = 1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    return x_train, x_test, y_train, y_test

def vectorize_text(x_train, x_test, feature_count):
    vectorizer = CV(strip_accents='unicode', analyzer = 'word',
                                    max_features = feature_count)
    text_train = vectorizer.fit_transform(x_train).toarray()
    text_test = vectorizer.transform(x_test).toarray()
    text_train,text_test = pd.DataFrame(text_train),pd.DataFrame(text_test)

    return text_train, text_test

def get_data(feature_count = 10000,choice = 1):
    df = read_data(choice)
    df = df[df.momentum.notnull()]
    df = df.fillna("")
    x_train, x_test, y_train, y_test = split_data(df)

    field1 = "header_text" if choice == 0 else "title"

    v1_train, v1_test = vectorize_text(x_train[field1],
                                     x_test[field1],feature_count)

    field1 = "body_text" if choice == 0 else "content"
    v2_train, v2_test = vectorize_text(x_train[field1],
                                     x_test[field1],feature_count)

    x_train = pd.concat([v1_train,v2_train], axis = 1, ignore_index = True)
    x_test = pd.concat([v1_test, v2_test], axis = 1, ignore_index = True)
    print "Total feature count:",x_train.shape[-1]

    return x_train, x_test, y_train, y_test
