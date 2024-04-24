import sys
import json
import uuid
import requests
from pprint import pprint

DEFAULT_API_VERSION = '3.0'
DEFAULT_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/translate'
DEFAULT_LOCATION = 'eastus'

HEADERS = {
    'Ocp-Apim-Subscription-Key': None,
    'Ocp-Apim-Subscription-Region': None,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


class Translator:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT, location=DEFAULT_LOCATION):
        self.api_key = api_key
        self.endpoint = endpoint
        self.headers = HEADERS
        self.headers['Ocp-Apim-Subscription-Key'] = api_key
        self.headers['Ocp-Apim-Subscription-Region'] = location

    def translate(self, text, target, source):
        params = {
            'api-version': DEFAULT_API_VERSION,
            'from': None,
            'to': target
        }
        body = [{'text': text}]
        resp = requests.post(
            self.endpoint,
            params=params,
            headers=self.headers,
            json=body
        )
        result = resp.json()
        temp = result[0]
        
        returnJson = {
            "confidence": temp['detectedLanguage']['score'],
            "output": temp['translations'][0]['text'],
            "source_language": source,
            "target_language": temp['translations'][0]['to']
        }
        return returnJson

    def __call__(self, text, target, source=None):
        return self.translate(text, target, source)


if __name__ == "__main__":
    text = sys.argv[1]
    dst = sys.argv[2]
    src = sys.argv[3]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Translator(keys['microsoft']['translate'])
    y = model(text, dst, src)
    pprint(y)
