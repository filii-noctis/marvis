import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Define Grocery Items to Search
grocery_items = ["Ground Beef", "Milk", "Chicken Breast", "Eggs", "Apples", 
                 "Avocado", "Mango", "Corn", "White Bread", "Baby Food"]

# Initialize a Dictionary for Storing Prices
grocery_prices = {item: {} for item in grocery_items}

# Set up Selenium WebDriver (Update ChromeDriver Path if Needed)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")

# lwklsdw
def scrape_walmart():
    base_url = "https://www.walmart.ca/search?q="
    
    for item in grocery_items:
        search_url = base_url + item.replace(" ", "+")
        driver.get(search_url)
        time.sleep(3)  # Wait for dynamic content to load

        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            product = soup.find("div", class_="css-1p3z9pl")  # Adjust class if needed
            if product:
                price = product.find("span", class_="css-2vqe5n").text.strip().replace("$", "")
                grocery_prices[item]["Walmart"] = float(price)
        except:
            grocery_prices[item]["Walmart"] = None

scrape_walmart()

def scrape_loblaws():
    base_url = "https://www.loblaws.ca/search?search-bar="
    
    for item in grocery_items:
        search_url = base_url + item.replace(" ", "%20")
        driver.get(search_url)
        time.sleep(3)

        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            product = soup.find("div", class_="product-tile__details")
            if product:
                price = product.find("span", class_="selling-price").text.strip().replace("$", "")
                grocery_prices[item]["Loblaws"] = float(price)
        except:
            grocery_prices[item]["Loblaws"] = None

scrape_loblaws()

def scrape_metro():
    base_url = "https://www.metro.ca/en/online-grocery/search?filter="

    for item in grocery_items:
        search_url = base_url + item.replace(" ", "%20")
        driver.get(search_url)
        time.sleep(3)

        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            product = soup.find("div", class_="product-item__details")
            if product:
                price = product.find("span", class_="regular-price").text.strip().replace("$", "")
                grocery_prices[item]["Metro"] = float(price)
        except:
            grocery_prices[item]["Metro"] = None

scrape_metro()
