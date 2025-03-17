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

Host: www.zehrs.ca
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
Cookie: NEXT_LOCALE=en; lcl_lang_pref=en; Origin_Session_Cookie=B; PCX_NEXT_ORIGIN=iceberg; akavpau_vp=1742252607~id=44f2c725898f35e49c7b047a9947222b; _abck=1A4C8EED9FB19E380A5FC44815559835~0~YAAQDJYqFwNHNZ2VAQAAlRNCpg18FmtZCEXxFgrmW/EuryXmfJNLj1sDlSCBHzLgCh9WL02NXdHSKSXcP8g0aUBwOI9YJS5uJA8kzd3z291CVWq+AHNtajtQFbeuKS4kYDH0XiHd+HPPpCJ568HEqMX+Nwa3VoKuvxcnhrZioMz7IymKINYp1hTTZPai0t5edBizZAMPU+0OTQWsY1YtVvT3tBrzrhV82MTRSctoNW01PA0zFWdMJpBhnpNR96LQ0iiJCVAc2V40CtsoYvUQwyRg60ZDJTF6Yb1QxUl86AitA93R4/e0r8fkuR+r/XLgxBk1FhWc4x+rM5XkJwR5PIIpz44SHk0CUmv0rLjoMtZkUATpOE9NCvCQAwTJTWpgKY9b/QwvTNGUwLIixizJZOp2Qv3ye03F3mtwINz0G8BRXURlMaxZZ3NFWxCRHfVpW9GzxUE/ShM7KhPG9QMgQBbUrNFddlkZ8ggoi+7jev2mobV8DUhh+jeenoE/iBCDjJqZNjlM1dPRvmSA1E3k1WVecYXqXY2oHtrFulztTCA8M3QrQQ==~-1~||0||~-1; ak_bmsc=1A8C6001B921BE09D6D9BFF52301BA8A~000000000000000000000000000000~YAAQDJYqF2MrNJ2VAQAAVxlAphvYN+Bqn8bLWIZ39vKVT7P5PEManiNYtKiHqYBUSlgK/FrxwfOJKakWvIuhD9U6QOwyaz39iO8UXzdJkG5wYDvgbgXRj02YrImCS6kKY8XM56E5oo09jQUPlg9RxEDcuIpypxIf536ezDd325VYlKIJqHUwq68WFG5fTJI8yjzYJBWw6disx6kziGVNqqgbi/2Z6FNbHboKsdvRZZVMdTPZuN+10HlSq6pQxXRT5Lha8XWBtXGWKyiWMJNDU3wYee4/pp7zk8fQ4udfJ6O3Xg2JsD2zyVAF+31HHfuZEnCfVY8QExUQ0b5raD6Gzcqc8GPokSmU5cb5Q9jbALkeiMU14SwiMAubkPey; bm_sz=AAA6BB720488EE205DB669636F4E7BCC~YAAQDJYqF2UrNJ2VAQAAVxlApht7u819g5RxMrtAUVyZMHOEjxhFAA+1Eq0p79Ro+v3kr21CJFFCAGppJ/Gd8qmgxETMRmfLh5vN3+fCFgwwwh6PPEtK97j4DL7CVlYlIyBtlLybrcWCvI0VVKEqhqX9dQFEs8Sep26LbWZ+o86tSlscxNBJcrF22irkKh5KE7O50CHkV22UFpu/8/dk/vxXK8n86POCG9IlJWA+He7/S6LJ84cDs7ZtNLxAZysd39RUSY2R15/16+q7jZnWfcgXyFTdKFc2v6/mawIH4RFZ5k/p9B8Z4g2PNAEppG9fgGoD8k2BOmJaF7x80BcXgWgErn6vkVuUh7idsA3bQGIkQdgbLwDucMJaqctpehLznQ==~3682870~3551287; PIM-SESSION-ID=kEyk0JDLZNwKEFGC; lastVisited=1742250973705; _spvid_ses.169e=*; _spvid_id.169e=344fb8f8-e229-4d51-a23a-787012eba378.1742250974.1.1742252722..31d567dd-651e-4b80-8089-7afcaeb61ec3..87d92451-ca1a-4e91-928c-442b4fea881b.1742250974440.33; forterToken=7cf69e6e8055488aa54a6305252fb4fb_1742250974452_14_dUAL43-mnts-a4_24ck_; customer_state=anonymous; bm_sv=F92A09C202CF987512E227D0BE41B9C7~YAAQBJYqF+0GZZiVAQAA3sZaphv3WwjrUu2qXwrSzELdSoHOeYjLwLRoTGedSWxjyvoF0HmwcI3LlDZKf2WV51/Ly+AZCxoqk0uG1SvZqz9C9W7if2NsgscIU+CMQfuoeOiBCC0IWiJPUjD+XeCiU8nEAqZpRJWpuF/ZWb4BgH9aG2KAiGppxk8ZyIleu4hNvvbAzbPIyqM/IV//sudxvc5qzvh7YPR528eDF5jAyoW8QpraSD4V7wXP783FGj8=~1; auto_store_selected=0525; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Mar+17+2025+18%3A38%3A27+GMT-0400+(Eastern+Daylight+Time)&version=202406.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=9eaaad3f-9429-4f07-9817-7aa0e76452c2&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&intType=1; OptanonAlertBoxClosed=2025-03-17T22:38:27.136Z
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Priority: u=0, i

# Updated URL patterns for Canadian retailers
retailer_urls = {
    "Walmart": "https://www.walmart.ca/search?q={}",
    "Zehrs": "https://www.zehrs.ca/en/search?search-bar={}",
    "NoFrills": "https://www.nofrills.ca/search?search-bar={}",
    "Metro": "https://www.metro.ca/en/online-grocery/search?filter={}",
    "Food Basics": "https://www.foodbasics.ca/search?filter={}"
}


def scrape_dispatcher(r_name: str, item: str):
    encoded_item: str = item.replace(" ", "%20")
    search_url: str = retailer_urls[r_name].format(encoded_item)
    # print(f"scanning {search_url}")

    if r_name == "Walmart":
        return scrape_walmart_url(search_url)
    elif r_name == "Zehrs":
        return scrape_zehrs_url(search_url)
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


def scrape_zehrs_url(search_url: str):
    response = requests.get(search_url, headers=walmart_headers, timeout=10)
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the span with data-testid="regular-price"
    price_span = soup.find('span', {'data-testid': 'regular-price'})
    
    if price_span:
        return price_span.text.strip()
    
    # Alternative approach if the above doesn't work
    price_span = soup.find('span', {'class': 'chakra-text css-pwnbcb'})
    
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
    items = [
        "Ground Beef", "Milk", "Chicken breast", "Eggs", "Apples",
        "Avocado", "Mango", "Corn", "White bread", "PlayStation 5"
    ]
    retailers = [r for r, _ in retailer_urls.items()]

    for item in items:
        print(f"=== results for {item}")
        for r in retailers:
            result = scrape_dispatcher(r, item)
            print(f"price from {r}: {result}")
