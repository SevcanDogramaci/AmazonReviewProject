from database_access import DatabaseAccess, DatabaseCreator
import os

db_file_to_open = r"amazon_reviews_us_shoes_v1_00.db"
db_file_to_open = os.getcwd() + '\data\\' + db_file_to_open
db_file_to_save = r"amazon_reviews_us_shoes_v1_00_2015_top10000_bad.db"

db_access = DatabaseAccess(db_file_to_open)
reviews = db_access.retrive_reviews_with_products_top_n(10000)

db_creator = DatabaseCreator(db_file_to_save)
db_creator.create_table("Product", db_creator.product_columns)
db_creator.create_table("Review", db_creator.review_columns)

with db_creator.conn:
    # insert data
    for index, review in reviews.iterrows():
        product_info = (review[10], review[11], review[12])
        review_info = (review[1], review[2], review[3],
                       review[4], review[5], review[6],
                       review[7], review[8], review[9])
        # insert product
        db_creator.insert_product(product_info)
        # insert review
        db_creator.insert_review(review_info)
