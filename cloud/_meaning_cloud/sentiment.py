from re import L
import sys
import json
import requests
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

DEFAULT_ENDPOINT = "https://api.meaningcloud.com/sentiment-2.1"


class Sentiment:
    def __init__(self, api_key):
        self.api_key = api_key

    def predict(self, text, lang="en"):
        payload = {
            "key": self.api_key,
            "txt": text,
            "lang": lang
        }
        resp = requests.post(DEFAULT_ENDPOINT, data=payload).json()

        if (resp['score_tag'] == 'P' or resp['score_tag'] == 'P+'):
            label = "positive"
        elif (resp['score_tag'] == 'N' or resp['score_tag'] == 'N+'):
            label="negative"
        else:
            label = 'neutral'

        return {'type': label,
                'score': str(int(resp['confidence'])/100) }

    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'score': 1, 'type':'positive'}
            return dummyReturn
        return self.predict(text)


if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Sentiment(keys['meaning_cloud'])
    y = model(text)
    pprint(y)
