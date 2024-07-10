from selenium import webdriver
from selenium.webdriver.common.by import By


options=webdriver.ChromeOptions()
options.add_experimental_option("detach",True)

driver=webdriver.Chrome(options=options)

driver.get("https://secure-retreat-92358.herokuapp.com/")

first_name=driver.find_element(By.XPATH,value="/html/body/form/input[1]")
first_name.send_keys("nnnnn")
last_name=driver.find_element(By.XPATH,value="/html/body/form/input[2]")
last_name.send_keys("iiiii")
email=driver.find_element(By.XPATH,value="/html/body/form/input[3]")
email.send_keys("jjjj@gmail.com")

button=driver.find_element(By.XPATH,value="/html/body/form/button")
button.click()



