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

def _authenticate_client(api_key, endpoint):
    ta_credential = AzureKeyCredential(api_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=ta_credential
    )
    return text_analytics_client


class Sentiment:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.client = _authenticate_client(api_key, endpoint)
    def predict(self, text):
        resp = self.client.analyze_sentiment(documents=[text])[0]
        output = {
            'positive': resp.confidence_scores.positive,
            'neutral': resp.confidence_scores.neutral,
            'negative': resp.confidence_scores.negative
        }
        return output
    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'positive': 1, 'neutral': 0, 'negative': 0}
            return dummyReturn
        return self.predict(text)


if __name__ == "__main__":
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Sentiment(keys['microsoft']['sentiment'], DEFAULT_ENDPOINT)
    y = model(text)
    pprint(y)
