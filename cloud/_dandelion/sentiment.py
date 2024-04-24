import requests
import json
from os.path import join, dirname
import sys

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

MAXSIZE = 1048576
DEFAULT_ENDPOINT = 'https://api.dandelion.eu/datatxt/sent/v1'
 
class Sentiment:
    def __init__(self, api_key):
        self.token = api_key
    def docAnalyze(self, text, isFile):
        if (isFile):
            text_file = open(join(dirname(__file__), text), "r")
            data = text_file.read()
            text_file.close()
        else:
            data = text


        if (len(data) > MAXSIZE):
            print("Input data too long, must be less than 1048576 characters.")
            return None

        self.payload = {
        'token': self.token,  
        'text' : data,
        'lang': 'en'
    }

        response = requests.get(DEFAULT_ENDPOINT, params=self.payload).json()
        if 'error' in response:
            print("Something went wrong.")
            return None
        
        data = response['sentiment']
        returnJson = {
            'type' : data['type'],
            'score' : data['score']
        }
        return returnJson
        
    def __call__(self, file_name, isFile = False):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'score': 1, 'type':'positive'}
            return dummyReturn
        return self.docAnalyze(file_name, isFile)



if __name__ == '__main__':
    
    file_name = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f) 
    model = Sentiment(keys['dandelion']['key'])
    model(file_name)

    

    # def urlAnalyze(self, text):        # For a website or article if necessary