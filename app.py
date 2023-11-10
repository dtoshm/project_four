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
    """
    Adds data from a CSV file to a database session.

    Args:
    session: A SQLAlchemy database session object.
    """
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


def backup_to_csv():
    """
    Export product data from the database to a CSV file.

    Args:
    session: A SQLAlchemy database session object.
    """
    products = session.query(Product).all()
    if not products:
        print("No products to export.")
        return
    csv_file_path = 'backup.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['product_name', 'product_price', 'product_quantity', 'date_updated']) # Headers
        for product in products:
            csv_writer.writerow([product.product_name, 
                                 product.product_price / 100, 
                                 product.product_quantity, 
                                 product.date_updated])
    print(f"Data has been exported to {csv_file_path}")
    

def menu():
    """
    Display a menu of options for a product inventory program.

    Returns:
    str: The user's choice (V, A, B, or E).
    """
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


def add_product():
    """
    Collects and validates information for a new product from user input.

    This function guides the user to input a new product's name, price, quantity, and date updated. It validates the
    input for each field to ensure it meets the required format and data type. If any input is invalid, the user is
    prompted to re-enter the data until it's correct. Once all information is collected and validated, a new Product
    object is created and added to the database session. The function then commits the changes to the database and
    prints a success message.

    Args:
    None

    Returns:
    Nones
    """
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
        update()
        
    else:
        session.add(new_product)
        session.commit()
        print('Book Added!')
        

def search_products():
    """
    Allow the user to search for and display product details by entering a product ID.

    This function retrieves a list of available product IDs from the database and prompts the user to enter a product ID.
    It validates the input and ensures that it corresponds to an existing product ID. Once a valid product ID is provided,
    it retrieves and displays the details of the corresponding product, including name, price, quantity, and date updated.

    Args:
    None

    Returns:
    None
    """
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



def update():  
    print("needs updating")  



if __name__ == '__main__':
    """
    Main script execution entry point.
    """
    Base.metadata.create_all(engine)
    app()
        