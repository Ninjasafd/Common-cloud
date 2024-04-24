import requests
import json
from os.path import join, dirname
import sys

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

DEFAULT_ENDPOINT = 'https://api.dandelion.eu/datatxt/li/v1'
MAXSIZE = 1048576

class Language:
    def __init__(self, api_key):
        self.token = api_key
    def docAnalyze(self, text, isFile):
        if (isFile):
            text_file = open(join(dirname(__file__), text), "r")
            data = text_file.read()
            text_file.close()
        else:
            data = text

        self.payload = {
        'token': self.token,  
        'text' : data,
    }
        if (len(data) > MAXSIZE):
            print("Input data too long, must be less than 1048576 characters.")
            return None

        response = requests.get(DEFAULT_ENDPOINT, params=self.payload).json()
        
        if 'error' in response:
            print("Something went wrong")
            return None

        data = response['detectedLangs'][0]
        returnJson = {
            'language' : data['lang'],
            'confidence' : data['confidence']
        }
        return returnJson
        
    def __call__(self, file_name, isFile = False):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn
        return self.docAnalyze(file_name, isFile)


if __name__ == '__main__':
    
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f) 
    model = Language(keys['dandelion']['key'])
    y = model(text)
    print(y)
