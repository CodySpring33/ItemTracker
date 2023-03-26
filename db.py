import sqlite3
import time
import os

DB_NAME = "csgo_items.db"
DB_DIR = os.path.join(os.getenv("APPDATA"), "csgoItemTracker")
DB_PATH = DB_PATH = os.path.join(DB_DIR, DB_NAME)

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items (name TEXT UNIQUE, url TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS item_prices (timestamp INTEGER, name TEXT, price REAL)")
        connection.commit()

def add_item(name, url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO items (name, url) VALUES (?, ?)", (name, url))
    conn.commit()
    conn.close()

def store_item_price(name, price):
    timestamp = int(time.time())
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO item_prices (timestamp, name, price) VALUES (?, ?, ?)", (timestamp, name, price))
        connection.commit()

def get_tracked_items():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    tracked_items = c.fetchall()
    conn.close()
    return tracked_items

def get_item_prices(name):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT timestamp, price FROM item_prices WHERE name=?", (name,))
        prices = cursor.fetchall()
    return prices

def get_previous_price(name):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT price FROM item_prices WHERE name=? ORDER BY timestamp DESC LIMIT 1", (name,))
        result = cursor.fetchone()
    return result[0] if result else None

def remove_item_by_index(index):
    tracked_items = get_tracked_items()
    if 0 <= index < len(tracked_items):
        item_name = tracked_items[index][0]
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM items WHERE name=?", (item_name,))
            cursor.execute("DELETE FROM item_prices WHERE name=?", (item_name,))
            connection.commit()
        print(f"Item '{item_name}' removed successfully.")
    else:
        print(f"Invalid index. Please enter an index between 0 and {len(tracked_items) - 1}.")

def swap_items(index1, index2):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT rowid, * FROM items")
    items = cursor.fetchall()

    if index1 < 0 or index2 < 0 or index1 > len(items) or index2 > len(items):
        print("Invalid indices. Please try again.")
        return

    item1 = items[index1]
    item2 = items[index2]

    cursor.execute("UPDATE items SET name=?, url=? WHERE rowid=?", ("TEMP", item2[2], item2[0]))
    cursor.execute("UPDATE items SET name=?, url=? WHERE rowid=?", (item2[1], item2[2], item1[0]))
    cursor.execute("UPDATE items SET name=?, url=? WHERE rowid=?", (item1[1], item1[2], item2[0]))

    conn.commit()
    conn.close()