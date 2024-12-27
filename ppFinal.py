import os
import time


def print_title(title):  # udah
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n -- {title} -- \n")


def duplicate_check(data_to_check, data_content):  # udah
    for data_list in data_content:
        if data_list[0] == data_to_check:
            return True
    return False


def format_file_header(file_name):  # udah
    headers = {
        "products.txt": "Product ID | Product Name | Qty | Description | Price (MYR)",
        "suppliers.txt": "Supplier ID | Name | Contact",
        "orders.txt": "Order ID | Product Name | Qty | Clients"
    }

    with open(file_name, 'r') as file:
        first_line = file.readline().strip()

    if first_line == headers[file_name]:
        return first_line
    with open(file_name, 'r+') as file:
        original_content = file.read()
        file.seek(0)
        file.write(headers[file_name] + "\n" + original_content)


def load_data(file_name):  # udah
    data = []

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file.readlines()[1:]:
                data.append(line.strip().split(','))
    elif not os.path.exists(file_name):
        with open(file_name, 'w'):
            pass

    format_file_header(file_name)

    return data


def save_data(file_name, data_content):  # udah
    file_header = format_file_header(file_name)

    with open(file_name, 'w') as file:
        file.write(file_header + '\n')
        for data in data_content:
            file.write(','.join([str(item) for item in data]) + '\n')


def add_product(products_data):  # udah
    print_title("ADDING PRODUCT")

    try:
        while 1:
            product_id = input('Enter your product id: ').upper()
            if duplicate_check(product_id, products_data):
                print("The ID already exist on the database")
            else:
                break
        product_name = input('Enter product name: ')
        product_count = int(input('Enter how many product: '))
        product_description = input('Enter description of product: ')
        product_price = float(input('Enter product price (in MYR): '))
    except ValueError:
        print("Wrong Value Type")
    else:
        products_data.append([product_id, product_name, product_count, product_description, product_price])
        save_data("products.txt", products_data)

        print(f'Number of product added: {len(products_data)}')
        print('Product is successfully added')


def update_product(products_data):  # udah
    print_title("UPDATE PRODUCT")
    item_number = 0

    print("Product ID | Product Name | Qty | Description | Price (MYR)")
    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")

    product_id = input('\nEnter the product ID : ').upper()
    for product in products_data:
        if product[0] == product_id:
            try:
                product[1] = input(f"Enter new Name (current: {product[1]}): ")
                product[2] = int(input(f"Enter new Qty (current: {product[2]}): "))
                product[3] = input(f"Enter new Description (current: {product[3]}): ")
                product[4] = float(input(f"Enter new price (current: {product[4]}): "))
            except ValueError:
                print("Wrong Value Type")
                return
            else:
                save_data("products.txt", products_data)
                print("Product updated successfully!")
                return
    else:
        print("Product not found")


def add_supplier(suppliers_data):  # udah
    print_title("ADDING SUPPLIER")

    try:
        while 1:
            supplier_id = input("Enter supplier ID: ").upper()
            if duplicate_check(supplier_id, suppliers_data):
                print("The ID already exist on the database")
            else:
                break
        name = input("Enter supplier name: ")
        contact = int(input("Enter supplier contact number: "))
    except ValueError:
        print("Wrong Value Type")
    else:
        suppliers_data.append([supplier_id, name, contact])
        save_data("suppliers.txt", suppliers_data)
        print("Suppliers successfully added!")


