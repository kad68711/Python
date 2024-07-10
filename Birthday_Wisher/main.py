

import pandas
import datetime as dt
import random
import smtplib

kyo=str(dt.date.today())

kyo=kyo[5:]




data=pandas.read_csv("birthdays.csv")
list=data.to_dict(orient="records")
hidzuke=""
for _ in list:
    
    year=(_['year'])
    
    month=(_['month'])
    day=(_['day'])
    hidzuke=f"{month}-{day}"
    print(hidzuke)
    
    if hidzuke==kyo:
        with open(f"letter_templates/letter_{random.randint(1,3)}.txt") as f:
            content=f.read()
            content=content.replace("[NAME]",_['name'])
            

            user_mail="eabc@gmail.com" #replace these with your email and password
            passw="asegfarg"

            with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=user_mail,password=passw)
                    connection.sendmail(from_addr=user_mail,to_addrs="ttp544522@yahoo.com",msg=f"Subject:WISHES\n\n{content}")
                

