from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Chrome()

driver.get("https://en.wikipedia.org/wiki/Main_Page")

print(driver.find_element(By.XPATH,value='//*[@id="articlecount"]/a[1]').text)



