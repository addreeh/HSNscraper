#######################################################
#                                                     #
#                 HSNscrapper                         #
#                 Author: Adrián Pino                 #
#                                                     #
#######################################################

# Import necessary libraries for the script
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sys
import time

# Import libraries for handling environment variables and making HTTP requests
from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables from a .env file
load_dotenv()

# Retrieve user credentials and tokens from environment variables
userlogin = os.getenv('USERLOGIN')
password = os.getenv('PASSWORD')
token = os.getenv('TOKEN')
chat_ids_json = os.environ.get('HSN_CHAT_IDS')
chat_ids = json.loads(chat_ids_json)

# Define the Telegram API endpoint for sending messages
telegram_api_send_msg = f'https://api.telegram.org/bot{token}/sendMessage'

def telegramMSG(str):
    """
    Send a message to a Telegram chat using the Telegram Bot API.

    Args:
        str (str): The message to send.

    Returns:
        None
    """
    for chat_id in chat_ids:
        data = {
            'chat_id': chat_id,
            'text': f'{str}',
            'parse_mode': 'Markdown'
        }

        r = requests.post(telegram_api_send_msg, data=data)

def login(driver):
    """
    Perform a login action on a website using the provided Selenium WebDriver.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        None
    """
    try:
        driver.get('https://www.hsnstore.com/customer/account/login/')
        driver.find_element(By.CSS_SELECTOR, 'input[name="login[username]"]').send_keys(userlogin)
        driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button#send2.btn.btn-orange-transparent.customligin_button').click()
    except Exception as e:
        msg = (f"Error in login: {e}")
        print(msg)
        # telegramMSG(msg)
        sys.exit()

def get_data():
    """
    Scrape data from a website, extract product information, and return it as a list of dictionaries.

    Returns:
        list: A list of product dictionaries containing 'name', 'price', and 'url'.
              Returns None on error.
    """
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

        login(driver)

        driver.get("https://www.hsnstore.com/checkout/cart/")
        time.sleep(10)

        products = []

        product1 = {
            "name": driver.find_element(By.CSS_SELECTOR, "div.item:nth-of-type(1) .product-name a").text.upper().split(" - ")[0],
            "price": driver.find_element(By.CSS_SELECTOR, 'div.item:nth-of-type(1) .col-sm-7 span.price').text.replace(" ", ""),
            "url": "https://www.hsnstore.com/marcas/sport-series/evowhey-protein-2-0-2kg-chocolate"
        }
        products.append(product1)

        product2 = {
            "name": driver.find_element(By.CSS_SELECTOR, "div:nth-of-type(2) .product-name a").text.upper().split(" - ")[0],
            "price": driver.find_element(By.CSS_SELECTOR, 'div:nth-of-type(2) .col-xs-12 .col-xs-12 .cart-price span').text.replace(" ", ""),
            "url": "https://www.hsnstore.com/marcas/sport-series/evocasein-2-0-caseina-micelar-digezyme-2kg-chocolate"
        }
        products.append(product2)

        driver.quit()

        return products
    except Exception as e:
        msg = (f"Error while fetching data: {e}")
        print(msg)
        # telegramMSG(msg)
        return None
        sys.exit()

if __name__ == '__main__':
    try:
        # Fetch product data from a website
        products = get_data()

        # Iterate through the list of products
        for product in products:
            product_name = product["name"]
            product_price = product["price"]
            product_url = product["url"]
            brand = "HSN"
            # Check if product information is available
            if product_name and product_price and product_url:
                # Create a message to notify about the price
                msg = f"*{brand} |* [{product_name}]({product_url}) *| {product_price}*"
                print(msg)
                telegramMSG(msg)
    except Exception as e:
        # Handle exceptions and display an error message
        msg = (f"Error sending and/or storing the data: {e}")
        print(msg)
        # telegramMSG(msg)
        sys.exit()
