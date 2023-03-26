import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
import time
import db
import api

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

def display_tracked_items():
    tracked_items = db.get_tracked_items()
    items_data = []
    for index, item in enumerate(tracked_items):
        name, url = item
        price = api.fetch_item_value(url)
        if price is not None:
            previous_price = db.get_previous_price(name)
            db.store_item_price(name, float(price.strip("$")))
            if previous_price is not None:
                price_diff = float(price.strip("$")) - previous_price
                if price_diff > 0:
                    arrow = "↑"
                    color = "green"
                elif price_diff < 0:
                    arrow = "↓"
                    color = "red"
                else:
                    arrow = "→"
                    color = "yellow"
                formatted_price = f"{price} [bold {color}]{arrow}[/bold {color}]"
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

def remove_items_by_user_input():
    while True:
        display_tracked_items()
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