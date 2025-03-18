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

# Enhanced headers for Walmart CA scraping
walmart_headers = {
    "Host": "www.walmart.ca",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=0, i"
}

# Metro headers for proper scraping
metro_headers = {
    "Host": "www.metro.ca",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Priority": "u=0, i",
    "TE": "trailers"
}

# Food Basics headers for proper scraping
foodbasics_headers = {
    "Host": "www.foodbasics.ca",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "TE": "trailers"
}

# Updated URL patterns for Canadian retailers
retailer_urls = {
    "Walmart": "https://www.walmart.ca/search?q={}",
    # NOTE: loblaw's sites cannot be parsed without selenium
    # "Zehrs": "https://www.zehrs.ca/en/search?search-bar={}",
    # "NoFrills": "https://www.nofrills.ca/search?search-bar={}",
    "Metro": "https://www.metro.ca/en/online-grocery/search?filter={}",
    "Food Basics": "https://www.foodbasics.ca/search?filter={}"
}


simple_items = [
    "beef", "milk", "chicken", "eggs", "apples",
    "avocados", "mangoes", "corn", "white bread", "grapes"
]

items = [
    "Ground Beef", "Skim Milk", "Chicken breast", "Eggs", "Bag of Apples",
    "Bag of Avocados", "Box of Mangoes", "Canned Corn", "White bread", "Grapes"
]

retailers = [r for r, _ in retailer_urls.items()]


def scrape_dispatcher(r_name: str, item: str):
    encoded_item: str = item.replace(" ", "%20")
    search_url: str = retailer_urls[r_name].format(encoded_item)
    # print(f"scanning {search_url}")

    if r_name == "Walmart":
        return scrape_walmart_url(search_url)
    elif r_name == "Metro":
        return scrape_metro_url(search_url)
    elif r_name == "Food Basics":
        return scrape_fb_url(search_url)
    # elif r_name == "Zehrs":
    #     return scrape_zehrs_url(search_url)
    else:
        return scrape_price(r_name, item)  # otherwise fall back to other function


def scrape_walmart_url(search_url: str):
    response = requests.get(search_url, headers=walmart_headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_groups = soup.find_all('div', {'role': 'group'})

    for group in product_groups:
        last_group = group.previous
        if last_group is not None:
            to_cont = False
            flex_ctr_ctr = last_group.find('div', class_='mt5 mb0')
            if flex_ctr_ctr:
                flex_ctr = flex_ctr_ctr.find('div', class_='flex items-center lh-title h2-l normal')
                if flex_ctr:
                    flex = flex_ctr.find('div', class_='gray f7 flex items-center')
                    to_cont = True
            if to_cont:
                continue

        price_div = group.find('div', {'data-automation-id': 'product-price'}) # Find the price div within the product group

        if price_div:
            price_element = price_div.find('div', class_='mr1 mr2-xl b black lh-copy f5 f4-l')

            if price_element:
                price = price_element.text.strip()
                return price

    return -1


def scrape_metro_url(search_url: str):
    response = requests.get(search_url, headers=metro_headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the span with data-testid="regular-price"
    price_span = soup.find('span', {'class': 'price-update'})

    if price_span:
        return price_span.text.strip()

    return -1


def scrape_fb_url(search_url: str):
    response = requests.get(search_url, headers=foodbasics_headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the span with data-testid="regular-price"
    price_span = soup.find('span', {'class': 'price-update'})

    if price_span:
        return price_span.text.strip()

    return -1


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

if __name__ == "__main__": # only execute tests if this file is ran directly
    # List of items to compare
    retailers = [r for r, _ in retailer_urls.items()]

    for item in items:
        print(f"=== results for {item} ===")
        for r in retailers:
            result = scrape_dispatcher(r, item)
            print(f"price from {r}: {result}")
        print()
