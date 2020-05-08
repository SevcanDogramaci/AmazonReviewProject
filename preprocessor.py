from database_access import DatabaseAccess
import pandas as pd

class Preprocessor:
    @staticmethod
    def __get_wordnet_pos(pos_tag):
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
        
    @staticmethod
    def clear_sentence(text):
        from nltk.stem import WordNetLemmatizer
        from nltk.corpus import wordnet
        from nltk.corpus import stopwords
        from nltk import pos_tag
        import string
        import nltk
    
        # convert to lower case
        text = text.lower()

        # tokenize text
        text = nltk.word_tokenize(text)

        # part-of-speech tagging
        pos_tags = pos_tag(text)

        # stemming
        lemmatizer = WordNetLemmatizer()     
        #text = [lemmatizer.lemmatize(tag[0], Preprocessor.__get_wordnet_pos(tag[1])) for tag in pos_tags]
        #text = [lemmatizer.lemmatize(tag[0], Preprocessor.__get_wordnet_pos(tag[1])) for tag in pos_tags if tag[1] is wordnet.NOUN]
        text = [lemmatizer.lemmatize(tag[0], Preprocessor.__get_wordnet_pos(tag[1])) for tag in pos_tags if tag[1].startswith('N')]

        # remove stopwords
        stopwords_en = stopwords.words('english')
        text = [word for word in text if word not in stopwords_en]

        # remove punctuation
        text = [word.strip(string.punctuation) for word in text]

        # remove numbers
        text = [word for word in text if not any(letter.isdigit() for letter in word)]

        # remove empty and one-letter words
        text = [word for word in text if len(word) > 1]

        return " ".join(text)
    
    @staticmethod
    def clear_doc(doc):
        clean_doc = []

        for sentence in doc:
            clean_sentence = Preprocessor.clear_sentence(sentence)
            if len(clean_sentence) > 2:
                clean_doc.append(clean_sentence)

        return clean_doc