import requests
import urllib.parse
import db
import os
from dotenv import load_dotenv
import json
import aiohttp

load_dotenv()


async def fetch_item_value(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()

            if response.status == 429 or data["success"] == False:
                print(f"Rate limit exceeded. Displaying last known price instead.")
                return -1

            try:
                price_element = data["lowest_price"]
            except:
                print("Price not found, most likely no item of this type on the market")
                return None

            if os.getenv('CURRENCY') != '$':
                price = price_element.replace(",","")
                price = price.replace(" ", "")
            else:
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

    if response.status_code != 429:
        first_result = search_results["results"][0]
        item_hash_name = first_result["hash_name"]
        item_url = f"http://steamcommunity.com/market/priceoverview/?appid=730&currency={os.getenv('CODE')}&market_hash_name={urllib.parse.quote(item_hash_name)}"
        return item_url
    else:
        print(f"API Call Failed. Status Code:{response.status_code}")
        return None
    
def add_item_by_name(item_name):
    url = search_item_url(item_name)
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    name = urllib.parse.unquote(query['market_hash_name'][0])
    if url is not None:
        db.add_item(name, url)
        print(f"Item '{name}' added successfully.")
    else:
        print(f"Item '{item_name}' not found.")

def extract_hash(url):
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    return urllib.parse.quote(query['market_hash_name'][0])