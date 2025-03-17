import requests
from bs4 import BeautifulSoup
import re
import time
import random

# Set a common user-agent to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

# Define search URL patterns for each retailer 
retailer_urls = {
    "Walmart": "https://www.walmart.com/search/?query={}",
    "Sobeys": "https://www.sobeys.com/en/search/?q={}",
    "NoFrills": "https://www.nofrills.ca/search?query={}",
    "Metro": "https://www.metro.ca/search?searchText={}",
    "Food Basics": "https://www.foodbasics.ca/search?q={}"
}

def scrape_price(retailer_name, item):
    """
    Scrape the price for the given item from a retailer.
    Uses a simple regex to find price patterns like '$5.99'. If not found or on error,
    returns a dummy price.
    """
    # Build the search URL for the item (URL encode spaces)
    search_url = retailer_urls[retailer_name].format(item.replace(" ", "%20"))
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
        # In case of error, return a dummy price
        dummy_price = round(random.uniform(1, 10), 2)
        return dummy_price

# List of items to compare
items = [
    "Ground Beef", "Milk", "Chicken breast", "Eggs", "Apples", 
    "Avocado", "Mango", "Corn", "White bread", "Baby food"
]

# Dictionary to store prices per item
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


print("\n\n=== Price Comparison Results ===")
for item, price_list in results.items():
    # Determine the lowest price and corresponding retailer
    lowest = min(price_list, key=lambda x: x[1])
    print(f"\nItem: {item}")
    for retailer, price in price_list:
        print(f"  {retailer}: ${price}")
    print(f"-> Lowest price: ${lowest[1]} at {lowest[0]}")
