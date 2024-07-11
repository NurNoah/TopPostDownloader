import praw
import requests
import schedule
import time
import json
import os

# Lese die Konfiguration aus der config.json-Datei
with open('config.json') as f:
    config = json.load(f)

# Reddit API Konfiguration
reddit = praw.Reddit(client_id=config['REDDIT_CLIENT_ID'],
                     client_secret=config['REDDIT_CLIENT_SECRET'],
                     user_agent=config['REDDIT_USER_AGENT'])

# Funktion zum Laden der heruntergeladenen Beiträge aus der Datei
def load_downloaded_posts():
    if os.path.exists('downloaded_posts.json'):
        with open('downloaded_posts.json', 'r') as f:
            return json.load(f)
    return []

# Funktion zum Speichern der heruntergeladenen Beiträge in eine Datei
def save_downloaded_posts():
    with open('downloaded_posts.json', 'w') as f:
        json.dump(downloaded_posts, f)

# Initialisiere die Liste mit bereits heruntergeladenen Beiträgen
downloaded_posts = load_downloaded_posts()

def download_top_post(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    
    for post in subreddit.new():
        if post.url not in downloaded_posts:
            url = post.url
            filename = url.split('/')[-1]
            
            response = requests.get(url)
            
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f'Downloaded {filename}')
                downloaded_posts.append(url)
                save_downloaded_posts()  # Speichern der Liste
            else:
                print('Failed to download the post')
            
        else:
            print(f'Post already downloaded: {post.url}')

download_top_post('OkBrudiMongo')
# Funktion einmal am Tag ausführen
#schedule.every().day.at("10:00").do(download_top_post, subreddit_name='OkBrudiMongo')

#while True:
#    schedule.run_pending()
#    time.sleep(60)  # Schlaf für eine Minute
