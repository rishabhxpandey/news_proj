from twilio.rest import Client
from dotenv import load_dotenv
import os
import requests
import random
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("API_KEY")
TWILIO_SID= os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
PERSONAL_NUMBER = os.getenv("PERSONAL_NUMBER")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

class News():
    def __init__(self):
        self.top_5 = []
        self.text = ""

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
    formatted_text = ""
    for item in news_list:
        formatted_text += item + "\n"
    return formatted_text
    '''
    for item in news_list:
        news.text += item + "\n"
    print(news.text)
    '''

def send(SID:str, auth:str, formatted_news:str):
    client = Client(SID, auth)
    client.messages.create(
        to = PERSONAL_NUMBER,
        from_ = TWILIO_NUMBER,
        body = formatted_news
    )

def log(content):
    with open('log.txt', 'a') as file:
        # Write the content to the file.
        file.write(content)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    news = News()
    try: 
        fetch_news(API_KEY)

        # Print news output in console
        formatted_news = prettify(news.top_5)
        print(formatted_news)  
        
        # Send the text
        # send(TWILIO_SID, TWILIO_AUTH_TOKEN, formatted_news)

        # Make log of news sent
        log("NEW LOG---------------" + str(datetime.now())[:19] + "\n" +
            "\n".join(news.top_5) + "\n")
    
    # Catch if there are any exceptions
    except Exception as e:
        print(f"Error: {e}")

'''
### IDEAS ###
--for daily run
# use azure functions instead of cronjob
--for signups
# make webapp where people can enter phone number to sign up
# allow people to text a number to sign up
--for news selection
# allow people to choose a country and news genre
'''