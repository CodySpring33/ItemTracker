import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
import time
import db
import api
import os
from dotenv import load_dotenv, set_key
import asyncio

load_dotenv()

def print_ascii_art():
    ascii_art = r''' /$$$$$$ /$$$$$$$$ /$$$$$$$$ /$$      /$$       /$$$$$$$$ /$$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$
|_  $$_/|__  $$__/| $$_____/| $$$    /$$$      |__  $$__/| $$__  $$ /$$__  $$ /$$__  $$| $$  /$$/
  | $$     | $$   | $$      | $$$$  /$$$$         | $$   | $$  \ $$| $$  \ $$| $$  \__/| $$ /$$/ 
  | $$     | $$   | $$$$$   | $$ $$/$$ $$         | $$   | $$$$$$$/| $$$$$$$$| $$      | $$$$$/  
  | $$     | $$   | $$__/   | $$  $$$| $$         | $$   | $$__  $$| $$__  $$| $$      | $$  $$  
  | $$     | $$   | $$      | $$\  $ | $$         | $$   | $$  \ $$| $$  | $$| $$    $$| $$\  $$ 
 /$$$$$$   | $$   | $$$$$$$$| $$ \/  | $$         | $$   | $$  | $$| $$  | $$|  $$$$$$/| $$ \  $$
|______/   |__/   |________/|__/     |__/         |__/   |__/  |__/|__/  |__/ \______/ |__/  \__/
                                                                                                 
                                                                                                 
                                                                                                 '''
    console = Console()

    for line in ascii_art.splitlines():
        formatted_line = ""
        for char in line:
            if char == "$":
                formatted_line += "[green]$[/green]"
            else:
                formatted_line += f"{char}" if char != " " else " "
        console.print(formatted_line)

def plot_item_price_graph(name):
    prices_data = db.get_item_prices(name)

    if prices_data:
        timestamps, prices = zip(*prices_data)
        human_readable_dates = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)) for ts in timestamps]

        plt.plot(human_readable_dates, prices)
        plt.xlabel("Date and Time")
        plt.ylabel("Price")
        plt.title(f"Price/Time Graph for {name}")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
    else:
        print(f"No price data found for the item '{name}'")

async def fetch_all_items(tracked_items):
    tasks = []
    for name, url in tracked_items:
        tasks.append(asyncio.create_task(api.fetch_item_value(url)))

    return await asyncio.gather(*tasks)

async def display_tracked_items():
    SIGN = os.getenv('CURRENCY')
    tracked_items = db.get_tracked_items()
    total_items = len(tracked_items)
    items_data = []

    prices = await fetch_all_items(tracked_items)

    for index, item in enumerate(tracked_items):
        name, url = item
        loading_bar(index+1, total_items)
        price = prices[index]
        if price is not None:
            if price == -1:
                price = db.get_previous_price(name)
                previous_price = -1
                price_float = 0.00
                price = f'{SIGN}' + str(price) + f" ({SIGN} {str(round(price * .85,2))})"
            else:
                previous_price = db.get_previous_price(name)
                price_float = float(price.strip(f"{SIGN}"))
                db.store_item_price(name, price_float)
                price_tax = round(price_float*.85,2) 


            if previous_price != -1:
                price_diff = price_float - previous_price
                if price_diff > 0:
                    arrow = "↑"
                    color = "green"
                elif price_diff < 0:
                    arrow = "↓"
                    color = "red"
                else:
                    arrow = "→"
                    color = "yellow"
                formatted_price = f"{price} ({SIGN} {price_tax}) [bold {color}]{arrow}[/bold {color}]"
            else:
                formatted_price = price
            items_data.append([index, name, formatted_price])

    table = Table(title="Tracked Items", show_header=True, header_style="bold")
    table.add_column("Index")
    table.add_column("Item Name")
    table.add_column("Price")

    for row in items_data:
        table.add_row(str(row[0]), row[1], row[2])

    console = Console()
    console.print(table)


def display_stored_items():
    SIGN = os.getenv('CURRENCY')
    tracked_items = db.get_tracked_items()
    items_data = []
    for index, item in enumerate(tracked_items):
        name, url = item
        price = db.get_previous_price(name)
        if price is not None:
            tax_price = round(price * .85,2)
            formatted_price = f'{SIGN}' + str(price)
            formatted_tax = f'{SIGN}' + str(tax_price)
            items_data.append([index, name, formatted_price+f" ({formatted_tax})"])

    table = Table(title="Tracked Items", show_header=True, header_style="bold")
    table.add_column("Index")
    table.add_column("Item Name")
    table.add_column("Price")

    for row in items_data:
        table.add_row(str(row[0]), row[1], row[2])

    console = Console()
    console.print(table)


def remove_items_by_user_input():
    while True:
        index_str = input("Enter the index of the item you want to remove (or 'q' to quit): ")
        if index_str.lower() == 'q':
            break
        else:
            try:
                index = int(index_str)
                db.remove_item_by_index(index)
            except ValueError:
                print("Invalid input. Please enter a valid index or 'q' to quit.")

def add_items_by_user_input():
    while True:
        item_name = input("Enter the name of the item you want to track (or 'q' to quit): ")
        if item_name.lower() == 'q':
            break
        else:
            api.add_item_by_name(item_name)

def get_item_by_index(index):
    tracked_items = db.get_tracked_items()
    if 0 <= index < len(tracked_items):
        return tracked_items[index]
    else:
        return None
    
def get_currency_symbol(currency_code):
    currency_symbols = {
        1: '$', 2: '£', 3: '€', 4: 'CHF', 5: '₽', 6: 'zł', 7: 'R$', 8: '¥',
        9: 'kr', 10: 'Rp', 11: 'RM', 12: '₱', 13: 'S$', 14: '฿', 15: '₫',
        16: '₩', 17: '₺', 18: '₴', 19: 'Mex$', 20: 'C$', 21: 'A$', 22: 'NZ$',
        23: '¥', 24: '₹', 25: 'CLP$', 26: 'S/', 27: '$', 28: 'R', 29: 'HK$',
        30: 'NT$', 31: 'SR', 32: 'AED', 33: 'kr', 34: '$', 35: '₪', 36: 'Br',
        37: '₸', 38: 'د.ك', 39: 'ر.ق', 40: '₡', 41: '$U'
    }
    return currency_symbols.get(currency_code, '')


def update_currency(currency):
    items = db.get_tracked_items()
    os.environ["CURRENCY"] = get_currency_symbol(currency)
    os.environ["CODE"] = str(currency)
    set_key('.env', 'CURRENCY', os.environ["CURRENCY"])
    set_key('.env', 'CODE', os.environ["CODE"])

    for item in items:
        hash = api.extract_hash(item[1])
        new_url = f"http://steamcommunity.com/market/priceoverview/?appid=730&currency={currency}&market_hash_name={hash}"
        db.update_url(new_url, item[0])

    print("Currency updated")

def loading_bar(current, total):

    bar_length = 30
    filled_length = int(round(bar_length * current / float(total)))

    percent = round(100.0 * current / float(total), 1)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    print(f'[{bar}] {percent}%\r', end='')
    if current == total:
        print()
 
