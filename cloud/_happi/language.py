import json
import sys
import requests
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

URL = "https://api.happi.dev/v1/language"


class LanguageDetector:
    def __init__(self, api_key):
        self.api_key = api_key
    def predict(self, text):
        _text = "%20".join(text.split())
        url = URL + "?text=" + _text + "&apikey=" + self.api_key
        resp = requests.get(url)
        resp = resp.json()

        # Returns the index of all possible languages detected
        returnJson = resp
        # return returnJson

        ## Might need to change this data processing section
        if (resp['success']):
            resp = resp['langs'][0]
            returnJson = {
                'language' : resp['code'],
                'confidence' : resp['confidence']
            }
            return returnJson
        else:
            print("Happi did not return a valid language.")
            return None

    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn
        return self.predict(text)

if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = LanguageDetector(keys['happi'])
    y = model("[45] ÙÙŠ ÙŠÙ†Ø§ÙŠØ± 2013ØŒ Ø³Ù…ÙŠØª ÙˆÙŠÙƒÙŠØ¨ÙŠØ¯ÙŠØ§ 274301ØŒ ÙƒÙˆÙŠÙƒØ¨ØŒ Ø¹Ù„Ù‰.")
    print(y)
