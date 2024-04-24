import os
import sys
import six
import json
from google.cloud import translate_v2 as translate

#from _common import GOOGLE_ENV
GOOGLE_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


class Translate:
    def __init__(self, api_key):
        os.environ[GOOGLE_ENV] = api_key
        self.client = translate.Client()

    def translate(self, text, target, source=None):
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")
        result = self.client.translate(text, target_language=target)
        returnJson = {
            "confidence": 0,            # Need to add confidence for Google
            "output": result['translatedText'],
            "source_language": result['detectedSourceLanguage'],
            "target_language": target
        }
        return returnJson

    def __call__(self, text, target, source=None):
        return self.translate(text, target, source)


if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Translate(keys['google'])
    y = model("ich heisse stefan", "en")
