import os


def print_title(title: str):
    """
    Clear the console then display the menu header
    """

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n -- {title} -- \n")


def duplicate_check(input_prompt: str, data_content) -> str:
    """
    Check if the input data is already exist or not in the database
    """

    # loop will be broken when the input ID does not exist in database
    while True:
        user_input = input(f"{input_prompt}").upper()

        for data_list in data_content:
            if data_list[0] == user_input:
                print("The ID already exist on the database")
                break

        else:
            return user_input


def format_file_header(file_name):
    """
    Display expected headers for each file type
    """

    headers = {
        "products.txt": "Product ID | Product Name | Qty | Description | Price (MYR)",
        "suppliers.txt": "Supplier ID | Name | Contact",
        "orders.txt": "Order ID | Product Name | Qty | Clients"
    }

    # store the first line to a variable
    with open(file_name, 'r') as file:
        first_line = file.readline().strip()

    # if first line does match, return first_line values
    if first_line == headers[file_name]:
        return first_line

    # if not, append first_line as a header for the file
    with open(file_name, 'r+') as file:
        original_content = file.read()
        file.seek(0)
        file.write(headers[file_name] + "\n" + original_content)


def load_data(file_name):
    """
    Load data from the file
    """

    data = []

    # check the file exists
    if os.path.exists(file_name):
        # read the data of the file starting from line 2. Strip white space and split new line with commas to append it to data list
        with open(file_name, 'r') as file:
            lines = file.readlines()[1:]
            data = [line.strip().split(',') for line in lines]

    elif not os.path.exists(file_name):
        # create an empty file with specified file name
        with open(file_name, 'w'):
            pass

    format_file_header(file_name)

    return data


def save_data(file_name, data_content):
    """
    Save data to the file
    """

    # check the file header is correct
    file_header = format_file_header(file_name)

    # overwrite its contents, write the header as the first line
    with open(file_name, 'w') as file:
        file.write(file_header + '\n')
        # iterate through each item in the data_content list
        for data in data_content:
            file.write(','.join([str(item) for item in data]) + '\n')


def add_product(products_data):
    """
    Add a new product
    """

    print_title("ADDING PRODUCT")

    try:
        # prompts the user to input the product details
        product_id = duplicate_check("Enter your product id: ", products_data).strip()
        product_name = input("Enter product name: ").strip()
        product_count = int(input("Enter how many product: "))
        product_description = input("Enter description of product: ").strip()
        product_price = float(input("Enter product price (in MYR): "))

    # displays error message if the user enters invalid data type
    except ValueError:
        print("Wrong Value Type")

        # executes if no exception is triggered in the “try” block
    else:
        products_data.append([product_id, product_name, product_count, product_description, product_price])
        save_data("products.txt", products_data)  # save data

        print(f"Number of product added: {len(products_data)}")
        print("Product is successfully added")


def update_product(products_data):
    """
    Update product details
    """

    print_title("UPDATE PRODUCT")
    item_number = 0

    print("Product ID | Product Name | Qty | Description | Price (MYR)")
    # iterate through the list of products and display each product added with details
    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")

    # Check if the ID exist or not
    product_id = input("\nEnter the product ID : ").strip().upper()
    for product in products_data:
        if product[0] == product_id:
            try:
                product[1] = input(f"Enter new Name (current: {product[1]}): ").strip()
                product[2] = int(input(f"Enter new Qty (current: {product[2]}): "))
                product[3] = input(f"Enter new Description (current: {product[3]}): ").strip()
                product[4] = float(input(f"Enter new price (current: {product[4]}): "))

            # display error message if user enters invalid data type
            except ValueError:
                print("Wrong Value Type")
                return

            else:
                save_data("products.txt", products_data)
                print("Product updated successfully!")
                return

    else:
        print("Product not found")


def add_supplier(suppliers_data):
    """
    Add a new suppliers
    """

    print_title("ADDING SUPPLIER")

    try:
        supplier_id = duplicate_check("Enter supplier ID: ", suppliers_data).strip()
        name = input("Enter supplier name: ").strip()
        contact = int(input("Enter supplier contact number: "))

    # display error message if user enters invalid data type
    except ValueError:
        print("Wrong Value Type")

    else:
        suppliers_data.append([supplier_id, name, contact])
        save_data("suppliers.txt", suppliers_data)  # save data
        print("Suppliers successfully added!")


