import pendulum
import os
import csv
import uuid
from datetime import datetime, timedelta
import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pineapple import intro_text

import seaborn as sns
from rich import print
from rich.table import Table
from rich.syntax import Syntax




# # Do not change these lines.
# __winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
# __human_name__ = "superpy"
# # Your code below this line.

# configuration for CSV files

BOUGHT_FILE = 'bought.csv'
SOLD_FILE = 'sold.csv'
DATE_FILE = 'date.csv'
BOUGHT_ITEMS = ['bought_id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
SOLD_ITEMS = ['sold_id', 'product_name', 'bought_id', 'sell_price', 'sell_date']

# getting today's date from file

def get_today_from_file(file_path):
    file_path = os.path.abspath(file_path)
    dt = pendulum.today().date()
    timeshift = 0
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            file_content = f.read().strip().split(',')
            timeshift = int(file_content[1]) if len(file_content) > 1 else 0
            
    with open(file_path, 'w') as f:
        f.write(f"{str(dt)},{timeshift}")
    dt = dt.add(days=timeshift)
    return dt


# retreiving TODAY and timeshift from file
today = get_today_from_file(DATE_FILE)

def check_file_exists(file, header):
    # turnign file file into an absolute path
    file = os.path.abspath(file)
    write_header = False
    if not os.path.exists(file):
        write_header = True
        with open(file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        intro_text()

# checking if bought and sold files exist, and create them if they don't
check_file_exists(BOUGHT_FILE, BOUGHT_ITEMS) 
check_file_exists(SOLD_FILE, SOLD_ITEMS) 


# shifting days from variable today
def timeshift(days, today = today):
    
    today = pendulum.today().date()
    timeshift = 0
    if os.path.exists(DATE_FILE):
        with open(DATE_FILE, 'r') as date_file:
            file_content = date_file.read().strip().split(',')
            timeshift = int(file_content[1]) if len(file_content) > 1 else 0
    updated_timeshift = timeshift + days
    with open(DATE_FILE, 'w') as date_file:
        date_file.write(f"{str(today)},{updated_timeshift}")
    return today.add(days=updated_timeshift)


# getting sold bought ids
def get_sold_bought_ids():
    sold_bought_ids = []
    with open(SOLD_FILE, "r") as sold_data:
        sold_reader = csv.DictReader(sold_data)
        
        for row in sold_reader:
            sold_bought_ids.append(row['bought_id'])
    return sold_bought_ids

# writing to csv function
def write_to_csv(file, item, header):
    with open(file, "a", newline='') as f:
        writer = csv.writer(f)
        # formatting expiration_date before writing to file
        item[4] = datetime.strptime(item[4], '%Y-%m-%d').strftime('%Y-%m-%d')
        writer.writerow(item)
    if file == BOUGHT_FILE:
        print(f"Purchase added: {item[1], item[3]}, {item[4]}")
    if file == SOLD_FILE:
        print(f"Sale added: {item[1], item[3]}, {item[4]}")

# reading from csv files
def read_from_csv(file):
    try:
        with open(file, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            items = [row for row in reader]
        return items
    except FileNotFoundError:
        return []

class Product:
    def __init__(self, name, price, expiration_date):
        self.name = name
        self.price = float(price)
        self.expiration_date = pendulum.parse(expiration_date, strict=False).format("YYYY-MM-DD")

    def validate(self):
        if not self.name.isalpha() and not self.name.isspace():
            raise ValueError("Name should only contain letters and spaces")
        if not isinstance(self.price, float):
            raise ValueError("Price should be a number.")

# buy function to purchases to the bought.csv file
def buy(product):
    product.validate()
    bought_id = str(uuid.uuid1())
    item = [bought_id, product.name, today.strftime('%Y-%m-%d'), product.price, product.expiration_date]
    check_file_exists(BOUGHT_FILE, BOUGHT_ITEMS)
    write_to_csv(BOUGHT_FILE, item, BOUGHT_ITEMS)

def multiple_buy(product, quantity):
    for i in range(quantity):
        buy(product)

def multiple_sell(product_name, sell_price, sell_date, quantity):
    for i in range(quantity):
        sell(product_name, sell_price, sell_date)


def sell(product_name, sell_price, sell_date=None):
    # validatiting the sell_price
    try:
        sell_price = float(sell_price)
    except ValueError:
        raise ValueError(f"Invalid sell price: '{sell_price}'. Please provide a price in numbers.")

    # validatiting the sell_date
    if sell_date is not None:
        sell_date = pendulum.parse(str(sell_date), strict=False).format("YYYY-MM-DD")
    else:
        sell_date = today.strftime('%Y-%m-%d')

    unused_bought_ids = []
    with open(BOUGHT_FILE, "r") as bought_data:
        bought_reader = csv.DictReader(bought_data)
        for row in bought_reader:
            if row['product_name'].lower() == product_name.lower() and row['expiration_date'] >= sell_date and row['bought_id'] not in get_sold_bought_ids():
                unused_bought_ids.append(row['bought_id'])

    if not unused_bought_ids:
        raise ValueError(f"No available {product_name} in stock.")

    sold_id = str(uuid.uuid1())
    item = [sold_id, product_name, unused_bought_ids[0], sell_price, sell_date]
    check_file_exists(SOLD_FILE, SOLD_ITEMS)
    write_to_csv(SOLD_FILE, item, SOLD_ITEMS)


# the inventory function will list all products in bought file, when these are not found in sold file
def inventory(date=today):
    bought_items = read_from_csv(BOUGHT_FILE)
    sold_items = read_from_csv(SOLD_FILE)

    # creating a SET to store bought_ids for products that have been sold
    sold_bought_ids = set([sold_item[2] for sold_item in sold_items])

    product_counts = {}

    for item in bought_items:
        expiration_date = pendulum.parse(item[4], strict=False).date()
        if date <= expiration_date and item[0] not in sold_bought_ids:
            # creating a list of relevant fields to use as identification in  product_counts dictionary
            key = [item[1], item[3], item[4]] # [name, price, expiration_date]
            key_str = ",".join(str(e) for e in key)
            if key_str in product_counts:
                # if product is already in dictionary, increment count
                product_counts[key_str] += 1
            else:
                # if product is not in dictionary, add it with a count of 1
                product_counts[key_str] = 1

    # printing the inventory report
    print("Current inventory as of", str(date)+":" + "\n")
    print("+--------------+-------+-----------+-----------------+")
    print("|{:<14}|{:>7}|{:>11}|{:>17}|".format("Product Name", "Count", "Buy Price", "Expiration Date"))
    print("+--------------+-------+-----------+-----------------+")
    for key_str, count in product_counts.items():
        key = key_str.split(",")
        name, price, expiration_date = key
        print("|{:<14}|{:>7}|{:>11}|{:>17}|".format(name, count, price, expiration_date))
    print("+--------------+-------+-----------+-----------------+")

#calculating revenue
def revenue(date1=None, date2=None, print_report=True):
    sold_items = read_from_csv(SOLD_FILE)
    revenue = 0
    if date1 is None:
        # if no start date is given, consider all sold items
        for item in sold_items:
            revenue += float(item[3])
    else:
        # Set end_date to today if it's not provided
        if date2 is None:
            end_date = today
        else:
            end_date = date2

        # Calculating revenue for sold items between start and end dates
        for item in sold_items:
            sold_date = pendulum.parse(item[4], strict=False).date()
            if date1 <= sold_date <= end_date:
                revenue += float(item[3])
    if print_report is True:
        print(f'Total revenue: {revenue:.2f}')
    return revenue

#calculating profit
def profit(date1=None, date2=None, current_date=today):
    sold_revenue = revenue(date1, date2, False)
    bought_items = read_from_csv(BOUGHT_FILE)
    if date2 is None:
        date2 = current_date
    total_cost = 0
    for item in bought_items:
        if date1 is None or pendulum.parse(item[2]).date() <= date1:
            total_cost += float(item[3])

    profit = 0 if sold_revenue is None else sold_revenue - total_cost
    if date1 is None:
        print(f'Total profit until {date2}: {profit:.2f}')
    else:
        print(f'Total profit from {date1} until {date2}: {profit:.2f}')

# calculating costs monthly
def monthly_data(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.set_index(date_column)
    monthly_df = df.resample('M').sum(numeric_only=True)
    return monthly_df

# calculating costs monthly
def costs_monthly():
    bought_items = read_from_csv(BOUGHT_FILE)
    bought_df = pd.DataFrame(bought_items, columns=BOUGHT_ITEMS)
    bought_df['buy_price'] = bought_df['buy_price'].astype(float)
    return monthly_data(bought_df, 'buy_date')

# calculating revenue monthly
def revenue_monthly():
    sold_items = read_from_csv(SOLD_FILE)
    sold_df = pd.DataFrame(sold_items, columns=SOLD_ITEMS)
    sold_df['sell_price'] = sold_df['sell_price'].astype(float)
    return monthly_data(sold_df, 'sell_date')

# calculating profit monthly
def profit_monthly():
    costs_df = costs_monthly()
    revenue_df = revenue_monthly()
    profit_df = revenue_df['sell_price'] - costs_df['buy_price']
    profit_df = pd.DataFrame(profit_df, columns=['profit'])
    return profit_df

# displaying a bar chart of costs, revenue, and profit monthly
def display_costs_revenue_profit():
    
    costs_df = costs_monthly()
    revenue_df = revenue_monthly()
    profit_df = profit_monthly()
    df = pd.concat([costs_df, revenue_df, profit_df], axis=1)
    df.plot.bar()
    plt.title('Costs, Revenue, and Profit Monthly Overview')
    plt.xlabel('Month and Year')
    plt.ylabel('Amount (€)')
    plt.xticks(range(len(df.index)), [x.strftime('%b %Y') for x in df.index], rotation=45)
    plt.grid(axis='y')
    plt.legend(['Costs', 'Revenue', 'Profit'])
    plt.tight_layout()
    plt.get_current_fig_manager().set_window_title('Super Mark Statistics')
    plt.show()

# converts date strings to date time objects, based on the value of today. 
def convert_date(date_str, today):
   
    date_mapping = {
        'today': today,
        'yesterday': today - pendulum.duration(days=1),
        'tomorrow': today + pendulum.duration(days=1),
        'next week': today + pendulum.duration(weeks=1)
    }

    try:
        if date_str in date_mapping:
            return date_mapping[date_str]
        else:
            return pendulum.parse(date_str, strict=False).date()
    except ValueError as e:
        raise ValueError(f"Invalid date format '{date_str}'. Expected format is 'YYYY-MM-DD' or use one of the following keywords: 'today', 'yesterday', 'tomorrow', 'next week'.") from e

#creating the extensive help menu with RICH, when the program is called with no arguments
def display_help_menu():
    

    # Create a table to display the actions and their descriptions
    table = Table(title="Welcome to the SUPER-MARK!", show_header=True, header_style="bold magenta")
    table.add_column("Action", style="cyan")
    table.add_column("Description", style="green")

    # Add rows to the table
    table.add_row("buy", "Buy a product")
    table.add_row("sell", "Sell a product")
    table.add_row("inventory", "Show the inventory")
    table.add_row("revenue", "Show the revenue")
    table.add_row("profit", "Show the profit")
    table.add_row("stats", "Display costs, revenue, and profit statistics")
    table.add_row("timeshift", "Shift the current date")

    # Print the table
    print(table)

    # Create a syntax-highlighted code block for examples
    code = '''
    Examples:
    python3 supermark.py buy Apple 10.00 2024-01-03 5  (PRODUCT)(PRICE)(EXP-DATE)(AMOUNT)(optional)
    python3 supermark.py sell Apple 10.00 2024-01-01  (PRODUCT)(PRICE)(EXP-DATE)
    python3 supermark.py inventory 2024-01-03 (DATE)(starting range)
    python3 supermark.py revenue 2024-01-01  (DATE)(starting range)
    python3 supermark.py profit 2024-01-01 2024-01-31    (DATE)(starting range)(DATE)(ending range)
    python3 supermark.py stats
    python3 supermark.py timeshift 5  (NUMBER OF DAYS TO SHIFT)
    python3 supermark.py timeshift 2024-02-02  (DATE TO SHIFT TO)
    '''
    syntax_code = Syntax(code, "python", theme="monokai", line_numbers=True)

    # Print the syntax-highlighted code block
    print(syntax_code)

# the argparse menu
if __name__ == "__main__":
    if len(sys.argv) == 1:
        display_help_menu()
        sys.exit()
    
    if len(sys.argv) > 1:
        
        parser = argparse.ArgumentParser(description='\n Welcome to the SUPER-MARK \n ')

        
        parser.add_argument('action', help='Action to perform', choices=['buy', 'sell', 'inventory', 'revenue', 'profit', 'stats', 'timeshift'])
        parser.add_argument('product_args', nargs='*', help='Product information (product_name [quantity] price)')

        parser.add_argument('--expiration-date', help='Expiration date of the product')
        parser.add_argument('--sell-price', help='Price at which to sell the product')
        parser.add_argument('--sell-date', help='Date on which the product was sold (optional)')
        parser.add_argument('--display-stats', action='store_true', help="Display Super Mark's costs, revenue, and profit statistics.")
        parser.add_argument('--amount', type=int, help='Amount of product to buy')

        args = parser.parse_args()

        if args.action == 'stats' or args.display_stats:
            display_costs_revenue_profit()

        if args.action == 'buy':
            if len(args.product_args) < 3:
                print("Please provide a product name, a price, an expiration date and an amount (optional) \n Example: python3 supermark.py buy Apple 10.00 2024-01-03 5")
                sys.exit()
            # deciding if we can buy, or multibuy, if there are more then 3 arguments
            product_name = args.product_args[0]
            price = args.product_args[1]
            date = str(convert_date(args.product_args[2], today))
            amount = None
            product = Product(product_name, price, date)
            if len(args.product_args) > 3 and args.product_args[3] is not None:
                amount = args.product_args[3]
                
            if amount:
                multiple_buy(product, int(amount))
            else:
                buy(product)

        elif args.action == 'sell':
            if len(args.product_args) < 2:
                print("Please provide a product name, a sell price, a sell date (optional), and an amount (optional) \n Example: python3 supermark.py sell Apple 10.00 2024-01-01 5")
                sys.exit()
            # performing sell action
            sell_date = today
            product_name = args.product_args[0]
            sell_price = args.product_args[1]
            amount = None
            if len(args.product_args) >= 3:
                sell_date = str(convert_date(args.product_args[2], today))
            if len(args.product_args) > 3 and args.product_args[3] is not None:
                amount = args.product_args[3]
            

            if amount:
                multiple_sell(product_name, sell_price, sell_date, int(amount))
            else:
                sell(product_name, sell_price, sell_date)

        elif args.action == 'inventory':
            # showing inventory action
            if len(args.product_args) == 0:
                date = today
            else:
                date = convert_date(args.product_args[0], today)

            inventory(date)

        elif args.action == 'revenue':
            # giving revenue overview, 
            if len(args.product_args) > 0:
                date_str = args.product_args[0]
                date = convert_date(args.product_args[0], today)
            else:
                date = today

            revenue(date)

        elif args.action == 'profit':
            # creating profit overview, with or without specified dates
            if len(args.product_args) == 0:
                profit(today)
            elif len(args.product_args) == 1:
                date1 = convert_date(args.product_args[0], today)
                profit(date1)
            elif len(args.product_args) > 1:
                date1 = convert_date(args.product_args[0], today)
                date2 = convert_date(args.product_args[1], today)
                profit(date1, date2)

        elif args.action == 'timeshift':
        
            if len(args.product_args) != 1:
                print("Please provide either the number of days to shift the date or a specific date. \nExample: python3 supermark.py timeshift 5\nExample: python3 supermark.py timeshift 2024-01-01")
                sys.exit()

            input_arg = args.product_args[0]
            
            try:
                # try to parse the input as a date
                input_date = pendulum.parse(input_arg, strict=True).date()
                # calculate the difference in days for the input date and the internal 'today' variable
                days_to_shift = (input_date - today).in_days()
                
            except ValueError:
                # if it's not a valid date, check if it's a integer representing the number of days to shift
                try:
                    days_to_shift = int(input_arg)
                    
                except ValueError:
                    print("Invalid input. Please provide either a valid date or a valid number of days to shift, bwwtween -10000 and 10000.")
                    sys.exit()

                # checking if the provided number of days to shift is within the given range
                if not -10000 <= days_to_shift <= 10000:
                    print("No valid number of days to timeshift. Must be between -10000 and 10000.")
                    sys.exit()
                    
            new_date = timeshift(days_to_shift)
            print(f"Shifted date by {days_to_shift} days. New date: {new_date}")


