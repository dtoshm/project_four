from models import (Base, session,
                    Product, engine)
import datetime
import csv
import time


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
              \rThe ID should be an option below.
              \rOptions: {options}
              \rPress ENTER to try again.
              \r**********************''')
            return


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


def add_csv():
    """
    Reads data from 'inventory.csv', processes each row, and adds products to the database.

    This function opens the 'inventory.csv' file, skips the header row, and iterates through each subsequent row.
    For each row, it extracts the product name, cleans the price, quantity, and date updated using respective
    cleaning functions, and creates a new Product object. The new product is then added to the database using
    the 'add_product' function.

    Args:
    None

    Returns:
    None
    """
    with open('inventory.csv') as csvfile:
        data=csv.reader(csvfile)
        next(data)
        for row in data:
            product_name = row[0]
            product_price = clean_price(row[1])
            product_quantity = clean_quantity(row[2])
            date_updated = clean_date(row[3])                
            new_product = Product(product_name=product_name,
                                    product_price=product_price,
                                    product_quantity=product_quantity,
                                    date_updated=date_updated)
            add_product(new_product)


def backup_to_csv():
    """
    Export product data from the database to a CSV file.

    Args:
    None

    This function retrieves all products from the database and exports their information to a CSV file. If no products
    are present, a message is printed, and the function returns. The exported CSV file includes headers for
    'product_name', 'product_price', 'product_quantity', and 'date_updated'. Date values are reformatted before
    export to the 'MM/DD/YYYY' format. The exported file is named 'backup.csv', and a success message is printed.

    Returns:
    None
    """
    products = session.query(Product).all()
    if not products:
        print("No products to export.")
        return
    csv_file_path = 'backup.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['product_name', 'product_price', 'product_quantity', 'date_updated'])
        for product in products:
            date_str = str(product.date_updated).split('-')
            formatted_date = f'{date_str[1]}/{date_str[2]}/{date_str[0]}'
            csv_writer.writerow([product.product_name, 
                                 str(f'${product.product_price / 100}'), 
                                 str(product.product_quantity), 
                                 formatted_date
                                ])
    time.sleep(1)
    print(f"Data Exported To: {csv_file_path}")

   
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


def add_product(new_product):
    """
    Updates an existing product or adds a new product to the database.

    This function queries the database to check if a product with the same name as 'new_product' already exists.
    If an existing product is found, it compares the date_updated values. If 'new_product' has a newer date, it updates
    the existing product with the new details and prints a message. If 'new_product' has an older or equal date,
    it prints a message indicating that the existing product remains unchanged. If no existing product is found,
    'new_product' is considered a new product, and it is added to the database with a corresponding message.

    Args:
    new_product (Product): The Product object to be added or used for updating.

    Returns:
    None
    """
    existing_product = session.query(Product).filter(Product.product_name==new_product.product_name).first()
    if existing_product:
        if existing_product.date_updated < new_product.date_updated:
            existing_product.product_name = new_product.product_name
            existing_product.product_price = new_product.product_price
            existing_product.product_quantity = new_product.product_quantity
            existing_product.date_updated = new_product.date_updated
            session.commit()
    else:
        session.add(new_product)
        session.commit()
    

def user_entered_product():
    """
    Collects and validates user input to create a new Product object.

    This function guides the user to input details for a new product, including name, price, quantity, and date updated.
    It uses validation functions to ensure the input meets the required format and data types. The user is prompted
    to re-enter the data until it's correct. Once all information is collected and validated, a new Product object
    is created and returned.

    Args:
    None

    Returns:
    Product: A new Product object with user-entered and validated information.
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
    return new_product


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
            new_product = user_entered_product()
            add_product(new_product)  
            time.sleep(1)
            print('Product Added')
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