def place_order(products_data, orders_data):
    """
    Placing order
    """

    print_title("ORDERING PRODUCT")

    item_number = 0  # an ordinary number (used in showing the products)
    order_id = 0  # automatic id in order list

    for i in orders_data:
        order_id += 1  # set the id for the latest (count how many orders have made)

    # TESTING IS THERE ANY DATA ?
    # if there is none, show error
    if not products_data:
        print("Sorry, we don't have any product right now")
        return

    # if there is show the available products
    print("Product Available currently: \n\n"
          "Product ID | Product Name | Qty | Description | Price (MYR)")

    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")

    order_product = input("\nSelect the product (ID): ").strip().upper()

    # (for) checking if there is a product or not
    for product in products_data:
        # checking if the user input a correct value
        if product[0] == order_product:
            order_id += 1  # setting the order id
            try:
                order_customer = input("Input the client name: ").strip()
                order_quantity = int(input(f"How many products would you like to order (Available: {product[2]}): "))

            # if the user input the wrong value type
            except ValueError:
                print("Wrong value type, please input number type")
                return

            else:
                # print an error if the ordered quantity is higher than in the inventory
                if order_quantity >= int(product[2]):
                    print("\nSorry, insufficient product")
                    return

                # add the data to the orders list
                orders_data.append([f"{order_id:04d}", product[1], order_quantity, order_customer])
                # reduce the product
                product[2] = int(product[2]) - order_quantity

                save_data("orders.txt", orders_data)
                save_data("products.txt", products_data)

                # show the orders which made
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Details:\n"
                      f"ID = {order_id:04d} | Product = {product[1]} | Order = {order_quantity} | Client = {order_customer} \n\n"
                      "Orders added successfully!")

                return

    # if there is no such product
    else:
        print("Product not found")
        return


def view_inventory(products_data):
    """
    View inventory
    """

    print_title("VIEW INVENTORY")
    item_number = 0

    print("Product ID | Qty | Price | Description | Price (MYR)")

    # iterate through the list of products and display each product added with details
    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")


def generate_reports(products_data, orders_data, suppliers_data):
    """
    Generate reports
    """

    print_title("GENERATE REPORTS")

    def low_stock_report(products_info):
        print_title("LOW STOCK REPORT")
        item_number = 0

        # Iterates through products_data and passes the if statement when the quantity is at or below 10.
        for product in products_info:
            if int(product[2]) <= 10:
                item_number += 1
                print(f"{item_number}. {product[0]} stock is at {product[2]}")

    def product_sales_report(products_info, orders_info):
        print_title("PRODUCT SALES REPORT")
        item_number = 0

        # Iterates through products_data and orders_data and passes the if statement when both names match.
        for product in products_info:
            for order in orders_info:
                if order[1] == product[1]:
                    item_number += 1
                    revenue = int(order[2]) * float(product[4])
                    print(
                        f"{item_number}. {product[1]}: {order[2]} unit{'s'[:int(order[2]) ^ 1]} sold for {revenue} MYR")

    def view_suppliers(suppliers_info):
        print_title("SUPPLIER LIST REPORT")
        item_number = 0

        # iterate through the list of products and display each product added with details
        print("Supplier ID | Name | Contact")

        for supplier in suppliers_info:
            item_number += 1
            print(f"{item_number}. {supplier[0]}, {supplier[1]}, {supplier[2]}")

    print("1. Low Stock\n"
          "2. Product Sales\n"
          "3. Supplier List")
    report_type = input("Pick the report you want: ").strip()

    match report_type:
        case "1":
            low_stock_report(products_data)
        case "2":
            product_sales_report(products_data, orders_data)
        case "3":
            view_suppliers(suppliers_data)
        case _:
            print("Invalid option, pick something within the range of 1-3")


def main():
    """
    Main menu option
    """

    # start an infinite loop until the user exits
    while True:
        print_title("Main Menu")

        # load data from file
        products_data = load_data('products.txt')
        suppliers_data = load_data('suppliers.txt')
        orders_data = load_data('orders.txt')

        print("1. Add a new product \n"
              "2. Update product details \n"
              "3. Add a new supplier \n"
              "4. Place an order \n"
              "5. View inventory \n"
              "6. Generate reports \n"
              "7. Exit \n")
        user_input = input("Enter Number: ").strip()

        match user_input:
            case "1":
                add_product(products_data)
            case "2":
                update_product(products_data)
            case "3":
                add_supplier(suppliers_data)
            case "4":
                place_order(products_data, orders_data)
            case "5":
                view_inventory(products_data)
            case "6":
                generate_reports(products_data, orders_data, suppliers_data)
            case "7":
                break
            case _:
                print("Invalid option, pick something within the range of 1-7")

        # Pause the program so the user can see logs of the function
        input("\nPress enter to continue... ")


if __name__ == "__main__":
    main()
