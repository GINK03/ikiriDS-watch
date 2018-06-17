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
  '''format rules
  https://twitter.com/nardtree/status/1006325372307161089 が直URLで、username + idで構成されている
  '''
  NGs = ['何かのイキリ語', 'クソ', 'ザコ']
  url = os.environ['SLACK_WEBHOOK_01']
  for name, create_at, text, tweetid in triples:
    #if any( [ ng in text for ng in NGs ] ):
    context = f'''{name} sanが、{create_at} \n https://twitter.com/{name}/status/{tweetid}'''
    payload = {'text':context, "channel": "#ikirids"}
    print( payload )
    requests.post(url, data=json.dumps(payload) )

def runner():
  try:
    print( 'called at', datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') )
    
    quads = []
    for member in tweepy.Cursor(api.list_members, 'Seed57_cash', 'ikirids1').items():
      obj = (member._json)
      #p8p.pprint( obj )
      name = obj['screen_name']
      create_at = obj['status']['created_at']
      text = obj['status']['text']
      tweetid = obj['status']['id']
      key = sha256(bytes(f'{name} {create_at}', 'utf-8')).hexdigest()

      serialized = json.dumps(obj, indent=2, ensure_ascii=False)

      if Path(f'logs/{key}').exists():
        continue

      with Path(f'logs/{key}').open('w') as f:
        f.write( serialized ) 
      print( name, create_at, text )
      quads.append( (name, create_at, text, tweetid) )
    checker( quads )
  except Exception as ex:
    print(ex)
    return

if __name__ == '__main__':
    api_key = os.environ['TWITTER_API']
    api_sec = os.environ['TWITTER_API_SEC']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
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

