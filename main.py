import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import platform
import streamlit as st

SHEETY_ENDPOINT = "https://api.sheety.co/d6b82e9c05bc37bf12c02605d8f5dd44/groceries/groceries"

# for root, dirs, files in os.walk("/"):
#     for name in files:
#         if "chromium" in name or "chromedriver" in name:
#             st.write(os.path.join(root, name))

sheety = requests.get(SHEETY_ENDPOINT, verify=False)
sheety_list = sheety.json()["groceries"]
# print(sheety_list)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)    # didn't work to keep browser open anyway

chrome_options = Options()
# chrome_options.add_argument("--headless") runs Chrome invisibly in the background
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

system = platform.system()

if system == 'Windows':
# Local Windows setup
    driver_path = os.path.join(os.path.dirname(__file__), "chromedriver-win64", "chromedriver.exe")
    service = Service(driver_path)
elif system == 'Linux':
# Streamlit Cloud or local Linux
    chrome_options.binary_location = '/usr/bin/chromedriver'
    service = Service('/usr/bin/chromium')
else:
    raise Exception(f"Unsupported OS: {system}")

driver = webdriver.Chrome(service=service, options=chrome_options)


for store in ["sixty", "ww"]:

    driver.get("https://www.checkers.co.za/" if store == "sixty" else "https://www.woolworths.co.za/dept/Food/_/N-1z13sk5")

    # sign_in = driver.find_element(By.CLASS_NAME, "profile-avatar_profile-avatar__edTU8")
    # sign_in.click()

    # sign_in_2 = driver.find_element(By.CSS_SELECTOR, ".button_profile-menu-item___CNYr span")
    # sign_in_2.click()

    # phone_no = driver.find_element(By.CLASS_NAME, "phone-input_phone-input__jHqh5") 
    # phone_no.send_keys("795052593")

    # sleep(10)

    # lets_go = driver.find_element(By.CLASS_NAME, "verify_button-primary__A9Zi8") 
    # lets_go.click()    
    
    sleep(30) # allow time for manual login so that the address can be used for nearest store and thus stock availability

    for item in sheety_list[0: len(sheety_list)-1]:
        search_bar = (  driver.find_element(By.CLASS_NAME, "search_input__kRTmL") if store == "sixty" 
                        else driver.find_element(By.ID, "cio-autocomplete-0-input"))
        search_bar.clear()
        search_bar.send_keys(item["item"])
        search_bar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "search_input__kRTmL")) if store == "sixty" else EC.element_to_be_clickable((By.ID, "cio-autocomplete-0-input")))
        search_bar.send_keys(Keys.ENTER)

        sleep(5)

        topN = item["considerTopNItems"] #precision of search text will affect relevance
        # wait = WebDriverWait(driver, 10)
        # topresults = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card_card__DsB3_ a")))
        topresults = [item.get_attribute("href") for item in 
                      (driver.find_elements(By.CSS_SELECTOR, ".product-card_card__DsB3_ a") if store == "sixty" 
                        else driver.find_elements(By.CLASS_NAME, "product--view"))][0:topN]
        topresults_prices = [float(item.text.split('R')[1]) for item in 
                             driver.find_elements(By.CLASS_NAME, "price-display_full__ngphI" if store == "sixty" else "price")][0:topN]
        if len(topresults) > 0:
            cheapest_price = min(topresults_prices)
            cheapest_result = topresults[topresults_prices.index(cheapest_price)]
            update_json = {
                "grocery":{
                    f"{store}CheapestPrice": int(cheapest_price),
                    f"{store}CheapestLink": cheapest_result,
                }
            }
        else:
            update_json = {
                "grocery":{
                    f"{store}CheapestPrice": "None",
                    f"{store}CheapestLink": "None",
                }
            }
        response = requests.put(f"{SHEETY_ENDPOINT}/{item["id"]}", json=update_json, verify=False)








