from mastodon import Mastodon
from bs4 import BeautifulSoup
import yaml
import sys
import langid
from time import sleep
import torch

## Load config details from YAML
def load_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print(error)
    return None

# pass the yaml-format config file as command-line argument
config = load_yaml(sys.argv[1])

# Set up Mastodon instance to listen on
mastodon = Mastodon(
    access_token = config['access_token'],
    api_base_url = config['masto_server']
)

# Set up topic model
from transformers import pipeline
mnli = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1", device=0 if torch.cuda.is_available() else -1)

# useful lil' function to get the text of a toot
def toot2text(status):
    toot_html = status['content']
    toot_soup = BeautifulSoup(toot_html, features="html.parser")
    toot_text = toot_soup.get_text()
    return(toot_text)

last_toot_id = None
while True:
    try:
        print("Checking for new toots...")
        recent_toots = mastodon.timeline_public(min_id=last_toot_id, limit=40)
        if len(recent_toots) > 0:
            print(f"Found {len(recent_toots)} new toots.")
            last_toot_id = recent_toots[0].id
            for toot in recent_toots:
                toot_text = toot2text(toot)
                if not toot_text:
                    continue
                lang_code = langid.classify(toot_text)[0]
                if lang_code=='en':
                    print(f'\n[{toot.id}]\n{toot_text}')
                    # check if on topic
                    try:
                        scores = mnli(toot_text, config['topic_list'], multi_label=True)['scores']
                    except Exception as e:
                        print(e)
                        scores = None
                else:
                    print(f"\nNon-English toot detected, skipping...")
                    scores = None
                if scores:
                    for score in scores:
                        if score > config['match_level']:
                            mastodon.status_bookmark(toot.id)
                            print("Bookmarked (score={}): ".format(round(score,2)))
                            break
        else:
            print("No new toots found; checking again in 60 seconds...")
    except Exception as e:
        print(e)
        print("Waiting 60 seconds...")
        sleep(60)
        continue