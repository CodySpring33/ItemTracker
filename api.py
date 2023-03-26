import time
import requests
import json
import urllib.parse
import db


def fetch_item_value(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    

    response = requests.get(url, headers=headers)

    if response.status_code == 429:
        print(f"Rate limit exceeded for the item at {url}. Retrying in 10 seconds...")
        time.sleep(10)
        return fetch_item_value(url)

    data = json.loads(response.content)
    price_element = data["lowest_price"]
    price = price_element.replace(",", "")
    
    if price:
        return price
    else:
        print(f"Could not fetch the price for the item at {url}.")
        return None
    
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
        db.add_item(item_name, url)
        print(f"Item '{item_name}' added successfully.")
    else:
        print(f"Item '{item_name}' not found.")