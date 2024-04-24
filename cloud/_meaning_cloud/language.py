import sys
import json
import requests
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

DEFAULT_ENDPOINT = 'https://api.meaningcloud.com/lang-4.0/identification'


class Language:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.api_key = api_key
        self.endpoint = endpoint
    def predict(self, text):
        payload = {
            'key': self.api_key,
            'txt': text
        }
        resp = requests.post(self.endpoint, data=payload).json()
        # return resp

        if resp['status']['code'] == 0 and len(resp['language_list']) > 0:
            temp = resp['language_list'][0]
            returnJson = {
                "language" : temp['language'],
                "confidence" : temp['relevance'] / 100      # Returns relevance out of 100 so convert that
            }
            return returnJson
        else:
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
    model = Language(keys['meaning_cloud'])
    y = model(text)
    pprint(y)
