import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import LanguageTranslatorV3
from pprint import pprint

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

DEFAULT_ENDPOINT = "https://api.us-south.language-translator.watson.cloud.ibm.com/instances/1b7c25c3-6078-47e2-a826-4c857ea7f9ec"


class LanguageDetector:
    def __init__(self, api_key):
        authenticator = IAMAuthenticator(api_key)
        self.languageIdentify = LanguageTranslatorV3(version='2018-05-01',authenticator=authenticator)
        self.languageIdentify.set_service_url(DEFAULT_ENDPOINT)

    def predict(self, text):
        language=self.languageIdentify.identify(
            text).get_result()
        data = json.dumps(language)
        data = json.loads(data)
        
        result = data['languages'][0]  
      
        return result

    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn
        return self.predict(text)


if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys=json.load(f)
    model=LanguageDetector(keys['ibm']['language'])
    model("Language translator translates text from one language to another.")
