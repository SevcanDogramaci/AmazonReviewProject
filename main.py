from pattern_matcher import PatternMatcher
from database_access import DatabaseAccess
from preprocessor import Preprocessor
from extracter_analyzer import *
from plotter import Plotter
from dbscan import DbScan

from collections import Counter
import os


def get_reviews():
    db_file = r"amazon_reviews_us_kindle.db"
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


def perform_db_scan(data, min_samples_val, eps_val):
    print("\n<----- Db Scan Starts ----->")

    dbscan = DbScan()
    dbres = dbscan.perform_db_scan(
        data, min_samples_val, eps_val)

    return dbres


def plot_db_scan(dbres, data, min_samples_val, eps_val, dataset_name):
    plotter = Plotter()
    title = dataset_name + " - eps: " + \
        str(eps_val) + ", min_samples: " + str(min_samples_val)
    plotter.plot_cluster(dbres, data, title)


def extract_results(labels, original_data, review_bodys):
    # print number of elements in each cluster
    cluster_counts = Counter(labels)
    print(cluster_counts)

    clusters = {}
    pattern_matcher = PatternMatcher()
    # find and print dbscan result on actual text data - review_bodys
    for i in set(labels):
        if i != -1:  # do not print if noise (-1)
            clusters[i] = []
            print(i, "----")
            for x in range(len(review_bodys)):
                if labels[x] == i:

                    print(">>>", (review_bodys[x]))

                    sentence = get_review(review_bodys[x])
                    matches = pattern_matcher.find_matches(sentence)
                    clusters[i].append((review_bodys[x][0], sentence, matches))

                    print(clusters[i], "\n")
    print(clusters)  
    input()
    return pattern_matcher.extract_objects(clusters)

def stringify_results(objects):

    objects_text = ""
    adjectives_text = ""

    for obj in objects:
        for key in obj.keys():
            if not (key in objects_text):
                objects_text += " " + key
        for value in obj.values():
            for val in value:
                opinion,_,_,_ = val
                if opinion is not None and not (opinion in adjectives_text):
                    adjectives_text += " " + opinion
    return objects_text, adjectives_text

def plot_wordcloud(text):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                min_font_size = 8).generate(text) 

    # plot the WordCloud image                        
    plt.figure(figsize = (5, 5), facecolor = None) 
    plt.imshow(wordcloud, interpolation='bilinear') 
    plt.axis("off") 

    plt.show() 
            
def get_review(sentence_tuple):
    review = preproc.split_review_into_sentences(
        original_review_bodys[sentence_tuple[1]])
    return review[sentence_tuple[2]]

def write_to_excel(objects_opinions):
    import xlwt 
    from xlwt import Workbook 
      
    # Workbook is created 
    wb = Workbook() 
      
    # add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet('Sheet 1') 
      
    
    row = 0
    
    for cluster_id, object_op in enumerate(objects_opinions):
    
        for ob, ops in object_op.items():
            
            if len(ops) < 1:
                sheet1.write(row, 0, cluster_id)
                sheet1.write(row, 1, ob)
                row += 1
                continue
                
            for op in ops:
                sheet1.write(row, 0, cluster_id)
                sheet1.write(row, 1, ob)
                if(op[0] is not None):
                    sheet1.write(row,2, op[0].lower())
                else:
                    sheet1.write(row,2, '-')    
                sheet1.write(row,3, op[1]['pos'])
                sheet1.write(row,4, op[1]['neg'])
                sheet1.write(row,5, op[1]['compound'])
                sheet1.write(row,6, op[1]['neu'])
                sheet1.write(row,7, op[2])
                sheet1.write(row,8, op[3])
                row += 1
      
    wb.save('xlwt example4.xls') 

# --- MAIN Starts


# initializations
dataset_name = "KINDLE"

# get reviews from database
data_frame = get_reviews()

original_review_bodys = list(data_frame["review_body"])

preproc = Preprocessor()

# split into sentences
#review_bodys = preproc.split_sentences(reviews=review_bodys)

data_frame = None  # to free memory space

# clear reviews body with preprocessing, inside preprocessing.py
cleaned_review_bodys = preproc.clear_reviews(
    original_review_bodys, data_size=700)

print("Total number of sentences: ", len(cleaned_review_bodys))
print("Total number of reviews left: ", len(
    set([review_idx for _, review_idx, _ in cleaned_review_bodys])))

input("\n\n Enter To Continue")
# get top words from reviews body, inside preprocessing.py
#find_top_words(review_bodys, 5)

# tf-idf
tf_idf_review_bodys = perform_tf_idf_and_print(min_df=1, max_df=0.8)

#plotter = Plotter()
#eps = plotter.plot_k_distance(tf_idf_review_bodys, k=2)

# db scan with min_samples and eps (eps observed from k-distance graph)
min_samples_val = 6
eps_val = 0.9
db_res = perform_db_scan(tf_idf_review_bodys, min_samples_val, eps_val)
plot_db_scan(db_res, tf_idf_review_bodys, min_samples_val, eps_val, dataset_name)
results = extract_results(db_res.labels_, original_review_bodys, cleaned_review_bodys)
print(results)

objects, adjectives= stringify_results(results)

plot_wordcloud(objects) 
plot_wordcloud(adjectives)

write_to_excel(results)

# --- MAIN Finishes
