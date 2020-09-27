import re
import json
import requests

credentials = open('creds.json')
credentials = json.load(credentials)
access_token = credentials['bearer']

class TwitterDownloader(object):
    def __init__(self, url):
        self.url = url
        self.base_uri = 'https://api.twitter.com/1.1/statuses/show.json'
        self.headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8","Accept-Encoding": "gzip"}
        self.url_media = None
        self.id_tweet = None

    def get_id(self):
        id_tweet = self.url.split('/status/')[-1]
        pattern = '^[0-9]+$'
        pattern = re.compile(pattern)
        match = re.match(pattern, id_tweet)
        if match:
            self.id_tweet = id_tweet
        else:
            print('Check Id')


    def get_media_url(self):
        r = requests.get(self.base_uri, headers=self.headers, params={'tweet_mode':'extended', 'id':self.id_tweet})
        media = r.json()['extended_entities']['media']
        if media[0]['type'] == 'photo':
            self.url_media = media[0]['media_url']
        elif media[0]['type'] == 'video':
            self.url_media = media[0]['video_info']['variants'][0]['url']


    def download_media(self):
        r = requests.get(self.url_media)
        content = r.content
        with open('download', 'wb') as f:
            f.write(content)