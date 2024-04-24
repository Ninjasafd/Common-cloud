import sys
import json
from os.path import join, dirname
import detectlanguage

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

class Language:
    def __init__(self, api_key):
        detectlanguage.configuration.api_key = api_key
    def predict(self, text, isFile):
        if (isFile):
            text_file = open(join(dirname(__file__), text), "r")
            data = text_file.read()
            text_file.close()
        else:
            data = text

        resp = detectlanguage.detect(data)
        temp = resp[0]
        returnJson = {
            "language" : temp['language'],
            "confidence" : temp['confidence']/13       # Confidence is weird on this one, it depends on amount of text given, I believe max is thirteen
        }
        return returnJson
    def __call__(self, file_name, isFile = False):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn
        return self.predict(file_name, isFile)


if __name__ == "__main__":
    file = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Language(keys['detectlanguage']['key'])
    model(file)
