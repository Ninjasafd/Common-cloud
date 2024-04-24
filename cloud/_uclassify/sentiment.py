import sys
import json
import requests
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

ENDPOINT = 'https://api.uclassify.com/v1/uClassify/Sentiment/classify/?readKey={}&text={}'


class Sentiment:
    def __init__(self, api_key):
        self.api_key = api_key
    def predict(self, text):
        _url = ENDPOINT.format(self.api_key, text)
        resp = requests.get(_url).json()
        return resp
    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'positive': 1, 'negative': 0}
            return dummyReturn
        return self.predict(text)

if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Sentiment(keys['uclassify'])
    y = model.predict(text)
    pprint(y)
