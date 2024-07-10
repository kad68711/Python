from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
import time





response=requests.get("https://appbrewery.github.io/Zillow-Clone/")

soup=BeautifulSoup(response.text,'html.parser')

price_list=soup.select('.PropertyCardWrapper__StyledPriceLine')
filtered_price_list=[price.text.strip('+/bdmo 1') for price in price_list]

print(filtered_price_list)

address_list=soup.select('address[data-test="property-card-addr"]')
filtered_address_list=[address.text.strip() for address in address_list]

print(filtered_address_list)

address_link=soup.select('a[data-test="property-card-link"]')
filtered_address_link=[link['href'] for link in address_link]

print(filtered_address_link)


options=webdriver.ChromeOptions()
options.add_argument("--incognito")




for i in range(0,len(price_list)):

    

    driver=webdriver.Chrome(options=options)

    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSeyyhK9AIsZiM_aZAaPOHpFUBVPIaRH5czHN_Q5TK461cht9g/viewform?usp=sf_link')

    time.sleep(4)


    address=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.click()
    address.send_keys(filtered_address_list[i])
    price=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.click()
    price.send_keys(filtered_price_list[i])
    link=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.click()
    link.send_keys(filtered_address_link[i])

    button=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    button.click()

