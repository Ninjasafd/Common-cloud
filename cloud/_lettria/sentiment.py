import lettria
import json
# import pprint
import sys
from os.path import join, dirname
from lettria import Sentiment

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

# This class has a slightly different name because of the import
class _Sentiment:
    def __init__(self, api_key):
        self.nlp = lettria.NLP(api_key)
        self.sentiment = Sentiment(self.nlp)
    def docAnalyze(self, text, isFile):
        if (isFile):
            text_file = open(join(dirname(__file__), file_name), "r")
            data = [text_file.read()]
            text_file.close()   
        else:
            data = [text]
        
        self.nlp.add_document(data, verbose = False)

        result = self.nlp.get_sentiment
        temp = result(granularity = "subsentence")

    
        returnJson = {
            "negative" : -temp['negative']['average'],
            "positive" : temp['positive']['average'],
        }

        return returnJson
        
    def __call__(self, data, isFile = False):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'positive': 1, 'neutral': 0, 'negative': 0}
            return dummyReturn
        return self.docAnalyze(data, isFile)


if __name__ == '__main__':
    
    file_name = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f) 
    model = _Sentiment(keys['lettria']['key'])
    model(file_name)
