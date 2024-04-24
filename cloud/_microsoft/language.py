import sys
import json
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

DEFAULT_ENDPOINT = "https://languagedetectstuff.cognitiveservices.azure.com/"

# TODO there are several common code patterns between the msft text analysis services
def _authenticate_client(api_key, endpoint=DEFAULT_ENDPOINT):
    ta_credential = AzureKeyCredential(api_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential
    )
    return text_analytics_client


class Language:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.client = _authenticate_client(api_key, endpoint)
    def predict(self, text):
        resp = self.client.detect_language(documents=[text])[0]
        output = {
            # 'language': resp.primary_language.name,
            'language': resp.primary_language.iso6391_name,
            'confidence': resp.primary_language.confidence_score
            
        }
        
        return output
    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn

        return self.predict(text)


if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Language(keys['microsoft']['language'], DEFAULT_ENDPOINT)
    y = model(text)
    pprint(y)
