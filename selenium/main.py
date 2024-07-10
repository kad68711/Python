from selenium import webdriver
from selenium.webdriver.common.by import By

options=webdriver.ChromeOptions()
options.add_experimental_option("detach",True)


driver=webdriver.Chrome()
driver.get("https://www.python.org")


menu=driver.find_element(By.XPATH,value='//*[@id="content"]/div/section/div[3]/div[2]/div/ul')

dates=menu.find_elements(By.TAG_NAME,value="time")
venue=menu.find_elements(By.TAG_NAME,value="a")

dict={}
for i in range(len(dates)):
    
    dict[i]={"time":dates[i].text,"venue":venue[i].text}

print(dict)



driver.close()
driver.quit()