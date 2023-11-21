
import pandas as pd

def test():
    stop_words = pd.read_csv('./keywordExtract/stopwords-en.txt', index_col=False, quoting=3, sep="\t", names=['stopword'],encoding='utf-8')
    stop_words = stop_words['stopword'].values
    print(stop_words)