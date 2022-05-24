import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


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
driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&f_TPR=r2592000&f_WT=2&geoId=100752109&keywords=python%20developer&location=Scotland%2C%20United%20Kingdom")

log_in = driver.find_element(By.LINK_TEXT, "Sign in")
log_in.click()

entity = driver.find_element(By.ID, "username")
entity.send_keys(ENTITY)

other = driver.find_element(By.ID, "password")
other.send_keys(OTHER)
other.send_keys(Keys.ENTER)

driver.maximize_window()

listings = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
num_listings = len(listings)
print(f"Nunber of listings: {num_listings}")

for idx, listing in enumerate(listings):
    print(f"\nJob Post #{idx}")
    listing = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")[idx]
    time.sleep(1)
    listing.click()
    time.sleep(1)
    job_title_element = WebDriverWait(
        listing, 
        3, 
        ignored_exceptions=(
            NoSuchElementException,
            StaleElementReferenceException)
            ).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "job-card-list__title"))
                )
    job_title = job_title_element.text
    print(f"job_title: {job_title}")
    company_name_element = WebDriverWait(
        listing, 
        3, 
        ignored_exceptions=(
            NoSuchElementException,
            StaleElementReferenceException)
            ).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "job-card-container__company-name"))
                )
    company_name = company_name_element.text
    print(f"company_name: {company_name}")
    job_description = driver.find_element(By.CLASS_NAME, "jobs-description-content__text").text
    print(f"job_description: {job_description}")
    # break

time.sleep(60)
driver.quit()