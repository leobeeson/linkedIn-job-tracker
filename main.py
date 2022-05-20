import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration.git
webdriver_service = Service("/usr/local/bin/chromedriver/stable/chromedriver")

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get page
driver.get("https://www.linkedin.com/jobs/")

recommended = driver.find_element(By.CSS_SELECTOR, "#ember1541").get_attribute("href")
print(f"{recommended}")

time.sleep(5)
driver.quit()