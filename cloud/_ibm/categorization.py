import sys
import json
from pprint import pprint
from ibm_watson import NaturalLanguageUnderstandingV1 as NLUV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features, CategoriesOptions
)

DEFAULT_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/5e13b72b-35d5-4c9e-a408-d7fbb5c89a2d'

DEFAULT_VERSION = '2021-08-01'

DEFAULT_N_CATEGORIES = 3
DEFAULT_FEATURES = Features(categories=CategoriesOptions(limit=DEFAULT_N_CATEGORIES))

class Categorization:
    def __init__(self, api_key, version=DEFAULT_VERSION, service_url=DEFAULT_URL):
        authenticator = IAMAuthenticator(api_key)
        self._nlu = NLUV1(version=version, authenticator=authenticator)
        self._nlu.set_service_url(service_url)
    def predict_string(self, text):
        result = self._nlu.analyze(text=text, features=DEFAULT_FEATURES)
        return result.get_result()
    def __call__(self, text):
        return self.predict_string(text)

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        text = ' '.join(f.readlines())
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Categorization(keys['ibm']['categorization'])
    y = model(text)
    pprint(y)
