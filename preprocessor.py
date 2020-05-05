from database import*
import pandas as pd
    
db_file = r"amazon_reviews_us_shoes_v1_00_2015_top10000.db"

def get_wordnet_pos(pos_tag):
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
    
def clear_text(text):
    from nltk.corpus import wordnet
    from nltk import pos_tag
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
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
    text = [lemmatizer.lemmatize(tag[0], get_wordnet_pos(tag[1])) for tag in pos_tags]
    #text = [lemmatizer.lemmatize(tag[0], get_wordnet_pos(tag[1])) for tag in pos_tags if tag[1] is wordnet.NOUN]
    #text = [lemmatizer.lemmatize(tag[0], get_wordnet_pos(tag[1])) for tag in pos_tags if tag[1].startswith('N')]
    
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

def main():
    import os
    db_conn = create_connection(os.getcwd() + '\data\\' + db_file)

    # get reviews
    sql_select_all_reviews  = "SELECT * FROM Review"
    reviews = execute_sql_query(db_conn, sql_select_all_reviews)

    # form data frame of reviews for manipulation
    data_frame = pd.DataFrame(reviews)
    data_frame.columns = ['review_id', 'marketplace', 'customer_id', 'product_id', 'rate', 
                        'helpful_votes', 'purchased', 'review_head', 'review_body', 'date']

    # clean reviews
    data_frame['review_head'] = [clear_text(text) for text in data_frame['review_head']]
    data_frame['review_body'] = [clear_text(text) for text in data_frame['review_body']]

    print(data_frame['review_head'])

    print(data_frame['review_body'])


if __name__ == '__main__':
    main()

