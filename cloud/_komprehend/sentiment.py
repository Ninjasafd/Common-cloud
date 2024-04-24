import sys
import json
import paralleldots
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

class Sentiment:
    def __init__(self, api_key):
        paralleldots.set_api_key(api_key)
    def analyze_file(self, filename, language="en"):
        return paralleldots.sentiment(filename, language).get('sentiment')
    def analyze(self, text, language="en"):
        #return paralleldots.sentiment(text, language).get('sentiment')
        result = paralleldots.sentiment(text, language)
        
        returnJson = result['sentiment']
        
        return returnJson


    def __call__(self, text, language="en"):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'positive': 1, 'neutral': 0, 'negative': 0}
            return dummyReturn
        return self.analyze(text, language)

if __name__ == '__main__':
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f) 
    model = Sentiment(keys['komprehend'])
    y = model.analyze(text)
    pprint(y)
