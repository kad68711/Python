from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)


driver.get("https://orteil.dashnet.org/cookieclicker/")

wait = WebDriverWait(driver, 10)

language_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="langSelect-EN"]')))
language_button.click()


cokie = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="bigCookie"]')))


while True:
    cokie.click()

    extras = driver.find_elements(
        By.CSS_SELECTOR, value=".product.unlocked.enabled")
    print(extras)
    try:
        random_extra = random.choice(extras)
        random_extra.click()
    except:
        pass