def place_order(products_data, orders_data):
    print_title("ORDERING PRODUCT")  # title

    item_number = 0  # an ordinary number (used in showing the products)
    order_id = 0  # automatic id in order list

    for i in orders_data:
        order_id += 1  # set the id for the latest (count how many orders have made)

    # TESTING IS THERE ANY DATA ?
    if not products_data:  # if there is no
        print("Sorry, we don't have any product right now")
        time.sleep(3)


    else:  # if there is
        # show the available products
        print("Product Available currently: \n")
        print("Product ID | Product Name | Qty | Description")
        for product in products_data:
            item_number += 1
            print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}")
        ask_user = input(
            "\nWhich way do you prefer to order the products (ID/Name): ").upper()  # ask the user to choose id or name

        # IF THE USER CHOSE ID
        if ask_user == 'ID':
            order_product = input("Select the product (ID): ").upper()

            # (for) checking if there is a product or not
            for product in products_data:
                if product[0] == order_product:

                    # checking if the user input a correct value
                    try:
                        order_id += 1  # setting the order id
                        order_customer = input("\nInput the client name: ")
                        order_quantity = int(input(f"How much products do you order (available[{product[2]}]): "))

                        # to test if the products quantity meet the user's order
                        if order_quantity <= int(product[2]):
                            orders_data.append([f"{order_id:04d}", product[1], order_quantity,
                                                order_customer])  # dd the data to the orders list
                            product[2] = int(product[2]) - order_quantity  # reduce the product
                            save_data("orders.txt", orders_data)  # save data orders
                            save_data("products.txt", products_data)  # save data products
                            print(
                                f"\nDetails:\nID = {order_id:04d} | Product = {product[1]} | Order = {order_quantity} | Client = {order_customer}\n\nOrders added successfully!\n")  # show the orders which made
                            time.sleep(3)
                            return

                        else:  # if the products quantity not meet the user's order
                            print(f"Sorry, insufficient product\n")
                            time.sleep(2)
                            return

                    except ValueError:  # if the user input the wrong value type
                        print("Wrong value type, please input number type")
                        time.sleep(2)
                        return

            else:  # if there is no such product
                print("Product not found")
                time.sleep(2)
                return


        # IF THE USER CHOSE NAME
        elif ask_user == 'NAME':
            order_product = input("Select the product (product name): ")

            # (for)checking if there is a product or not
            for product in products_data:
                if product[1] == order_product:

                    # checking if the user input a correct value
                    try:
                        order_id += 1  # setting the order id
                        order_customer = input("\nInput the client name: ")
                        order_quantity = int(input(f"How much products do you order (available[{product[2]}]): "))

                        # testing if the products quantity meet the user's order
                        if order_quantity <= int(product[2]):
                            orders_data.append([f"{order_id:04d}", product[1], order_quantity,
                                                order_customer])  # add the data to the orders list
                            product[2] = int(product[2]) - order_quantity  # reduce the product
                            save_data("orders", orders_data)  # save data orders
                            save_data("products", products_data)  # save data products
                            print(
                                f"\nDetails:\nID = {order_id:04d} | Product = {product[1]} | Order = {order_quantity} | Client = {order_customer}\n\nOrders added successfully!\n")  # show the orders which made
                            time.sleep(3)
                            return

                        else:  # if the products quantity not meet the user's order
                            print(f"Sorry, insufficient product\n")
                            time.sleep(2)
                            return

                    except ValueError:  # if the user input the wrong value type
                        print("Wrong value type, please input number type")
                        time.sleep(2)
                        return

            else:  # if there is no such product
                print("Product not found")
                time.sleep(2)
                return


        # IF THE USER DID NOT INPUT ID NOR NAME
        else:
            print("Please input correctly(ID/Name)\n")
            time.sleep(2)
            return


def view_inventory(products_data):
    print_title("VIEW INVENTORY")
    item_number = 0

    print("Product ID | Qty | Price | Description | Price (MYR)")
    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")

    while 1:
        go_back = input("Do you want to go back? (y/n): ").lower()
        if go_back == 'y':
            break


def generate_reports(products_data, orders_data):
    def low_stock_report(products_data):
        print_title("LOW STOCK REPORT")
        item_number = 0

        for product in products_data:
            if int(product[2]) <= 10:
                item_number += 1
                print(f"{item_number}. {product[0]} stock is at {product[2]}")

    def product_sales_report(products_data, orders_data):
        print_title("PRODUCT SALES REPORT")
        item_number = 0

        for product in products_data:
            for order in orders_data:
                if order[1] == product[1]:
                    item_number += 1
                    revenue = (int(order[2]) * float(product[4]))
                    print(
                        f"{item_number}. {product[1]}: {order[2]} unit{'s'[:int(order[2]) ^ 1]} sold for {revenue} MYR")

    print_title("GENERATE REPORTS")
    print("1. Low Stock\n"
          "2. Product Sales")
    report_type = input("Pick the report you want: ")
    match report_type:
        case "1":
            low_stock_report(products_data)
        case "2":
            product_sales_report(products_data, orders_data)
        case _:
            print("Invalid option, pick something within the range of 1-2")
            time.sleep(2)
            return
    while 1:
        go_back = input("Do you want to go back? (y/n): ").lower()
        if go_back == 'y':
            break


def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        products_data = load_data('products.txt')
        suppliers_data = load_data('suppliers.txt')
        orders_data = load_data('orders.txt')

        user_input = input("1. Add a new product \n"
                           "2. Update product details \n"
                           "3. Add a new supplier \n"
                           "4. Place an order \n"
                           "5. View inventory \n"
                           "6. Generate reports \n"
                           "7. Exit \n"
                           "Enter Number: ")

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
                generate_reports(products_data, orders_data)
            case "7":
                break
            case _:
                print("Invalid option, pick something within the range of 1-7")


if __name__ == "__main__":
    main()