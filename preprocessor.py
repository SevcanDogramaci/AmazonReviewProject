from database_access import DatabaseAccess
import pandas as pd


class Preprocessor:

    def split_sentences(self, reviews):
        sentences = []
        for review in reviews:
            for sentence in self.__split_into_sentences(review):
                sentences.append(sentence)
        return sentences

    def split_review_into_sentences(self, review):
        sentences = []
        for sentence in self.__split_into_sentences(review):
            sentences.append(sentence)
        return sentences


    def __split_into_sentences(self, text):
        import re
        alphabets = "([A-Za-z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"

        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(websites, "<prd>\\1", text)
        if "Ph.D" in text:
            text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
        text = re.sub(acronyms+" "+starters, "\\1<stop> \\2", text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" +
                      alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(alphabets + "[.]" + alphabets +
                      "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" "+suffixes+"[.] "+starters, " \\1<stop> \\2", text)
        text = re.sub(" "+suffixes+"[.]", " \\1<prd>", text)
        text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
        if "”" in text:
            text = text.replace(".”", "”.")
        if "\"" in text:
            text = text.replace(".\"", "\".")
        if "!" in text:
            text = text.replace("!\"", "\"!")
        if "?" in text:
            text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    def __get_wordnet_pos(self, pos_tag):
        from nltk.corpus import wordnet

        if pos_tag.startswith('J'):
            return wordnet.ADJ
        elif pos_tag.startswith('V'):
            return wordnet.VERB
        elif pos_tag.startswith('N'):
            return wordnet.NOUN
        elif pos_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def __clear_sentence(self, text):
        from nltk.stem import WordNetLemmatizer
        from nltk.corpus import wordnet
        from nltk.corpus import stopwords
        from nltk import pos_tag
        import string
        import nltk

        # convert to lower case
        text = text.lower()

        # tokenize text
        words = set(nltk.corpus.words.words())

        text = " ".join(w for w in nltk.wordpunct_tokenize(text)
                        if w.lower() in words)

        text = nltk.word_tokenize(text)

        # part-of-speech tagging
        pos_tags = pos_tag(text)

        # stemming
        lemmatizer = WordNetLemmatizer()
        text = [lemmatizer.lemmatize(tag[0], self.__get_wordnet_pos(
            tag[1])) for tag in pos_tags if tag[1].startswith('N')]

        # remove stopwords
        stopwords_en = stopwords.words('english')
        text = [word for word in text if word not in stopwords_en]

        # remove punctuation
        text = [word.strip(string.punctuation) for word in text]

        # remove numbers
        text = [word for word in text if not any(
            letter.isdigit() for letter in word)]

        # remove empty and one-letter words
        text = [word for word in text if len(word) > 1]

        return " ".join(text)

    # iterates through reviews and returns processed review array.
    def clear_doc(self, doc):
        clean_doc = []

        for sentence in doc:
            clean_sentence = self.__clear_sentence(sentence)
            # eliminate short or empty strings.
            if len(clean_sentence) > 2:
                clean_doc.append(clean_sentence)

        return clean_doc

    def clear_reviews(self, reviews, data_size):
        from extracter_analyzer import get_polarity, isNegative

        clean_doc = []

        for i in range(0, len(reviews)):
            if len(clean_doc) >= data_size:
                break
            review = reviews[i]
            sentence_idx = 0
            for sentence in self.__split_into_sentences(review):
                polarity = get_polarity(sentence)

                if isNegative(polarity):

                    clean_sentence = self.__clear_sentence(sentence)

                    # eliminate short or empty strings.
                    if len(clean_sentence) > 2:
                        clean_doc.append((clean_sentence, i, sentence_idx))
                        
                        print("Original Sentence: ", sentence)
                        print("Preprocessed Sentence: ", clean_sentence)

                sentence_idx += 1

        return clean_doc
