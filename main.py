import pandas as pd
from sklearn.decomposition import NMF
from extracter_analyzer import ExtracterAnalyzer
from database_access import DatabaseAccess
from preprocessor import Preprocessor
import os

db_file = r"amazon_reviews_us_shoes_v1_00_2015_top10000.db"
db_file = os.getcwd() + '\data\\' + db_file

db = DatabaseAccess(db_file)
data_frame = db.retrive_reviews()

review_bodys = Preprocessor.clear_doc(data_frame["review_body"][0:100])
review_heads = Preprocessor.clear_doc(data_frame["review_head"][0:100])

# get top words from review head
ExtracterAnalyzer.find_top_words(review_heads, 5)

# get top words from review body
ExtracterAnalyzer.find_top_words(review_bodys, 5)

# find nouns in reviews
for review in data_frame["review_body"]:
    print("REVIEW >>> " + review)
    ExtracterAnalyzer.find_nouns(review)
    ExtracterAnalyzer.find_defs(review)

ngrams = ExtracterAnalyzer.get_ngrams('this is a foo bar sentences and i want to ngramize it', 4)

print(ExtracterAnalyzer.get_tfidf([str(sen) for sen in review_bodys]))
print(ExtracterAnalyzer.get_count_vectorizer([str(sen) for sen in review_bodys]))

#dataFrame = get_polarity_scores(data_frame["review_body"])
# print(dataFrame.mean())
# print(dataFrame)
