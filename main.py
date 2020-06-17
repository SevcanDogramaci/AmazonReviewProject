from database_access import DatabaseAccess
from preprocessor import Preprocessor
from extracter_analyzer import *
from plotter import Plotter
from dbscan import DbScan
import os


def get_reviews():
    db_file = r"amazon_reviews_us_Watches_v1_00_2015_top10000.db"
    db_file = os.getcwd() + '\data\\' + db_file

    db = DatabaseAccess(db_file)
    return db.retrive_reviews()


def perform_tf_idf_and_print(min_df=0.05, max_df=0.9):
    print("\n<----- Tf Idf Starts ----->")
    tf_idf_review_bodys = get_tfidf(
        [sen[0] for sen in cleaned_review_bodys], min_df=min_df, max_df=max_df)

    # print results
    print(tf_idf_review_bodys)
    return tf_idf_review_bodys


def perform_db_scan_and_print(data, original_data, review_bodys, min_samples_val, eps_val, dataset_name):
    from collections import Counter

    print("\n<----- Db Scan Starts ----->")

    dbscan = DbScan()
    dbres = dbscan.perform_db_scan(
        data, min_samples_val, eps_val)  # inside dbscan.py

    plotter = Plotter()
    title = dataset_name + " - eps: " + \
        str(eps_val) + ", min_samples: " + str(min_samples_val)
    plotter.plot_cluster(dbres, data, title)  # inside plotter.py

    labels = dbres.labels_
    # print number of elements in each cluster
    clusters = Counter(labels)
    print(clusters)

    # find and print dbscan result on actual text data - review_bodys
    for i in set(labels):
        if i != -1:  # do not print if noise (-1)
            print(i, "----")
            for x in range(len(data)):
                if labels[x] == i:
                    print(">>>", (review_bodys[x]))
                    #original_review_id = (review_bodys[x])[1]
                    #print(original_data[original_review_id])

# --- MAIN Starts


# initializations
dataset_name = "SHOES"

# get reviews from database
data_frame = get_reviews()

original_review_bodys = list(data_frame["review_body"])

preproc = Preprocessor()

# split into sentences
#review_bodys = preproc.split_sentences(reviews=review_bodys)

# filter reviews according to sentiment analysis results
# original_review_bodys = polarize_reviews_body(200, review_bodys)
# print("Row number after polarity score: ", len(review_bodys))

data_frame = None  # to free memory space

# clear reviews body with preprocessing, inside preprocessing.py
cleaned_review_bodys = preproc.clear_reviews(
    original_review_bodys, data_size=1000)

print(cleaned_review_bodys)

# get top words from reviews body, inside preprocessing.py
#find_top_words(review_bodys, 5)

# tf-idf
tf_idf_review_bodys = perform_tf_idf_and_print(min_df=1, max_df=0.8)

#plotter = Plotter()
#eps = plotter.plot_k_distance(tf_idf_review_bodys, k=2)

# db scan with min_samples and eps (eps observed from k-distance graph)
perform_db_scan_and_print(
    tf_idf_review_bodys, original_review_bodys, cleaned_review_bodys, 2, 1.0, dataset_name)


# --- MAIN Finishes
