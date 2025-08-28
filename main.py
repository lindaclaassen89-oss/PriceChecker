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
import logging

SHEETY_ENDPOINT = "https://api.sheety.co/d6b82e9c05bc37bf12c02605d8f5dd44/groceries/groceries"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"\n\nApp   loaded    at: {datetime.datetime.now()}\n\n")

if "init_time" not in st.session_state:
    st.session_state.init_time = datetime.datetime.now()
logger.info(f"\n\nSession started at: {datetime.datetime.now()}\n\n")

if "run_nr" not in st.session_state:
    st.session_state.run_nr = 1
else:
    st.session_state.run_nr += 1
logger.info(f"\n\nSession run_nr: {st.session_state.run_nr}\n\n")

sheety = requests.get(SHEETY_ENDPOINT, verify=False)
sheety_list = sheety.json()["groceries"]
# print(sheety_list)

def get_linux_driver():
    # Detect paths
    driver_path = subprocess.run(['which', 'chromedriver'], capture_output=True, text=True).stdout.strip()
    browser_path = subprocess.run(['which', 'chromium'], capture_output=True, text=True).stdout.strip()

    if not driver_path or not browser_path:
        st.error("❌ Could not find chromedriver or chromium in PATH.")
        return None

    # Set up options
    chrome_options = Options()
    chrome_options.binary_location = browser_path
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36")

    # Optional: ensure /tmp is writable
    if not os.access("/tmp", os.W_OK):
        st.warning("⚠️ /tmp is not writable. Chromium may fail to launch.")

    # Launch driver
    try:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        st.error("🚨 Failed to launch Chromium")
        st.exception(e)
        return None
    

def get_driver_for_os():
    system = platform.system().lower()
    if system == 'windows':
    # Local Windows setup
        driver_path = os.path.join(os.path.dirname(__file__), "chromedriver-win64", "chromedriver.exe")
        service = Service(driver_path)
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=service, options=chrome_options)
    elif system == 'linux':
    # Streamlit Cloud or local Linux
        return get_linux_driver()
    else:
        raise Exception(f"Unsupported OS: {system}")
    

# User profile:
user_cell_no = "795052593"
user_dob = "29/12/1989"
user_email = "paulw.claassen@gmail.com"
user_pw = "Affies2007"


if "store" not in st.session_state: # for loop through stores doesn't work, because we can't save the browser's position in "driver"
    st.session_state.store = "sixty"
# the else is set after the whole Sixty run (line 240-ish)
store = st.session_state.store
logger.info(f"{store.upper()} {store.upper()} {store.upper()} {store.upper()} {store.upper()} {store.upper()} {store.upper()}")


if store == "sixty" and "driverSixty" not in st.session_state: # Streamlit is reactive, meaning it automatically reruns your script from top to bottom every time a user interacts with a widget, so only run the OTP navigation and text_input the first time
    logger.info(f"\n\nDriver not in st.session_state: {datetime.datetime.now()} Run_nr: {st.session_state.run_nr}\n\n")

    driver = get_driver_for_os()
    st.session_state.driverSixty = driver
    driver.get("https://www.checkers.co.za/") 
    wait = WebDriverWait(driver, 10)

    # JS so that headless mode can work
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2) # give JS time to react
    
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    driver.save_screenshot("debug1"+store+".png")
    if store == "sixty":
        image1sixty = Image.open("debug1"+store+".png")
        st.image(image1sixty, caption="Screenshot before sign_in", use_container_width=True)
    else:
        image1Ww = Image.open("debug1"+store+".png")
        st.image(image1Ww, caption="Screenshot before sign_in", use_container_width=True)
    # st.write(driver.page_source)

    # Login so that the address can be used for nearest store and thus stock availability:

    sign_in = wait.until(
        lambda d:   EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'profile-avatar')]"))(d) and
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'profile-avatar')]"))(d)
        )
    sign_in.click()

    sign_in_2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button_profile-menu-item___CNYr span")))
    sign_in_2.click()

    phone_no = driver.find_element(By.CLASS_NAME, "phone-input_phone-input__jHqh5") 
    phone_no.send_keys(user_cell_no)

    lets_go = driver.find_element(By.CLASS_NAME, "verify_button-primary__A9Zi8") 
    lets_go.click() 


if store == "sixty" and "otp" not in st.session_state: # WW doesn't require OTP
    
    logger.info(f"\n\nOtp not in st.session_state: {datetime.datetime.now()} Run_nr: {st.session_state.run_nr}\n\n")
    
    otp = st.text_input("Please input OTP sent to 0" + user_cell_no + ":")
    # otp = input("Please input OTP sent to 0" + user_cell_no + ":")

    if otp: # first run it'll be blank
        st.session_state.otp = otp # manually rather than using "key" in text_input so that we can control the flow
        logger.info(f"\n\nOTP {otp} added to st.session_state: {datetime.datetime.now()} Run_nr: {st.session_state.run_nr}\n\n")


