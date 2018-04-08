import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer as TF

def read_data(fn = "./data/opoint.csv"):
    df = pd.read_csv(fn, sep = ',')
    return df

def split_data(df):
    y = df['momentum']
    x = df.drop('momentum', axis = 1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    return x_train, x_test, y_train, y_test

def vectorize_text(x_train, x_test, feature_count):
    count_vect = CountVectorizer(strip_accents='unicode', analyzer = 'word', 
                                 max_features = feature_count)
    text_train = count_vect.fit_transform(x_train).toarray()
    text_test = count_vect.transform(x_test).toarray()
    text_train,text_test = pd.DataFrame(text_train),pd.DataFrame(text_test)
    
    return text_train, text_test

def get_data(feature_count = 10000):
    df = read_data()
    df = df[df.momentum.notnull()]
    df = df.fillna("")
    x_train, x_test, y_train, y_test = split_data(df)
    x_train, x_test = vectorize_text(x_train['header_text'], 
                                     x_test['header_text'],feature_count)

    return x_train, x_test, y_train, y_test

if __name__ == "__main__":
    master_function()
