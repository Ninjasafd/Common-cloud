import sys
import json
import requests
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

ENDPOINT = 'https://api.uclassify.com/v1/uClassify/language-detector/classify/?readKey={}&text={}'

DEFAULT_N_RESULTS = 3


class Language:
    def __init__(self, api_key):
        self.api_key = api_key
    def predict(self, text, top_n=DEFAULT_N_RESULTS):
        _url = ENDPOINT.format(self.api_key, text)
        resp = requests.get(_url).json()
        plist = list(resp.items())
        plist.sort(key=lambda p: p[1], reverse=True)
        top = plist[:top_n]
        temp = top[0]
        returnJson = {
            "language" : temp[0][-3:],
            "confidence" : temp[1]
        }
        return returnJson
    def __call__(self, text, top_n=DEFAULT_N_RESULTS):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn
        return self.predict(text, top_n)

if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Language(keys['uclassify'])
    y = model.predict(text)
    pprint(y)
