from logger_config import logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Log start
logger.info("Starting script...")

# Set headless mode (optional)
options = Options()
options.add_argument("--headless")  

# Launch Firefox with options
driver = webdriver.Firefox(options=options)

try:
    # Visit site
    driver.get("https://ayushkhaire.site")
    logger.info("Opened https://ayushkhaire.site")

    # Wait for page to load (simple wait; can use WebDriverWait for better practice)
    time.sleep(3)

    logger.info("title: %s", driver.title)

finally:
    # Close the browser
    driver.quit()
    logger.info("Browser closed.")