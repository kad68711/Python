from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

driver.get("https://wynk.in/music")

driver.find_element(By.XPATH,value='//*[@id="__next"]/header/section[1]/div[2]/span/div').click()

time.sleep(5)


number=driver.find_element(By.NAME,value='phone')
number.click()
number.send_keys("9976898793")
time.sleep(2)


send=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit'][data-testid='loginSendOtpButton'].login_loginModalBtn__BVZOc")))
send.click()

otp=input("code recieved:  ")


otp_number=driver.find_element(By.NAME,value='phone')
otp_number.click()
otp_number.send_keys(otp)

time.sleep(5)

try:
    driver.find_element(By.XPATH,value='//*[@id="headlessui-dialog-:rm:"]/div/div[2]/div/div[2]/div[2]/form/div[3]/button[2]').click()
except:
    pass

with open("songs.txt") as f:
    songs=f.readlines()


time.sleep(3)

for song in songs:

    time.sleep(2)

    try:
        search=driver.find_element(By.CSS_SELECTOR,value="input[title='Search'][placeholder='Search Songs']")
        search.click()
        search.send_keys(song.strip())


        time.sleep(4)


        first_result=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.zapSearch_zapSearchItem__btvXc')))
        first_result.click()

        time.sleep(2)

        like=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'button.bg-white span.icon-ic_heart')))
        like.click()


    except:
        print(f"{song} wa nai")
