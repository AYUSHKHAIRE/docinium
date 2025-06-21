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
options.headless = True  # Set to False if you want to see the browser

# Launch Firefox with options
driver = webdriver.Firefox(options=options)

try:
    # Visit site
    driver.get("https://dev.to")
    logger.info("Opened https://dev.to")

    # Wait for page to load (simple wait; can use WebDriverWait for better practice)
    time.sleep(3)

    # Find the search field (new Selenium syntax using By)
    search_input = driver.find_element(By.ID, "nav-search")
    search_input.send_keys("Selenium")
    search_input.send_keys(Keys.ENTER)

    logger.info("Search performed successfully.")

finally:
    # Close the browser
    driver.quit()
    logger.info("Browser closed.")
