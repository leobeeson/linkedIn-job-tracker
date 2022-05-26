import time
import json
from urllib.parse import quote_plus

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


import os
from dotenv import load_dotenv


load_dotenv()
ENTITY = os.environ.get("ENTITY")
OTHER = os.environ.get("OTHER")



ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

# Functions
def wait_for_element(driver: WebDriver, class_name: str) -> WebElement:
    element = WebDriverWait(
        driver=driver,timeout=3,ignored_exceptions=ignored_exceptions
        ).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, class_name))
            )
    return element


# Set path to chromedriver as per your configuration.git
webdriver_service = Service("C:\Drivers\chromedriver.exe")

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service)


keyword_argument = "python developer"
keyword_url_safe = quote_plus(keyword_argument)

location_argument = "scotland, united kingdom"
location_url_safe = quote_plus(location_argument)

full_url = f"https://www.linkedin.com/jobs/search/?f_TPR=r604800&f_WT=2%2C3&keywords={keyword_url_safe}&location={location_url_safe}"

driver.get(full_url)
print(f"full_url: {full_url}")

log_in = driver.find_element(By.LINK_TEXT, "Sign in")
log_in.click()

entity = driver.find_element(By.ID, "username")
entity.send_keys(ENTITY)

other = driver.find_element(By.ID, "password")
other.send_keys(OTHER)
other.send_keys(Keys.ENTER)

driver.maximize_window()


pages = driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator")
print(f"Number of Pages: {len(pages)}")

listings_data = []

for page_num in range(1, len(pages) + 1):
    print(f"Page Number: {page_num}")
    listings = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
    num_listings = len(listings)
    print(f"Nunber of listings: {num_listings}")
    
    for idx, listing in enumerate(listings):
        listing_data = {}
        listing_data["page_number"] = page_num
        listing_data["results_position"] = idx

        listing = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")[idx]
        time.sleep(0.5)
        listing.click()
        time.sleep(0.5)
        
        job_id = listing.get_attribute("data-occludable-job-id")
        listing_data["job_id"] = job_id

        job_title_element = wait_for_element(listing, "job-card-list__title")
        job_title = job_title_element.text
        listing_data["job_title"] = job_title

        job_url = job_title_element.get_attribute("href")
        listing_data["job_url"] = job_url
        
        company_name_element = wait_for_element(listing, "job-card-container__company-name")
        company_name = company_name_element.text
        listing_data["company_name"] = company_name
        
        job_description_element = wait_for_element(driver, "jobs-description-content__text")
        job_description = job_description_element.text
        listing_data["job_description"] = job_description
        
        listings_data.append(listing_data)

    if page_num < len(pages):
        page_xpath = f"/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/section/div/ul/li[{page_num + 1}]/button"
        pagination = driver.find_element(By.XPATH, page_xpath)
        pagination.click()
        time.sleep(5)

date_prefix = time.strftime("%Y-%m-%d")

listings_data_filename = f"{date_prefix}_{keyword_url_safe}_{location_url_safe}.json"
with open(f"data/{listings_data_filename}", "w", encoding="utf-8") as f:
    json.dump(listings_data, f, ensure_ascii=False, indent=4)

time.sleep(60)
driver.quit()