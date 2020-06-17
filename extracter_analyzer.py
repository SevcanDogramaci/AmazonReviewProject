from re import search
from nltk import pos_tag
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


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

# --------------------------------------------------------------------

"""
str = "DONT BUY THESE!	Do not buy these! They break very fast I spun then for 15 minutes " + \
    "and the end flew off don't waste your money." + "They are made from cheap plastic and" + \
    " have cracks in them. Buy the poi balls they work a lot better if you only have limited funds."
#str = "It comes with a rechargeable battery that does not seem to last all that long, especially if you use the flash a lot."
#str = "After nearly 800 pictures I have found that this camera takes incredible pictures"
#str = "The strap is horrible and gets in the way of parts the camera you need access to."
"""

def find_matched_phrases(phrases, patterns):
    for pattern in patterns:
        for chunk in phrases:
            if search(pattern, chunk[1]) is not None:
                print("Pattern is ", pattern)
                print("Ngram: ", chunk[0])
                print("Postags: ", chunk[1])
                print("Opinion word: ", search_opinion_word(
                    chunk[0], chunk[1]))
                print()


def search_opinion_word(phrase, postag):
    postag = postag[:-1].split(";")
    tag_id = None

    for tag in postag:
        if tag == "JJ":
            tag_id = postag.index(tag)
            break
        elif tag == "RB" or tag == "RBR" or tag == "RBS":
            tag_id = postag.index(tag)

    return phrase[tag_id]


def get_words_and_postags(ngrams):
    words_and_postags = []
    for ngram in ngrams:
        ngram = pos_tag(ngram)
        words = []
        postags = ""

        for item in ngram:
            words.append(item[0])
            postags += (item[1] + ";")
        words_and_postags.append((words, postags))

    return (words_and_postags)


three_element_patterns = ["JJ;(NN|NNS);(NN|NNS);",
                          "NN;VBZ;JJ;",             # added for test
                          "(RB|RBR|RBS);(JJ|RB|RBR|RBS);JJ;",
                          "(RB|RBR|RBS);(JJ|RB|RBR|RBS);(NN|NNS);"]
two_element_patterns = ["JJ;(NN|NNS);",
                        "(RB|RBR|RBS);JJ;",
                        "(VBN|VBD);(NN|NNS);",
                        "(RB|RBR|RBS);(VBN|VBD);",
                        "(VBN|VBD);(RB|RBR|RBS);"]
"""
two_element_ngrams = get_ngrams(str, 2)
three_element_ngrams = get_ngrams(str, 3)

find_matched_phrases(get_words_and_postags(
    two_element_ngrams), two_element_patterns)
print(">> ---- <<")
find_matched_phrases(get_words_and_postags(
    three_element_ngrams), three_element_patterns)
"""