from models import (Base, session,
                    Product, engine)
import datetime
import csv
import time


# def add_csv():
#     with open('suggested_books.csv') as csvfile:
#         data=csv.rater(csvfile)
#         for row in data:
#             item_in_db = session.query()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