def search_items(store, driver, wait):
    # if store == "sixty": 
        # modal = driver.find_element(By.ID, "tw-modal")
        # wait.until(EC.staleness_of(modal))
    search_bar = (wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.search_input__kRTmL"))) if store == "sixty" 
                    else wait.until(EC.element_to_be_clickable((By.ID, "cio-autocomplete-0-input"))))
    sleep(5) # prevents send_keys's ElementNotInteractableException - above modal staleness only works for first iteration and still not always
    for item in sheety_list[0: len(sheety_list)-1]:
        search_bar.clear()
        search_bar.send_keys(item["item"])
        search_bar.send_keys(Keys.ENTER)

        topN = item["considerTopNItems"] #precision of search text will affect relevance
        sleep(3) # prevents below line's StaleElementReferenceException
        topresults = [item.get_attribute("href") for item in 
                        (wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card_card__DsB3_ a"))) if store == "sixty" 
                            else wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product--view"))))][0:topN]
        topresults_prices = [float(item.text.split('R')[1]) for item in 
                            driver.find_elements(By.CLASS_NAME, "price-display_full__ngphI" if store == "sixty" else "price")][0:topN]
        if len(topresults) > 0:
            cheapest_price = min(topresults_prices)
            cheapest_result = topresults[topresults_prices.index(cheapest_price)]
            update_json = {
                "grocery":{
                    f"{store}CheapestPrice": int(cheapest_price),
                    f"{store}CheapestLink": cheapest_result,
                    "datetimeUpdated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
            }
        else:
            update_json = {
                "grocery":{
                    f"{store}CheapestPrice": "None",
                    f"{store}CheapestLink": "None",
                    "datetimeUpdated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
            }
        response = requests.put(f"{SHEETY_ENDPOINT}/{item["id"]}", json=update_json, verify=False)


if store == "sixty" and "otp" in st.session_state and "driverSixty" in st.session_state:
    
    logger.info(f"\n\nBoth driver and OTP in st.session_state: {datetime.datetime.now()} Run_nr: {st.session_state.run_nr}\n\n")
    
    driver = st.session_state.driverSixty
    otp = st.session_state.otp

    driver.save_screenshot("debug2.png")
    image2 = Image.open("debug2.png")
    st.image(image2, caption="Screenshot before OTP_inputs", use_container_width=True)
    # st.write(driver.page_source)

    OTP_inputs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "otp-input_otp-input__yxfQO")))

    st.write(len(OTP_inputs))

    OTP_inputs[0].send_keys(otp[0])
    OTP_inputs[1].send_keys(otp[1])
    OTP_inputs[2].send_keys(otp[2])
    OTP_inputs[3].send_keys(otp[3])
    OTP_inputs[3].send_keys(Keys.TAB + Keys.ENTER)

    # DOB_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".input.input_input__qgb6Z")))
    DOB_input = wait.until(
            lambda d:   EC.presence_of_element_located((By.XPATH, '//*[@id="tw-modal"]/div/div/div/div[1]/div/form/div[1]/div/input'))(d) and
                        EC.visibility_of_element_located((By.XPATH,'//*[@id="tw-modal"]/div/div/div/div[1]/div/form/div[1]/div/input'))(d)
        )
    DOB_input.send_keys(user_dob)
    DOB_input.send_keys(Keys.TAB + Keys.ENTER)

    search_items(store, driver, wait)

    st.session_state.store = "ww"
    store = "ww"


if st.session_state.store == "ww": # should only run once after all of the above
    logger.info(f"{store.upper()} {store.upper()} {store.upper()} {store.upper()} {store.upper()} {store.upper()} {store.upper()}")
    logger.info(f"\n\nand thus Driver not in st.session_state: {datetime.datetime.now()} Run_nr: {st.session_state.run_nr}\n\n")

    driver = get_driver_for_os()
    # st.session_state.driver = driver
    driver.get("https://www.woolworths.co.za/dept/Food/_/N-1z13sk5")
    wait = WebDriverWait(driver, 10)

    # JS so that headless mode can work
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2) # give JS time to react
    
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    driver.save_screenshot("debug1"+store+".png")
    if store == "sixty":
        image1sixty = Image.open("debug1"+store+".png")
        st.image(image1sixty, caption="Screenshot before sign_in", use_container_width=True)
    else:
        image1Ww = Image.open("debug1"+store+".png")
        st.image(image1Ww, caption="Screenshot before sign_in", use_container_width=True)
    # st.write(driver.page_source)

    # Login so that the address can be used for nearest store and thus stock availability:

    sign_in = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".signInLabelLogin span")))
    sign_in.click()

    email = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".email-address input")))
    email.send_keys(user_email)

    email = driver.find_element(By.ID, "fldPasswordSml")
    email.send_keys(user_pw)

    sign_in_2 = driver.find_element(By.ID, "login")
    sign_in_2.click()

    search_items(store, driver, wait)
