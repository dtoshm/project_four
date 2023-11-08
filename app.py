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
    except IndexError:
        print("** ERROR **")
    else: 
        return return_date


def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
              \n** ID ERROR **
              \rThe ID format should be a number.
              \rPress ENTER to try again.
              \r**************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
              \n** ID ERROR **
              \rOptions: {options}
              \rPress ENTER to try again.
              \r**************''')
            return
        
        
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


def menu():
    while True:
        print('''  
              \nProduct Inventory
              \rV) Display a product by its ID
              \rA) Add Product
              \rB) Backup All Pruducts
              \rE) Exit''')
        choice = input('What would you like to do? ').lower()
        if choice in ['v', 'a', 'b', 'e']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above.
                  \rA number from V, A, B, E.
                  \rPress enter to try again.''')


def app():
    add_csv()
    app_running = True
    while app_running: 
        choice = menu()
        if choice == 'v':
            # search products
            id_options = []
            for product in session.query(Product):
                id_options.append(product.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nID Options: {id_options}
                    \rProduct ID: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.id==id_choice).first()
            print(f'''
                  \nName: {the_product.product_name}
                  \rPrice: ${the_product.product_price / 100}
                  \rQuantity: {the_product.product_quantity}
                  \rDate: {the_product.date_updated}''')
        elif choice == 'a':
            # add products   
            product_name = input("New Product Name: ")
            price_error = True
            while price_error:
                price = input("New Product Price: ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                quantity = input("New Product Quantity: ")
                quantity = clean_quantity(quantity)
                if type(quantity) == int:
                    quantity_error = False
            date_error = True
            while date_error:
                date = input("New Product Date Updated (ex m/d/y): ")
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            new_product = Product(product_name=product_name,
                                product_price=price,
                                product_quantity=quantity,
                                date_updated=date)
            session.add(new_product)
            session.commit()
            print('Book Added!')
            time.sleep(1.5)
        elif choice == 'b':
            print('b')
        else:
            print("Thank you come again!")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
