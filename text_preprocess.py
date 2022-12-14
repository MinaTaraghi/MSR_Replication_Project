#
# Text Preprocessing Utils:
# Data cleaning
# Vectorization (BOW (count), and TF-IDF)
#

import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt


#
# adapted from:
# https://stackoverflow.com/a/2743163/6463816

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def strip_punctuation(string):
    string = re.sub('[^A-Za-z0-9]+',' ', string)
    return string

#
# adapted from
#
#https://www.geeksforgeeks.org/python-split-camelcase-string-to-individual-strings/

def camel_case_split(str):
    words = [[str[0]]]

    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return ''.join([''.join(word) for word in words] )

def apply_stop_stem(str):
    ps = PorterStemmer()
    words = str.split ()
    sw=[]
    to_remove=set(stopwords.words('english'))
    for w in words:
        if w not in to_remove:
            sw.append(ps.stem(w))

    return ' '.join(sw)


def cleanup(df):
    df.dropna(inplace=True)
    for index, row in df.iterrows():
        text=row["XCM"]
        text=text.lower()
        text=strip_non_ascii(text)
        text=strip_punctuation(text)
        text=camel_case_split(text)
        text=apply_stop_stem (text)
        df.at[index,'XCM'] = text
    df.groupby('defect_status').XCM.count().plot.bar(ylim=0, color=['red','green'])
    #plt.show()
    plt.savefig("barchart.png")
    return df

def create_count_corpora(df,min_freq):
    cv = CountVectorizer(min_df=min_freq)

    cv.fit(df['XCM'])
    vector = cv.transform(df['XCM'])
    #
    # uncomment if needed
    #
    # print("Vocabulary")
    # print(cv.vocabulary_)
    print("Shape")
    print(vector.shape)
    print("Array type:")
    print(vector.toarray().shape)
    bigarray = vector.toarray()
    print(bigarray.shape)

    return bigarray, df['defect_status']


def create_tfidf_corpora(df,min_freq):
    cv = TfidfVectorizer(min_df=min_freq)

    cv.fit(df['XCM'])
    vector = cv.transform(df['XCM'])
    #
    # uncomment if needed
    #
    # print("Vocabulary")
    # print(cv.vocabulary_)
    print("Shape")
    print(vector.shape)
    print("Shape")
    print(vector.shape)
    print("Array type:")
    print(vector.toarray().shape)
    bigarray = vector.toarray()
    print(bigarray.shape)

    return bigarray, df['defect_status']

