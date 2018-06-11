import tweepy
import json
import pprint
pp = pprint.PrettyPrinter(indent=1)
from pathlib import Path
from hashlib import sha256
import time
import datetime
import schedule
import os
import requests

def checker(triples):
  NGs = ['何かのイキリ語', 'クソ', 'ザコ']
  url = os.environ['SLACK_WEBHOOK_01']
  for name, create_at, text in triples:
    #if any( [ ng in text for ng in NGs ] ):
    context = f'''{name} sanが、{create_at}に、{text}　という発言をしています。'''
    payload = {'text':context, "channel": "#ikirids"}
    print( payload )
    requests.post(url, data=json.dumps(payload) )

def runner():
  print( 'called at', datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') )
  
  triples = []
  for member in tweepy.Cursor(api.list_members, 'Seed57_cash', 'ikirids1').items():
    obj = (member._json)
    name = obj['screen_name']
    create_at = obj['status']['created_at']
    text = obj['status']['text']
    key = sha256(bytes(f'{name} {create_at}', 'utf-8')).hexdigest()

    serialized = json.dumps(obj, indent=2, ensure_ascii=False)

    if Path(f'logs/{key}').exists():
      continue

    with Path(f'logs/{key}').open('w') as f:
      f.write( serialized ) 
    print( name, create_at, text )
    triples.append( (name, create_at, text) )
  checker( triples )


if __name__ == '__main__':
  try:
    api_key = '8KRoh3ZP2zWJ5CnLqRuWvfFWL'
    api_sec = os.environ['TWITTER_API_SEC']
    access_token = '2343754692-rOsQybI8qWkMzLECPyuSzOYIxM4z7tVv8PqYbnu'
    access_token_sec = os.environ['TWITTER_ACCESS_TOKEN_SEC']
    auth = tweepy.OAuthHandler(api_key, api_sec)
    auth.set_access_token(access_token, access_token_sec)
    api = tweepy.API(auth)
    schedule.every(3).minutes.do(runner)
    
    # run at first 
    runner()
    while True:
      schedule.run_pending()
      time.sleep(1)

  except Exception as ex:
    print(ex)
    time.sleep(1)
