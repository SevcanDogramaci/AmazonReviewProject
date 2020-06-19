from re import search
from nltk import pos_tag
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

analyser = SentimentIntensityAnalyzer()

def get_common_words(val):
    s = ""
    for item in val:
        s = s + " " + item[0]
        
    counter = Counter(s.split())
    most_occur = counter.most_common(2)
    
    if len(most_occur) > 1:
        if most_occur[0][1] != most_occur[1][1]:
            most_occur = [most_occur[0]]
            
    return most_occur

def find_top_words(data, word_num):

    doc = pd.Series(data)

    # find top words in cleared reviews by counting
    top = doc.value_counts().head(word_num).index.tolist()
    print("Top " + str(word_num) + " words : " + str(top))
    return top


def get_polarity_scores(sentences):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    analyser = SentimentIntensityAnalyzer()

    scores = []

    # get polarity score of reviews
    for sentence in sentences:
        score = analyser.polarity_scores(sentence)
        scores.append(score)

    return pd.DataFrame(scores)


def get_tfidf(sentences, min_df, max_df):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import NMF

    # TF - IDF
    tfidf = TfidfVectorizer(ngram_range=(1, 2), max_df=max_df, min_df=min_df)
    features = tfidf.fit_transform(sentences)

    # Nonnegative Matrix Factorization
    nmf = NMF(n_components=4, random_state=1).fit(features)

    # Print topics
    for topic_idx, topic in enumerate(nmf.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([tfidf.get_feature_names()[i]
                        for i in topic.argsort()[:-5 - 1:-1]]))
        print()

    return pd.DataFrame(features.todense(), columns=tfidf.get_feature_names())


def get_count_vectorizer(sentences):
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer()
    x = vectorizer.fit_transform(sentences)
    vectorizer.build_analyzer()

    return pd.DataFrame(x.todense(), columns=vectorizer.get_feature_names())


def get_ngrams(sentence, n):
    from nltk import ngrams
    return ngrams(sentence.split(), n)


# def isNegative(polarity, x):
#    return polarity["compound"][x] < 0 and polarity["neu"][x] < 0.9

def isNegative(polarity):
    return polarity["compound"] < 0 and polarity["neu"] < 0.9


def get_polarity(sentence):
    score = analyser.polarity_scores(sentence)
    return score


def polarize_reviews_body(data_size, reviews):
    polarity = get_polarity_scores(reviews[0:data_size])
    print(polarity)
    review_bodys = []
    for x in range(len(polarity)):
        if isNegative(polarity, x):
            review_bodys.append(reviews[x])
    return review_bodys

