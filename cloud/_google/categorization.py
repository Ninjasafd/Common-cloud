import os
import sys
import json
from pprint import pprint
from google.cloud import language_v1

from _common import GOOGLE_ENV

PLAIN_TEXT = language_v1.Document.Type.PLAIN_TEXT


class TextCategorization:
    """
    off-the-shelf Google Cloud model
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        os.environ[GOOGLE_ENV] = api_key
        self.client = language_v1.LanguageServiceClient()
        print(dir(self.client)); print()
    def predict_string(self, text):
        document = language_v1.Document(content=text, type_=PLAIN_TEXT)
        result = self.client.classify_text(
                        request={'document': document}
                    ).categories
        output = []
        for y in result:
            output.append({'label': y.name, 'confidence': y.confidence})
        return output
    def __call__(self, text):
        return self.predict_string(text)

if __name__ == "__main__":
    infile = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    with open(infile, 'r', encoding='utf-8') as f:
        text = ' '.join(f.readlines())
    model = TextCategorization(keys['google'])
    y = model(text)
    pprint(y)
