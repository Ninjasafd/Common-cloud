import sys
import json
import requests
from pprint import pprint

ENDPOINT = 'https://language.uclassify.com/translate/v1/?key={}&source={}&target={}&t={}'

DEFAULT_N_RESULTS = 3

# This API only supports the following source languages:
SRC_LANGS = ['sv', 'es', 'fr']
# This API only supports the following target languages:
DST_LANGS = ['en']

def _check_lang(lang, _type):
    if _type == 'src':
        return lang in SRC_LANGS
    else:
        return lang in DST_LANGS

class Translate:
    def __init__(self, api_key):
        self.api_key = api_key
    def predict(self, text,  target, source):
        _url = ENDPOINT.format(self.api_key, source, target, text)
        resp = requests.get(_url).json()

        returnJson = {
            "confidence" : "None",
            "output" : resp["translations"][0],
            "source_language" : resp["source"],
            "target_language" : resp["target"]
        }
        return returnJson
    def __call__(self, text, target, source="es"):
        return self.predict(text, target, source)

if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Translate(keys['uclassify'])
    y = model.predict('bonjour oui oui', target='en', source='es')
    pprint(y)
