import sys
import json
import requests
from pprint import pprint

ENDPOINT = 'https://api.uclassify.com/v1/uClassify/iab-taxonomy-v2/classify/?readKey={}&text={}'

DEFAULT_N_RESULTS = 5

class Categorization:
    def __init__(self, api_key):
        self.api_key = api_key
    def predict(self, text, top_n=DEFAULT_N_RESULTS):
        _url = ENDPOINT.format(self.api_key, text)
        resp = requests.get(_url).json()
        plist = list(resp.items())
        plist.sort(key=lambda p: p[1], reverse=True)
        top = plist[:top_n]
        return top
    def __call__(self, text, top_n=DEFAULT_N_RESULTS):
        return self.predict(text, top_n)

if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Categorization(keys['uclassify'])
    y = model.predict(text)
    pprint(y)
