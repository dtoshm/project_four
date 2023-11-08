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


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        print("** ERROR **")
    else: 
        return return_date


def add_csv():
    with open('inventory.csv') as csvfile:
        data=csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = clean_quantity(row[2])
                date_updated = clean_date(row[3])                
                new_product = Product(product_name=product_name,
                                      product_price=product_price,
                                      product_quantity=product_quantity,
                                      date_updated=date_updated)
                session.add(new_product)
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
