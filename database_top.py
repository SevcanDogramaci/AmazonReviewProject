import sqlite3
from sqlite3 import Error


db_file_to_open = r"amazon_reviews_us_shoes_v1_00.db"
db_file_to_save = r"amazon_reviews_us_shoes_v1_00_2015_top10000.db"


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
    result = None

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
    
db_conn = create_connection(db_file_to_open)

reviews = []
with db_conn:
    # get data
    reviews = execute_sql_query(db_conn, "SELECT * FROM Review INNER JOIN Product on Product.product_id = Review.product_id WHERE substr(review_date,1,4) = '2015' LIMIT 10000")

db_conn = create_connection(db_file_to_save)

with db_conn:
    # enable foreign keys integrity
    db_conn.execute("PRAGMA foreign_keys = 1")
    #execute_sql_query(db_conn, "DROP TABLE IF EXISTS Review")
    #execute_sql_query(db_conn, "DROP TABLE IF EXISTS Product")

    # create Product table
    create_table(db_conn, sql_create_product_table)

    # create Review table
    create_table(db_conn, sql_create_review_table)

    # insert data
    for review in reviews:
        product_info = (review[10], review[11], review[12])
        review_info = (review[1], review[2], 
                        review[3], review[4], review[5], review[6], 
                        review[7], review[8], review[9])
        # insert product
        insert_product(db_conn, product_info)
        # insert review
        insert_review(db_conn, review_info)