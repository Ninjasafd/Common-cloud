from monkeylearn import MonkeyLearn
from os.path import join, dirname
import json
from pprint import pprint
import sys

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

DEFAULT_ENDPOINT = 'https://api.monkeylearn.com/v3/classifiers/cl_pi3C7JiL/classify/'

class Sentiment:
    def __init__(self, api_key):
        self.ml = MonkeyLearn(api_key)
        self.model_id = "cl_pi3C7JiL"
    def docAnalyze(self, text, isFile):
        # Read data from file to a string
        if (isFile):
            text_file = open(join(dirname(__file__), text), "r")
            data = [text_file.read()]
            text_file.close()
        else:
            data = [text]
        
        response = self.ml.classifiers.classify(self.model_id, data)
        temp = response.body[0]['classifications'][0]

        returnJson = {
            "score" : temp['confidence'],
            "type" : temp['tag_name']
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
    model = Sentiment(keys['monkeylearn']['key'])
    model(file_name)

    