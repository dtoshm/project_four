from models import (Base, session,
                    Product, engine)
import datetime
import csv
import time


def clean_price(price_str):
    """
    Cleans a price string by removing the dollar sign, converting it to a float,
    and returning an integer.

    Args:
    price_str (str): A string representing a price with a dollar sign.

    Returns:
    int: The cleaned price in cents.
    """
    try:
        cleaned_price = float(price_str.replace('$', ''))
    except ValueError:
        print('\n****** PRICE ERROR ******')
        print('Please enter a price (ex 5.99)')
    else:
        return int(cleaned_price * 100)


def clean_quantity(quantity_str):
    """
    Cleans a quantity string by converting it to an integer.

    Args:
    quantity_str (str): A string representing a quantity.

    Returns:
    int: The cleaned quantity as an integer.
    """
    try:
        cleaned_quantity = int(quantity_str)
    except ValueError:
        print('\n****** QUANTITY ERROR ******')
        print('Please enter a quantity (ex 5)')
    else:
        return int(cleaned_quantity)


def clean_date(date_str):
    """
    Cleans a date string in the format 'MM/DD/YYYY' and returns a datetime.date object.

    Args:
    date_str (str): A string representing a date in the 'MM/DD/YYYY' format.

    Returns:
    datetime.date: The cleaned date as a datetime.date object.
    """
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except (ValueError, IndexError):
        print('\n****** DATE ERROR ******')
        print('Please enter a date (ex 04/08/2021)')
    else: 
        return return_date


def clean_id(id_str, options):
    """
    Cleans an ID string by converting it to an integer and validating it against a list of options.

    Args:
    id_str (str): A string representing an ID to be cleaned.
    options (list): A list of valid options to compare the cleaned ID against.

    Returns:
    int or None: The cleaned ID if it's valid, or None if an error occurs.
    """
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
              \n****** ID ERROR ******
              \rThe ID format should be a number.
              \rPress ENTER to try again.
              \r************************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
              \n****** ID ERROR ******
              \rOptions: {options}
              \rPress ENTER to try again.
              \r**********************''')
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


def add_product():
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
        date = input("New Product Date Updated (ex 04/08/2021): ")
        date = clean_date(date)
        if type(date) == datetime.date:
            date_error = False
    new_product = Product(product_name=product_name,
                        product_price=price,
                        product_quantity=quantity,
                        date_updated=date)
    
    if session.query(Product).filter(Product.product_name==product_name).first():
        the_product = session.query(Product).filter(Product.product_name==new_product.product_name).first()
        if new_product.date_updated > the_product.date_updated:
            the_product.product_name = new_product.product_name
            the_product.product_price = new_product.product_price
            the_product.product_quantity = new_product.product_quantity
            the_product.date_updated = new_product.date_updated
            session.commit()
            print('Product Updated!')
            time.sleep(1.5)
        elif new_product.date_updated < the_product.date_updated:
            print('Product Entered Older Than Existing Records')
        else:
            print('Product Entered Matches Existing Records')
    else:
        session.add(new_product)
        session.commit()
        print('Product Added!')
        









def app():
    """
    Run a product inventory application.
    """
    add_csv()
    app_running = True
    while app_running: 
        choice = menu()
        if choice == 'v':
            search_products()     
        elif choice == 'a':
            add_product()  
        elif choice == 'b':
            backup_to_csv()
        else:
            print("Thank you come again!")
            app_running = False






if __name__ == '__main__':
    """
    Main script execution entry point.
    """
    Base.metadata.create_all(engine)
    app()
        