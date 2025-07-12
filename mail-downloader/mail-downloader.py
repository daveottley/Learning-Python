import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True

# Create a Firefox profile and set preferences
profile = webdriver.FirefoxProfile()
download_dir = "/Downloads/old_mail"
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.dir", download_dir)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf, application/octet-stream")

# Attach the profile to the options
options.profile = profile

driver = webdriver.Firefox(options=options)

try:
    driver.get("https://texasregisteredagent.net/client-login/")
    driver.find_element(By.ID, "email_address").send_keys("properties@daveottley.com")
    driver.find_element(By.ID, "password").send_keys("Rainbow2021$")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit'].button").click()
    
    time.sleep(9)  # Wait for login to complete

    driver.get("https://accounts.texasregisteredagent.net/#/documents")
    per_page_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "perPageSelect"))
    )
    
    # Initialize the Select object
    select = Select(per_page_select)

    select.select_by_value("10000")

    rows = driver.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        try:
            # Locate the button with text 'View' inside the row using a relative XPath.
            view_button = row.find_element(By.XPATH, ".//button[contains(normalize-space(.), 'View')]")
            view_button.click()
            time.sleep(3) # Wait for page refresh (would like something more solid)

            download_button = driver.find_element(By.XPATH, "//button[.//text()[contains(normalize-space(.), 'Download')]]")
            download_button.click()
            time.sleep(3) # Wait for download to consumate
        except Exception as e:
            print("View button not found in this row:", e)
    
finally:
    driver.quit()

