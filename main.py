from extracter_analyzer import ExtracterAnalyzer
from database_access import DatabaseAccess
from preprocessor import Preprocessor
from dbscan import DbScan, HDbScan
import os

def plot_k_distance(data):
    import numpy as np
    from sklearn.datasets.samples_generator import make_blobs
    from sklearn.neighbors import NearestNeighbors
    from matplotlib import pyplot as plt
    import seaborn as sns
    sns.set()
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(data)
    distances, indices = nbrs.kneighbors(data)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    plt.plot(distances)

def plot_cluster(cluster, sample_matrix):
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    import numpy as np

    sample_matrix = StandardScaler().fit_transform(sample_matrix)
    core_samples_mask = np.zeros_like(cluster.labels_, dtype=bool)
    core_samples_mask[cluster.core_sample_indices_] = True
    labels = cluster.labels_

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)  # generator comprehension 
        # X is your data matrix
        X = np.array(sample_matrix)

        xy = X[class_member_mask & core_samples_mask]

        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)
   
    #plt.savefig('cluster.png')
    
def printDbScan(data, review_bodys):
    print("\n<----- Db Scan Starts ----->")
    dbres = DbScan.performDbScan(data, 5, 0.9)
    plot_cluster(dbres, data)
    
    """
    print(dbres)
    for i in set(dbres):
        print(i, "----")
        for x in range(len(data)):
            if dbres[x] == i and i != -1:
                print(review_bodys[x] , " ")
    """
                
    #print("\n<----- HDb Scan Starts ----->")
    #print(HDbScan.performDbScan(data))

db_file = r"amazon_reviews_us_shoes_v1_00_2015_top10000.db"
db_file = os.getcwd() + '\data\\' + db_file

db = DatabaseAccess(db_file)
data_frame = db.retrive_reviews()

review_bodys = Preprocessor.clear_doc(data_frame["review_body"][0:1000])
review_heads = Preprocessor.clear_doc(data_frame["review_head"][0:1000])

print(review_bodys)

# get top words from review head
ExtracterAnalyzer.find_top_words(review_heads, 5)
#ExtracterAnalyzer.find_top_words(data_frame["review_head"], 5)

# get top words from review body
ExtracterAnalyzer.find_top_words(review_bodys, 5)
#ExtracterAnalyzer.find_top_words(data_frame["review_body"], 5)

"""
# find nouns in reviews
for review in data_frame["review_body"]:
    print("REVIEW >>> " + review)
    ExtracterAnalyzer.find_nouns(review)
    ExtracterAnalyzer.find_defs(review)
"""

#ngrams = ExtracterAnalyzer.get_ngrams('this is a foo bar sentences and i want to ngramize it', 4)
#print(ngrams)

print("\n<----- Tf Idf Starts ----->")
tf_idf_review_bodys = ExtracterAnalyzer.get_tfidf([str(sen) for sen in review_bodys])
count_vectorizer_review_bodys = ExtracterAnalyzer.get_count_vectorizer([str(sen) for sen in review_bodys])
print(tf_idf_review_bodys)
print(count_vectorizer_review_bodys)

#dataFrame = get_polarity_scores(data_frame["review_body"])
# print(dataFrame.mean())
# print(dataFrame)

printDbScan(tf_idf_review_bodys, review_bodys)