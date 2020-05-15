import sqlite3
from sqlite3 import Error
import pandas as pd


class DatabaseAccess:
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            self.conn = sqlite3.connect(file_name)
            print("Connected to database!")
        except Error as e:
            print("Cannot connect to database!")

    def __execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def retrive_reviews(self, product_id=None, star_rating=6):
        if product_id is None:
            ret = self.__execute_query(
                "SELECT * FROM Review WHERE star_rating < 2")
        else:
            ret = self.__execute_query(
                "SELECT * FROM Review WHERE product_id=", product_id, " AND star_rating < ", star_rating)
        data = pd.DataFrame(ret)
        data.columns = ['review_id', 'marketplace', 'customer_id', 'product_id', 'rate',
                        'helpful_votes', 'purchased', 'review_head', 'review_body', 'date']

        return data

    def retrive_reviews_with_products(self):
        ret = self.__execute_query(
            "SELECT * FROM Review INNER JOIN Product ON Review.product_id = Product.product_id")

        data = pd.DataFrame(ret)
        data.columns = ['review_id', 'marketplace', 'customer_id', 'product_id', 'rate',
                        'helpful_votes', 'purchased', 'review_head', 'review_body', 'date'
                        'product_id', 'product_title', 'product_category']

        return data

    def retrive_products(self):
        data = pd.DataFrame(self.__execute_query("SELECT * FROM Product"))
        data.columns = ['product_id', 'product_title', 'product_category']

        return data

    def retrive_products_top_n(self, n):
        data = pd.DataFrame(self.__execute_query(
            "SELECT * FROM Product LIMIT " + str(n)))
        data.columns = ['product_id', 'product_title', 'product_category']

        return data

    def retrive_reviews_top_n(self, n):
        ret = self.__execute_query("SELECT * FROM Review LIMIT " + n)
        data = pd.DataFrame(ret)
        data.columns = ['review_id', 'marketplace', 'customer_id', 'product_id', 'rate',
                        'helpful_votes', 'purchased', 'review_head', 'review_body', 'date']

        return data

    def retrive_reviews_with_products_top_n(self, n):
        ret = self.__execute_query(
            "SELECT * FROM Review INNER JOIN Product ON Review.product_id = Product.product_id LIMIT " + str(n))

        data = pd.DataFrame(ret)
        data.columns = ['review_id', 'marketplace', 'customer_id', 'product_id', 'rate',
                        'helpful_votes', 'purchased', 'review_head', 'review_body', 'date',
                        'product_id', 'product_title', 'product_category']

        return data

    def retrieve_top_worst_products(self, n=10, star_rating=3):
        ret = self.__execute_query(
            "SELECT product_id, COUNT(*) as count FROM Review GROUP BY product_id HAVING star_rating < ", star_rating, "ORDER BY count DESC")
        data = pd.DataFrame(ret)
        data.columns = ['product_id', 'count']

        return data


class DatabaseCreator:
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name

        try:
            self.conn = sqlite3.connect(db_file_name)
            print("Connected to database!")
        except Error as e:
            print("Cannot connect to database!")

        self.review_columns = """ (
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
        self.product_columns = """ (
                                        product_id text PRIMARY KEY CHECK(length(product_id) = 10),
                                        product_title text NOT NULL,
                                        product_category text NOT NULL
                                    )"""

    def __execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)

    def __execute_insert(self, query, values):
        cur = self.conn.cursor()
        cur.execute(query, values)

    def create_table(self, table_name, columns):
        self.__execute_query("PRAGMA foreign_keys = 1")
        try:
            self.__execute_query(
                "CREATE TABLE IF NOT EXISTS " + table_name + columns)
            print("Table CREATED: " + table_name)
        except Error as e:
            print("Table NOT CREATED: " + table_name + " " + str(e))

    def insert_review(self, values):
        sql_insert_review = """INSERT INTO Review(marketplace, customer_id, product_id, 
                                            star_rating, helpful_votes, verified_purchase, 
                                            review_headline, review_body, review_date) 
                                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        try:
            self.__execute_insert(sql_insert_review, values)
            print("Review inserted!")
        except Error as e:
            print("Review NOT inserted! - " + str(e))

    def insert_product(self, values):
        sql_insert_product = """INSERT INTO Product VALUES(?, ?, ?)"""

        try:
            self.__execute_insert(sql_insert_product, values)
            print("Product inserted!")
        except Error as e:
            print("Product NOT inserted! - " + str(e))
