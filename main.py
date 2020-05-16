from dbscan import perform_db_scan
from database_access import DatabaseAccess
from plotter import plot_cluster
from extracter_analyzer import *
from preprocessor import *
import os


def split_sentences(reviews):
    sentences = []
    for review in reviews:
        for sentence in split_into_sentences(review):
            sentences.append(sentence)
    return sentences


def get_reviews():
    db_file = r"amazon_reviews_us_Jewelry_v1_00.db"
    db_file = os.getcwd() + '\data\\' + db_file

    db = DatabaseAccess(db_file)
    return db.retrive_reviews(star_rating=2)


def isNegative(polarity, x):
    return polarity["compound"][x] < 0.2 and polarity["neu"][x] < 0.9 and polarity["neg"][x] > 0.1


def polarize_reviews_body(data_size, reviews):
    polarity = get_polarity_scores(reviews["review_body"][0:data_size])
    print(polarity)
    review_bodys = []
    for x in range(len(polarity)):
        if isNegative(polarity, x):
            review_bodys.append(reviews["review_body"][x])
    return review_bodys
"""


def polarize_reviews_body(data_size, reviews):
    polarity = get_polarity_scores(reviews[0:data_size])
    print(polarity)
    review_bodys = []
    for x in range(len(polarity)):
        if isNegative(polarity, x):
            review_bodys.append(reviews[x])
    return review_bodys
"""


def perform_tf_idf_and_print(min_df=0.05, max_df=0.9):
    print("\n<----- Tf Idf Starts ----->")
    tf_idf_review_bodys = get_tfidf(
        [str(sen) for sen in review_bodys], min_df=min_df, max_df=max_df)
    print(tf_idf_review_bodys)
    return tf_idf_review_bodys


def perform_db_scan_and_print(data, review_bodys, min_samples_val, eps_val):
    print("\n<----- Db Scan Starts ----->")
    dbres = perform_db_scan(data, min_samples_val, eps_val)
    plot_cluster(dbres, data)

    print(dbres.labels_)
    for i in set(dbres.labels_):
        print(i, "----")
        for x in range(len(data)):
            if dbres.labels_[x] == i and i != -1:
                print(review_bodys[x], " ")


# get reviews
data_frame = get_reviews()
"""
# split into sentences
sentences = split_sentences(data_frame["review_body"])
[print("---- " , sentence) for sentence in sentences[0:100]]

print("\n\n")

"""
# polarize reviews body
review_bodys = polarize_reviews_body(2000, data_frame)

data_frame = None
print("Row number after polarity score: ", len(review_bodys))

# clear reviews body
review_bodys = clear_doc(review_bodys)
print(review_bodys)

# get top words from reviews body
find_top_words(review_bodys, 5)

# tf-idf
tf_idf_review_bodys = perform_tf_idf_and_print(min_df=1, max_df=0.8)

# db scan
perform_db_scan_and_print(tf_idf_review_bodys, review_bodys, 5, 0.9)


"""
print("\n<----- HDb Scan Starts ----->")
print(HDbScan.performDbScan(data))

print(review_bodys)

# get top words from review head
find_top_words(review_heads, 5)
find_top_words(data_frame["review_head"], 5)

# get top words from review body
find_top_words(review_bodys, 5)
find_top_words(data_frame["review_body"], 5)

# find nouns in reviews
for review in data_frame["review_body"]:
    print("REVIEW >>> " + review)
    find_nouns(review)
    find_defs(review)

ngrams = get_ngrams('this is a foo bar sentences and i want to ngramize it', 4)
print(ngrams)

count_vectorizer_review_bodys = get_count_vectorizer([str(sen) for sen in review_bodys])

print(count_vectorizer_review_bodys)

plot_k_distance(tf_idf_review_bodys)
"""
