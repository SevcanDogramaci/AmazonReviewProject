import pandas as pd
from sklearn.decomposition import NMF
from preprocessor import Preprocessor
import spacy

nlp = spacy.load("en_core_web_sm")

class ExtracterAnalyzer:
    @staticmethod
    def find_nouns(document):
        document = nlp(document)
        # split to sentences
        for sentence in document.sents:
            sentence = nlp(sentence.text)
            # iterate over nouns in sentence
            for chunk in sentence.noun_chunks:
                print(chunk.text, chunk.root.text,
                      chunk.root.dep_, chunk.root.head.text + "\n")

    @staticmethod
    def find_defs(document):
        document = nlp(document)
        # split to sentences
        for sentence in document.sents:
            sentence = nlp(sentence.text)
            for token in sentence:
                print(token.text, token.dep_, token.head.text,
                      token.head.pos_, [child for child in token.children])

    @staticmethod
    def find_top_words(data, word_num):
        doc = pd.Series(Preprocessor.clear_doc(data))
        top = doc.value_counts().head(word_num).index.tolist() 
        print(str(word_num) + " words : " + str(top))
        return top

    @staticmethod
    def get_polarity_scores(sentences):
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        analyser = SentimentIntensityAnalyzer()

        scores = []

        for sentence in sentences:
            score = analyser.polarity_scores(sentence)
            print(sentence, " :::: ", score)
            scores.append(score)

        return pd.DataFrame(scores)

    @staticmethod
    def get_tfidf(sentences):
        from sklearn.feature_extraction.text import TfidfVectorizer

        tfidf = TfidfVectorizer(ngram_range=(1, 2))
        features = tfidf.fit_transform(sentences)
        nmf = NMF(n_components=4, random_state=1).fit(features)

        for topic_idx, topic in enumerate(nmf.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([tfidf.get_feature_names()[i]
                            for i in topic.argsort()[:-5 - 1:-1]]))
            print()

        return pd.DataFrame(features.todense(), columns=tfidf.get_feature_names())

    @staticmethod
    def get_count_vectorizer(sentences):
        from sklearn.feature_extraction.text import CountVectorizer

        vectorizer = CountVectorizer()
        x = vectorizer.fit_transform(sentences)
        vectorizer.build_analyzer()

        return pd.DataFrame(x.todense(), columns=vectorizer.get_feature_names())

    @staticmethod
    def get_ngrams(sentence, n):
        from nltk import ngrams
        return ngrams(sentence.split(), n)
