from selenium import webdriver
from selenium.webdriver.common.by import By


options=webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_experimental_option("detach",True)


driver=webdriver.Chrome(options=options)

driver.get('https://docs.google.com/forms/d/e/1FAIpQLSeyyhK9AIsZiM_aZAaPOHpFUBVPIaRH5czHN_Q5TK461cht9g/viewform?usp=sf_link')


address=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
address.click()
address.send_keys('kansas')
price=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
price.click()
price.send_keys('kansas')
link=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
link.click()
link.send_keys('kansas')

button=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
button.click()

