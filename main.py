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
import subprocess
from PIL import Image
import datetime

print("\n\nApp   loaded   at:", datetime.datetime.now(), "\n\n")

if "init_time" not in st.session_state:
    st.session_state.init_time = datetime.datetime.now()
    print("\n\nSession started at:", st.session_state.init_time, "\n\n")

# SHEETY_ENDPOINT = "https://api.sheety.co/d6b82e9c05bc37bf12c02605d8f5dd44/groceries/groceries"

# sheety = requests.get(SHEETY_ENDPOINT, verify=False)
# sheety_list = sheety.json()["groceries"]
# # print(sheety_list)

# def get_linux_driver():
#     # Detect paths
#     driver_path = subprocess.run(['which', 'chromedriver'], capture_output=True, text=True).stdout.strip()
#     browser_path = subprocess.run(['which', 'chromium'], capture_output=True, text=True).stdout.strip()

#     if not driver_path or not browser_path:
#         st.error("❌ Could not find chromedriver or chromium in PATH.")
#         return None

#     # Set up options
#     chrome_options = Options()
#     chrome_options.binary_location = browser_path
#     chrome_options.add_argument("--headless=new")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--window-size=1920,1080")
#     chrome_options.add_argument("--remote-debugging-port=9222")
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36")

#     # Optional: ensure /tmp is writable
#     if not os.access("/tmp", os.W_OK):
#         st.warning("⚠️ /tmp is not writable. Chromium may fail to launch.")

#     # Launch driver
#     try:
#         service = Service(driver_path)
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#         return driver
#     except Exception as e:
#         st.error("🚨 Failed to launch Chromium")
#         st.exception(e)
#         return None


# system = platform.system().lower()

# if system == 'windows':
# # Local Windows setup
#     driver_path = os.path.join(os.path.dirname(__file__), "chromedriver-win64", "chromedriver.exe")
#     service = Service(driver_path)
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(service=service, options=chrome_options)
# elif system == 'linux':
# # Streamlit Cloud or local Linux
#     driver = get_linux_driver()
# else:
#     raise Exception(f"Unsupported OS: {system}")


# # User profile:
# cell_no = "795052593"
# dob = "29/12/1989"


# for store in ["sixty", "ww"]:

#     driver.get("https://www.checkers.co.za/" if store == "sixty" else "https://www.woolworths.co.za/dept/Food/_/N-1z13sk5")

#     # JS so that headless mode can work
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     sleep(2) # give JS time to react


#     # Login so that the address can be used for nearest store and thus stock availability:
    
#     WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

#     if "OTP" not in st.session_state: # Streamlit is reactive, meaning it automatically reruns your script from top to bottom every time a user interacts with a widget
        
#         driver.save_screenshot("debug.png")
#         image = Image.open("debug.png")
#         st.image(image, caption="Screenshot before sign_in", use_container_width=True)
#         # st.write(driver.page_source)

#         sign_in = WebDriverWait(driver, 20).until(
#             lambda d:   EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'profile-avatar')]"))(d) and
#                         EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'profile-avatar')]"))(d)
#             )
#         # sign_in.click()

#         sign_in_2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_profile-menu-item___CNYr span")))
#         sign_in_2.click()

#         phone_no = driver.find_element(By.CLASS_NAME, "phone-input_phone-input__jHqh5") 
#         phone_no.send_keys(cell_no)

#         lets_go = driver.find_element(By.CLASS_NAME, "verify_button-primary__A9Zi8") 
#         lets_go.click()    

#         # Text input using session state
#         st.write("Creating text_input")
#         st.text_input("Please input OTP sent to 0" + cell_no + ":", key="OTP")
#         st.write("Created text_input")

#         sleep(30) # give the user a chance before rerunning script

#         OTP = st.session_state.OTP
#         st.write(OTP)

#         #OTP = input("Please input OTP sent to 0" + cell_no + ":")

#         driver.save_screenshot("debug.png")
#         image = Image.open("debug.png")
#         st.image(image, caption="Screenshot before OTP_inputs", use_container_width=True)
#         # st.write(driver.page_source)

#         OTP_inputs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "otp-input_otp-input__yxfQO")))

#         st.write(len(OTP_inputs))

#         OTP_inputs[0].send_keys(OTP[0])
#         OTP_inputs[1].send_keys(OTP[1])
#         OTP_inputs[2].send_keys(OTP[2])
#         OTP_inputs[3].send_keys(OTP[3])
#         OTP_inputs[3].send_keys(Keys.TAB + Keys.ENTER)

#         # DOB_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".input.input_input__qgb6Z")))
#         DOB_input = WebDriverWait(driver, 20).until(
#                 lambda d:   EC.presence_of_element_located((By.XPATH, '//*[@id="tw-modal"]/div/div/div/div[1]/div/form/div[1]/div/input'))(d) and
#                             EC.visibility_of_element_located((By.XPATH,'//*[@id="tw-modal"]/div/div/div/div[1]/div/form/div[1]/div/input'))(d)
#             )
#         DOB_input.send_keys(dob)
#         DOB_input.send_keys(Keys.TAB + Keys.ENTER)


#     for item in sheety_list[0: len(sheety_list)-1]:
#         search_bar = (  driver.find_element(By.CLASS_NAME, "search_input__kRTmL") if store == "sixty" 
#                         else driver.find_element(By.ID, "cio-autocomplete-0-input"))
#         search_bar.clear()
#         search_bar.send_keys(item["item"])
#         search_bar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "search_input__kRTmL")) if store == "sixty" else EC.element_to_be_clickable((By.ID, "cio-autocomplete-0-input")))
#         search_bar.send_keys(Keys.ENTER)

#         sleep(5)

#         topN = item["considerTopNItems"] #precision of search text will affect relevance
#         # wait = WebDriverWait(driver, 10)
#         # topresults = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card_card__DsB3_ a")))
#         topresults = [item.get_attribute("href") for item in 
#                     (driver.find_elements(By.CSS_SELECTOR, ".product-card_card__DsB3_ a") if store == "sixty" 
#                         else driver.find_elements(By.CLASS_NAME, "product--view"))][0:topN]
#         topresults_prices = [float(item.text.split('R')[1]) for item in 
#                             driver.find_elements(By.CLASS_NAME, "price-display_full__ngphI" if store == "sixty" else "price")][0:topN]
#         if len(topresults) > 0:
#             cheapest_price = min(topresults_prices)
#             cheapest_result = topresults[topresults_prices.index(cheapest_price)]
#             update_json = {
#                 "grocery":{
#                     f"{store}CheapestPrice": int(cheapest_price),
#                     f"{store}CheapestLink": cheapest_result,
#                 }
#             }
#         else:
#             update_json = {
#                 "grocery":{
#                     f"{store}CheapestPrice": "None",
#                     f"{store}CheapestLink": "None",
#                 }
#             }
#         response = requests.put(f"{SHEETY_ENDPOINT}/{item["id"]}", json=update_json, verify=False)




