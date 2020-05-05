import sqlite3
from sqlite3 import Error

def parse_tsv_file(file):
    
    lines = []
    
    try:
        with open(file, 'r', encoding='utf-8') as reader:
            # skip column info line
            next(reader)
            
            for line in reader:
                line = line.split("\t")
                lines.append(line)
    except Error as e:
        print(e)
        
    return lines


def parse_json_file (file):
    import json
    jsons = []
    
    try:
        with open(file, 'r', encoding='utf-8') as reader:
            for line in reader:
                line = json.loads(line)
                jsons.append(line)
    except Error as e:
        print(e)
        
    return jsons



def create_connection(db_file):
    
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database!")
    except Error as e:
        print("Cannot connect to database!")
        
    return conn



def create_table(conn, sql_query):
    
    try:
        c = conn.cursor()
        c.execute(sql_query)
        print("Table created!")
    except Error as e:
        print("Table NOT created! - " + str(e))


def execute_sql_query(conn, sql_query):
    try:
        c = conn.cursor()
        c.execute(sql_query)
        result = c.fetchall()
        print("Query executed!")
    except Error as e:
        print("Query NOT executed! - " + str(e))
        
    return result




def insert_product(conn, review_info):
    
    sql_insert_product = """INSERT INTO Product VALUES(?, ?, ?)"""
    
    try:
        cur = conn.cursor()
        cur.execute(sql_insert_product, review_info)
        print("Product inserted!")
    except Error as e:
        print("Product NOT inserted! - " + str(e))



def insert_review(conn, review_info):
    
    sql_insert_review = """INSERT INTO Review(marketplace, customer_id, product_id, 
                                            star_rating, helpful_votes, verified_purchase, 
                                            review_headline, review_body, review_date) 
                                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    try:
        cur = conn.cursor()
        cur.execute(sql_insert_review, review_info)
        print("Review inserted!")
    except Error as e:
        print("Review NOT inserted! - " + str(e))


def main():
    
    db_file = r"amazon_reviews_us_shoes_v1_00.db"
    tsv_file = "amazon_reviews_us_Shoes_v1_00.tsv"
    json_review_file = "sample_review_json.json"
    json_product_file = "sample_product_json.json"

    
    sql_create_product_table = """CREATE TABLE IF NOT EXISTS Product (
                                        product_id text PRIMARY KEY CHECK(length(product_id) = 10),
                                        product_title text NOT NULL,
                                        product_category text NOT NULL
                                    )"""

    sql_create_review_table = """CREATE TABLE IF NOT EXISTS Review (
                                    review_id integer PRIMARY KEY AUTOINCREMENT,
                                    marketplace text NOT NULL DEFAULT 'US' CHECK(length(marketplace) = 2),
                                    customer_id text NOT NULL,
                                    product_id text NOT NULL CHECK(length(product_id) = 10),
                                    star_rating integer NOT NULL DEFAULT 0 CHECK(star_rating < 6),
                                    helpful_votes integer NOT NULL DEFAULT 0,
                                    verified_purchase text NOT NULL CHECK(length(verified_purchase) = 1),
                                    review_headline text NOT NULL,
                                    review_body text NOT NULL,
                                    review_date text NOT NULL,
                                    FOREIGN KEY (product_id) REFERENCES Product (product_id) 
                                )"""
    
    db_conn = create_connection(db_file)
    
    with db_conn:
        # enable foreign keys integrity
        db_conn.execute("PRAGMA foreign_keys = 1")
        
        # create Product table
        create_table(db_conn, sql_create_product_table)

        # create Review table
        create_table(db_conn, sql_create_review_table)
        
        # get data
        reviews = parse_tsv_file(tsv_file)
        """
        json_reviews = parse_json_file(json_review_file)
        json_products = parse_json_file(json_product_file)
        
        #insert json data
        for product in json_products:
            product_info = (product["asin"], product["title"], product["main_cat"])
            insert_product(db_conn, product_info)
            
        #insert json data
        for review in json_reviews:
            from datetime import datetime
            ts = review["unixReviewTime"]
            review_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
            
            if(review["verified"]):
                verified = 'Y'
            else:
                verified = 'N'
                
            try:
                review_vote = review[vote]
            except:
                review_vote = 0
                
            review_info = ("US",review["reviewerID"],review["asin"], 
                           review["overall"], review_vote, verified, 
                           review["summary"], review["reviewText"], review_date)
            insert_review(db_conn, review_info)
        
        """
        # insert data
        for review in reviews:
            product_info = (review[3], review[5], review[6])
            review_info = (review[0], review[1], review[3], 
                           review[7], review[8], review[11], review[12], 
                           review[13], review[14].split("\n")[0])
            # insert product
            insert_product(db_conn, product_info)
            # insert review
            insert_review(db_conn, review_info)


if __name__ == '__main__':
    main() 

