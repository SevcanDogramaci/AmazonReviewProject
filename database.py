from database_access import DatabaseCreator

def parse_tsv_file(file):
    lines = []

    try:
        with open(file, 'r', encoding='utf-8') as reader:
            # skip column info line
            next(reader)

            for line in reader:
                line = line.split("\t")
                lines.append(line)
    except Exception as e:
        print(e)

    return lines


def parse_json_file(file):
    import json
    jsons = []

    try:
        with open(file, 'r', encoding='utf-8') as reader:
            for line in reader:
                line = json.loads(line)
                jsons.append(line)
    except Exception as e:
        print(e)

    return jsons


db_file = r"amazon_reviews_us_Watches_v1_00.db"
tsv_file = r"./data/amazon_reviews_us_Watches_v1_00.tsv"
json_review_file = "sample_review_json.json"
json_product_file = "sample_product_json.json"

# create tables
db_creator = DatabaseCreator(db_file)
db_creator.create_table("Product", db_creator.product_columns)
db_creator.create_table("Review", db_creator.review_columns)

# get data
reviews = parse_tsv_file(tsv_file)

with db_creator.conn:
    # insert data
    for review in reviews:
        product_info = (review[3], review[5], review[6])
        review_info = (review[0], review[1], review[3],
                       review[7], review[8], review[11], review[12],
                       review[13], review[14].split("\n")[0])
        # insert product
        db_creator.insert_product(product_info)
        # insert review
        db_creator.insert_review(review_info)