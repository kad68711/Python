import requests
import datetime

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
KEY="W2345sdgtTIZY44J7"
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

now=datetime.date.today()
todays_date=str( now )
yesterdays_date=str( now - datetime.timedelta(days=1))
daybefore_yesterdays_date= str(now - datetime.timedelta(days=2))



response=requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&outputsize=compact",headers={"apikey":KEY})
response.raise_for_status()

data=response.json()
print(data)


# if abs(int(float(data["Time Series (Daily)"][yesterdays_date]["1. open"]))-int(float(data["Time Series (Daily)"][daybefore_yesterdays_date]["1. open"])))==5:
#     get_news=True




# ## STEP 2: Use https://newsapi.org
# # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
# if get_news==True:
#     key="e67b2fqweger45149e032a203a"
#     response_for_news=requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={daybefore_yesterdays_date}&to={todays_date}&sortBy=popularity&apiKey={key}")
#     response_for_news.raise_for_status()

#     news_data=response_for_news.json()["articles"][:3]
    
#     article_titles=[i["title"] for i in news_data if i["title"]!='[Removed]']

#     print(article_titles)





# ## send email usign smtp

