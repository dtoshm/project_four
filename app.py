from models import (Base, session,
                    Product, engine)
import datetime
import csv
import time


def add_csv():
    with open('inventory.csv') as csvfile:
        data=csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                print(row)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
