from pickle import FALSE
import sys
import json
from os.path import join, dirname
from pprint import pprint
from monkeylearn import MonkeyLearn

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

DEFAULT_ENDPOINT = 'https://api.monkeylearn.com/v3/classifiers/cl_Vay9jh28/classify/'


class Language:
    def __init__(self, api_key):
        self.ml = MonkeyLearn(api_key)
        self.model_id = "cl_Vay9jh28"
    def predictUseFile(self, textdata, isFile):
        if (isFile == True):
            text_file = open(join(dirname(__file__), textdata), "r")
            data = [text_file.read()]
            text_file.close()
        else:
            data = [textdata]
        result = self.ml.classifiers.classify(self.model_id, data)
        result = result.body[0]['classifications'][0]
    
        returnJson = {
            'language' : result['tag_name'][-2:],
            'confidence' : result['confidence']
        }
        
        return returnJson

    def __call__(self, data, isFile=False):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn
        return self.predictUseFile(data, isFile)
        


if __name__ == "__main__":
    file = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Language(keys['monkeylearn']['key'])
    model(file)
