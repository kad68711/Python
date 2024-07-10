from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)

driver.get("https://orteil.dashnet.org/cookieclicker/")

wait = WebDriverWait(driver, 5)  # 5 seconds timeout

# Using a combination of By.ID and By.CSS_SELECTOR
language_button = wait.until(EC.presence_of_element_located((By.ID, 'langSelect-EN')))
language_button.click()
