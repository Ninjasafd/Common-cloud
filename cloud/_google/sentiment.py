import os
import sys
import json
from pprint import pprint
from google.cloud import language_v1

#from _google_common import GOOGLE_ENV

# from _google_common import GOOGLE_ENV
GOOGLE_ENV = 'GOOGLE_APPLICATION_CREDENTIALS'
PLAIN_TEXT = language_v1.Document.Type.PLAIN_TEXT

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

class Sentiment:
    """
    off-the-shelf Google Cloud model
    """

    def __init__(self, api_key=None):
        self.api_key = api_key
        os.environ[GOOGLE_ENV] = self.api_key
        self.client = language_v1.LanguageServiceClient()

    def predict_string(self, text):
        document = language_v1.Document(content=text, type_=PLAIN_TEXT)
        result = self.client.analyze_sentiment(
            request={'document': document}
        ).document_sentiment

        score = result.score
        if score > 0:
            type = "positive"
        elif score < 0:
            type = "negative"
        else:
            type = "neutral"

        returnJson = {'score': result.magnitude,
                      'type': type}

        return returnJson

    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'type': "positive", 'score':1}
            return dummyReturn
        return self.predict_string(text)


if __name__ == "__main__":
    instring = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Sentiment(keys['google'])
    y = model(instring)
    pprint(y)
