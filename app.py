from models import (Base, session,
                    Product, engine)
import datetime
import csv
import time


def clean_price(price_str):
    try:
        cleaned_price = float(price_str.replace('$', ''))
    except ValueError:
        print('** ERROR **')
    else:
        return int(cleaned_price * 100)


def clean_quantity(quantity_str):
    try:
        cleaned_quantity = int(quantity_str)
    except ValueError:
        print('** ERROR **')
    else:
        return int(cleaned_quantity)


def add_csv():
    with open('inventory.csv') as csvfile:
        data=csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = clean_quantity(row[2])
  
        #         date_updated = row[3]
        #         new_product = Product(product_name=product_name,
        #                               product_price=product_price,
        #                               product_quantity=product_quantity,
        #                               date_updated=date_updated)
        #         session.add(new_product)
        # session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
