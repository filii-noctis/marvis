import requests
from bs4 import BeautifulSoup
import re
import time
import random

# Common user-agent to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0"
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

# Updated URL patterns for Canadian retailers
retailer_urls = {
    "Walmart": "https://www.walmart.ca/search?q={}",
    "Zehrs": "https://www.zehrs.ca/en/search?search-bar={}",
    "NoFrills": "https://www.nofrills.ca/search?search-bar={}",
    "Metro": "https://www.metro.ca/en/online-grocery/search?filter={}",
    "Food Basics": "https://www.foodbasics.ca/search?filter={}"
}

def scrape_price(retailer_name, item):
    """
    Scrape the price for the given item from a retailer.
    Uses a simple regex to find price patterns like '$5.99'. If not found or on error,
    returns a dummy price.
    """
    # URL-encode the item by replacing spaces with %20
    encoded_item = item.replace(" ", "%20")
    search_url = retailer_urls[retailer_name].format(encoded_item)
    print(search_url)
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract all text and search for a price pattern like '$5.99'
        text = soup.get_text()
        match = re.search(r'\$\s?(\d+(?:\.\d{1,2})?)', text)
        if match:
            price = float(match.group(1))
            return price
        else:
            # If no price is found, return a dummy price (for demo purposes)
            dummy_price = round(random.uniform(1, 10), 2)
            print(f"[{retailer_name}] No price found for '{item}'. Using dummy price ${dummy_price}.")
            return dummy_price
    except Exception as e:
        print(f"[{retailer_name}] Error scraping '{item}': {e}")
        dummy_price = round(random.uniform(1, 10), 2)
        return dummy_price

# List of items to compare
items = [
    "Ground Beef", "Milk", "Chicken breast", "Eggs", "Apples", 
    "Avocado", "Mango", "Corn", "White bread", "Baby food"
]

# Dictionary to store prices per item; key=item, value=list of tuples (retailer, price)
results = {}

# Loop through each item and each retailer to get the prices
for item in items:
    results[item] = []
    print(f"\nScraping prices for: {item}")
    for retailer in retailer_urls:
        price = scrape_price(retailer, item)
        results[item].append((retailer, price))
        # Pause to reduce risk of being blocked
        time.sleep(1)

# Print the results in a simple table-like format
print("\n\n=== Price Comparison Results ===")
for item, price_list in results.items():
    # Determine the lowest price and corresponding retailer
    lowest = min(price_list, key=lambda x: x[1])
    print(f"\nItem: {item}")
    for retailer, price in price_list:
        print(f"  {retailer}: ${price}")
    print(f"-> Lowest price: ${lowest[1]} at {lowest[0]}")
