import json
import sys
from os.path import join, dirname
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

DEFAULT_ENDPOINT = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/466dc207-4022-44f0-8a1d-9e9d0761c103'


class Sentiment:
    def __init__(self, api_key):
        authenticator = IAMAuthenticator(api_key)
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2021-08-01',
            authenticator=authenticator
        )
        self.natural_language_understanding.set_service_url(DEFAULT_ENDPOINT)
    # def urlAnalyze(self, text):        # For a website or article if necessary

    def docAnalyze(self, text, isFile):
        # Read data from file to a string
        if (isFile):
            text_file = open(join(dirname(__file__), text), "r")
            data = text_file.read()
            text_file.close()
        else:
            data = text
        
        response = self.natural_language_understanding.analyze(
            text = data,                              # ▼ Can add targets right here like       ```targets=['Leonardo', 'Actor']````
            features=Features(sentiment=SentimentOptions())).get_result()

        returnJson = {
            'score' : response['sentiment']['document']['score'],
            'type' : response['sentiment']['document']['label']
        }
        return returnJson
        
    def __call__(self, file_name, isFile=False):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'score': 1, 'type':'positive'}
            return dummyReturn
        return self.docAnalyze(file_name, isFile)


if __name__ == '__main__':
    
    file_name = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f) 
    model = Sentiment(keys['ibm']['sentiment'])
    model(file_name)


    