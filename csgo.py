import requests
import sqlite3
import time
import urllib.parse
import json
from tabulate import tabulate
import matplotlib.pyplot as plt


DB_NAME = "csgo_items.db"

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
    print(ascii_art)

def init_db():
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items (name TEXT UNIQUE, url TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS item_prices (timestamp INTEGER, name TEXT, price REAL)")
        connection.commit()

def store_item_price(name, price):
    timestamp = int(time.time())
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO item_prices (timestamp, name, price) VALUES (?, ?, ?)", (timestamp, name, price))
        connection.commit()

def add_item(name, url):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO items (name, url) VALUES (?, ?)", (name, url))
    conn.commit()
    conn.close()

def get_tracked_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    tracked_items = c.fetchall()
    conn.close()
    return tracked_items

def get_item_prices(name):
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT timestamp, price FROM item_prices WHERE name=?", (name,))
        prices = cursor.fetchall()
    return prices

def plot_item_price_graph(name):
    prices_data = get_item_prices(name)

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

def fetch_item_value(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    price_element = data["lowest_price"]
    
    if price_element:
        return price_element
    else:
        print(f"Could not fetch the price for the item at {url}.")
        return None


def track_items():
    tracked_items = get_tracked_items()
    for item in tracked_items:
        name, url = item
        price = fetch_item_value(url)
        if price is not None:
            print(f"{name}: {price}")

def search_item_url(item_name):
    search_url = "https://steamcommunity.com/market/search/render/"
    query = {
        "appid": 730,  # CS:GO
        "norender": 1,
        "count": 1,  # Only get the first result
        "query": item_name
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    response = requests.get(search_url, params=query, headers=headers)
    search_results = response.json()

    if search_results["total_count"] > 0:
        first_result = search_results["results"][0]
        item_hash_name = first_result["hash_name"]
        item_url = f"http://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={urllib.parse.quote(item_hash_name)}"
        return item_url
    else:
        return None

def add_item_by_name(item_name):
    url = search_item_url(item_name)
    if url is not None:
        add_item(item_name, url)
        print(f"Item '{item_name}' added successfully.")
    else:
        print(f"Item '{item_name}' not found.")

def add_items_by_user_input():
    while True:
        item_name = input("Enter the name of the item you want to track (or 'q' to quit): ")
        if item_name.lower() == 'q':
            break
        else:
            add_item_by_name(item_name)

def user_wants_to_add_item():
    while True:
        user_input = input("Do you want to add an item to track? (y/n): ").lower()
        if user_input in ["y", "n"]:
            return user_input == "y"
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def display_tracked_items():
    tracked_items = get_tracked_items()
    items_data = []
    for index, item in enumerate(tracked_items):
        name, url = item
        price = fetch_item_value(url)
        if price is not None:
            items_data.append([index, name, price])
            store_item_price(name, float(price.strip("$")))
    
    table = tabulate(items_data, headers=["Index", "Item Name", "Price"], tablefmt="grid")
    print(table)

def get_item_by_index(index):
    tracked_items = get_tracked_items()
    if 0 <= index < len(tracked_items):
        return tracked_items[index]
    else:
        return None    

def remove_item_by_index(index):
    tracked_items = get_tracked_items()
    if 0 <= index < len(tracked_items):
        item_name = tracked_items[index][0]
        with sqlite3.connect(DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM items WHERE name=?", (item_name,))
            connection.commit()
        print(f"Item '{item_name}' removed successfully.")
    else:
        print(f"Invalid index. Please enter an index between 0 and {len(tracked_items) - 1}.")

def remove_items_by_user_input():
    while True:
        display_tracked_items()
        index_str = input("Enter the index of the item you want to remove (or 'q' to quit): ")
        if index_str.lower() == 'q':
            break
        else:
            try:
                index = int(index_str)
                remove_item_by_index(index)
            except ValueError:
                print("Invalid input. Please enter a valid index or 'q' to quit.")


if __name__ == "__main__":
    init_db()

    print_ascii_art()

    while True:
        action = input("Do you want to (a)dd, (r)emove, (g)raph, or (q)uit? ").lower()
        if action == 'a':
            add_items_by_user_input()
        elif action == 'r':
            remove_items_by_user_input()
        elif action == 'g':
            display_tracked_items()
            index_str = input("Enter the index of the item you want to graph (or 'q' to quit): ")
            if index_str.lower() == 'q':
                continue
            else:
                try:
                    index = int(index_str)
                    item = get_item_by_index(index)
                    if item is not None:
                        name, _ = item
                        plot_item_price_graph(name)
                    else:
                        print(f"Invalid index. Please enter an index between 0 and {len(tracked_items) - 1}.")
                except ValueError:
                    print("Invalid input. Please enter a valid index or 'q' to quit.")
        elif action == 'q':
            break
        else:
            print("Invalid input. Please enter 'a', 'r', 'g', or 'q'.")

    while True:
        display_tracked_items()
        time.sleep(120)  # Sleep for an hour before checking again