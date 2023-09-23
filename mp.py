#######################################################
#                                                     #
#                 MPscrapper                          #
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

# Import MongoDB library for database operations and datetime for date and time handling
import pymongo
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()

# Retrieve user credentials and tokens from environment variables
userlogin = os.getenv('USERLOGIN')
password = os.getenv('PASSWORD')
token = os.getenv('TOKEN')
chat_ids_json = os.environ.get('MP_CHAT_IDS')
chat_ids = json.loads(chat_ids_json)

# Define the Telegram API endpoint for sending messages
telegram_api_send_msg = f'https://api.telegram.org/bot{token}/sendMessage'

# Create a MongoDB client and connect to the local database
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Access the "webscrap" database within MongoDB
db = client["webscrap"]

# Access the "supple" collection within the database
collection = db["supple"]

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
        driver.get('https://www.myprotein.es/login.jsp?returnTo=https://www.myprotein.es/my.basket')
        driver.find_element(By.CSS_SELECTOR, 'input[type="email"]').send_keys(userlogin)
        driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
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
        driver.maximize_window()

        login(driver)

        time.sleep(10)

        products = []

        product1 = {
            "name": driver.find_element(By.CSS_SELECTOR, 'p.athenaBasket_itemName').text.upper().split(" - ")[0] + " 2,5KG",
            "price": driver.find_element(By.CSS_SELECTOR, 'div.athenaBasket_bodyItem.athenaBasket_bodyItem-subTotal').text.replace(" ", ""),
            "url": "https://www.myprotein.es/nutricion-deportiva/impact-whey-protein/10530943.html"
        }
        products.append(product1)

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
            brand = "MP"

            # Check if product information is available
            if product_name and product_price and product_url:
                # Check if the product already exists in the MongoDB collection
                doc = collection.find_one({"name": product_name})
                if doc:
                    # If the product exists, update its price and historical data
                    if doc["price"] != product_price:
                        # Retrieve the previous price from MongoDB
                        mongoPrice = doc["price"]

                        # Update the historical price and date data
                        historic = doc["historic"]
                        historic.append(product_price)
                        date = doc["date"]
                        date.append(datetime.now().strftime("%d/%m/%Y"))

                        collection.update_one({"_id": doc["_id"]}, {"$set": {"price": product_price, "historic": historic}})

                        # Convert prices to float for comparison
                        floatPrice = product_price.replace("€", "").replace(",", ".")
                        minPrice = doc["minPrice"]
                        floatMinPrice = minPrice.replace("€", "").replace(",", ".")
                        maxPrice = doc["maxPrice"]
                        floatMaxPrice = maxPrice.replace("€", "").replace(",", ".")

                        # Update the minimum and maximum prices if necessary
                        if float(floatPrice) < float(floatMinPrice):
                            collection.update_one({"_id": doc["_id"]}, {"$set": {"minPrice": product_price}})
                        elif float(floatPrice) > float(floatMaxPrice):
                            collection.update_one({"_id": doc["_id"]}, {"$set": {"maxPrice": product_price}})

                        # Create a message to notify about the price change
                        msg = f"*{brand} |* [{product_name}]({product_url}) *| {mongoPrice}* ➜ *{product_price}*"
                        if product_price == minPrice:
                            msg += "\n⚠️ *This is the lowest recorded price*"
                        elif float(floatPrice) > float(floatMaxPrice):
                            msg += "\n⛔️ *This is the highest recorded price*"
                            collection.update_one({"_id": doc["_id"]}, {"$set": {"maxPrice": product_price}})
                        print(msg)
                        telegramMSG(msg)
                else:
                    # If the product is new, insert it into the MongoDB collection
                    obj = {
                        "_id": collection.count_documents({}) + 1,
                        "brand": brand,
                        "name": product_name,
                        "price": product_price,
                        "minPrice": product_price,
                        "maxPrice": product_price,
                        "historic": [product_price],
                        "date": [datetime.now().strftime("%d/%m/%Y")]
                    }
                    collection.insert_one(obj)

                    # Create a message to notify about the new product
                    msg = (f"*{brand} |* [{product_name}]({product_url}) *| {product_price}*")
                    print(msg)
                    telegramMSG(msg)
    except Exception as e:
        # Handle exceptions and display an error message
        msg = (f"Error sending and/or storing the data: {e}")
        print(msg)
        # telegramMSG(msg)
        sys.exit()
