## About the Project

This project aims to extract product defects and opinions from customer reviews by using text clustering and sentiment analysis. The customer review data used in the project are produced from Amazon Customer Reviews Dataset available [here](https://s3.amazonaws.com/amazon-reviews-pds/readme.html). 

For further details, please look at our [paper](https://ieeexplore.ieee.org/document/9377851). Please cite this paper if you want to utilize this project.

## Requirements

→ **Working environment**

Python 3+ (developed with 3.7)

→ **Required libraries**

Available in `requirements.txt`. Install with `pip install -r requirements.txt`.

## **Installation**

You can clone the project by running the following command or download it as a zip file via [GitHub](https://github.com/SevcanDogramaci/AmazonReviewProject).

`git clone https://github.com/SevcanDogramaci/AmazonReviewProject.git`
## Usage

To run the system, you can use either of the files and run :

→ `product_category.ipynb` Jupyter Notebook in the `./test` folder 

→ `main.py` file in the root directory. 

Two different datasets are provided for the test purposes in the `./data` folder. 

You can also download datasets from [here](https://s3.amazonaws.com/amazon-reviews-pds/readme.html) and create database files for these datasets using `database.py` file in the root directory.
