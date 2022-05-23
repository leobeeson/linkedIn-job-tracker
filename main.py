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

listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in listings:
    listing.click()
    job_title = listing.find_element(By.CLASS_NAME, "job-card-list__title").text
    company_name = listing.find_element(By.CLASS_NAME, "job-card-container__company-name").text
    print(f"job_title: {job_title} -> company_name: {company_name}\n")
    job_description = driver.find_element(By.CLASS_NAME, "jobs-description-content__text").text
    print(f"job_description: {job_description}")
    break

time.sleep(60)
driver.quit()