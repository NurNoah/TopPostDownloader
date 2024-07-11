import praw
import requests
import schedule
import time
import json

with open('config.json') as f:
    config = json.load(f)
# Reddit API Konfiguration
reddit = praw.Reddit(client_id=config['REDDIT_CLIENT_ID'],
                     client_secret=config['REDDIT_CLIENT_SECRET'],
                     user_agent=config['REDDIT_USER_AGENT'])

def download_top_post(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    #top_post = next(subreddit.top(time_filter='day', limit=1))
    top_post = next(subreddit.new())
    url = top_post.url
    
    # Bestimmen des Dateinamens
    filename = url.split('/')[-1]
    
    # Download des Inhalts
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')
    else:
        print('Failed to download the top post')

download_top_post('OkBrudiMongo')
# Funktion einmal am Tag ausführen
#schedule.every().day.at("10:00").do(download_top_post, subreddit_name='OkBrudiMongo')

#while True:
#    schedule.run_pending()
#    time.sleep(60)  # Schlaf für eine Minute