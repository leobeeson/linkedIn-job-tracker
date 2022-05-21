import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import os
from dotenv import load_dotenv


load_dotenv()
ENTITY = os.environ.get("ENTITY")
OTHER = os.environ.get("OTHER")


# Set path to chromedriver as per your configuration.git
webdriver_service = Service("C:\Drivers\chromedriver.exe")

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service)

# Get page
# driver.get("https://www.linkedin.com/jobs/")
# Remote/Scotland/python%20developer
driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&f_WT=2&geoId=100752109&keywords=python%20developer&location=Scotland%2C%20United%20Kingdom")

log_in = driver.find_element(By.LINK_TEXT, "Sign in")
log_in.click()

entity = driver.find_element(By.ID, "username")
entity.send_keys(ENTITY)

other = driver.find_element(By.ID, "password")
other.send_keys(OTHER)
other.send_keys(Keys.ENTER)


time.sleep(60)
driver.quit()