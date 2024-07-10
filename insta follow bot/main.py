from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time

load_dotenv()


options=webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
options.add_argument("--incognito")

driver=webdriver.Chrome(options=options)

driver.get("https://www.instagram.com")
time.sleep(5)

email=driver.find_element(By.XPATH,value='//*[@id="loginForm"]/div/div[1]/div/label/input')
email.click()
email.send_keys(os.getenv("mail"))

ps=driver.find_element(By.XPATH,value='//*[@id="loginForm"]/div/div[2]/div/label/input')
ps.click()
ps.send_keys(os.getenv("ps"))

driver.find_element(By.XPATH,value='//*[@id="loginForm"]/div/div[3]').click()

import time

time.sleep(15)

driver.get('https://www.instagram.com/chefsteps/followers/')



time.sleep(5)

popup=driver.find_element(By.CSS_SELECTOR,value='._aano')



for i in range(5):

  driver.execute_script('arguments[0].scrollTop=arguments[0].scrollHeight',popup)

time.sleep(5)
follow_button=driver.find_elements(By.CSS_SELECTOR,value="button._acan._acap._acas._aj1-._ap30")


for i in range(1,len(follow_button)):
  
  try:
    follow_button[i].click()
    time.sleep(2)
  except:
    driver.find_element(By.CSS_SELECTOR,value='class="_a9-- _ap36 _a9_1').click()


    






