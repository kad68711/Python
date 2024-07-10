import requests
from bs4 import BeautifulSoup
import dotenv
import os
import smtplib

dotenv.load_dotenv()


'''getting the price of the product'''
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9"

}
URL="https://www.amazon.com/dp/B01NBKTPTS?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
response=requests.get(url=URL,headers=header)



soup = BeautifulSoup(response.text,"html.parser")

price = soup.find(class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)

title = soup.find(id="productTitle").get_text().strip()


'''below code for sending mail'''

if price_as_float<200:
    message=f"Subject:Amazon price alert\n\n Price for {title} is {price_as_float} link for product is {URL}"
    with smtplib.SMTP(host="smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=os.getenv("user_mail"),password=os.getenv("passw"))
        connection.sendmail(from_addr=os.getenv("user_mail"),to_addrs=os.getenv("user_mail"),msg=message.encode("utf-8"))



