from twilio.rest import Client
from dotenv import load_dotenv
import os
import requests
import random

load_dotenv()

API_KEY = os.getenv("API_KEY")
TWILIO_SID= os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
PERSONAL_NUMBER = os.getenv("PERSONAL_NUMBER")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")


class News():
    def __init__(self, top_5):
        self.top_5 = []
        self.text = ""

news = News(None)

def fetch_news(api_key, country='us', category=None):
    main_url = "https://newsapi.org/v2/top-headlines"
    query_params = {
        "apiKey": api_key,
        "country": country,
    }

    if category:
        query_params['category'] = category
    
    # fetching & printing data in json format
    res = requests.get(url=main_url, params=query_params)
    page = res.json()
    #print(json.dumps(page, indent=4))
    #print(page)
    
    article = page["articles"]

    trending_news = []
    for ar in article:
        trending_news.append(ar["title"])

    dirty_out = random.sample(trending_news, 5)
    news.top_5 = [f"{dirty_out.index(x) + 1}. {x}" for x in dirty_out]

def prettify(news_list:list):
    for item in news_list:
        news.text += item + "\n"
    print(news.text)
    

def send(SID:str, auth:str):
    client = Client(SID, auth)
    # message = 
    client.messages.create(
        to = PERSONAL_NUMBER,
        from_ = TWILIO_NUMBER,
        body = news.text
    )

if __name__ == '__main__':
    # print(PERSONAL_NUMBER)
    os.system('cls' if os.name == 'nt' else 'clear')
    fetch_news(API_KEY)
    prettify(news.top_5)
    send(TWILIO_SID, TWILIO_AUTH_TOKEN)
