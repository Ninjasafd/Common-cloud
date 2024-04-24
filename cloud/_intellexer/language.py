import requests
import json

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

"""
    Object language
    - language
    - score
"""

class Language:
    def __init__(self, json):
        self.__language = json["language"]
        self.__weight = json["weight"]

    def get_language(self):
        return self.__language

    def get_weight(self):
        return self.__weight


class RecognizeLanguageResult:
    def __init__(self, json):
        self.__language = []
        if json["languages"] is not None:
            for lan in json["languages"]:
                self.__language.append(Language(lan))

    def get_languages(self):
        return self.__language


class LanguageDetector:
    def __init__(self, api_key):
        self.api_key = api_key

    def predict(self, text):
        url = "http://api.intellexer.com/recognizeLanguage?"\
              "apikey={0}".format(self.api_key)
        try:
            response = requests.post(url, data=text)
            if response.status_code == 400:
                print("400 Bad Request")
                raise Exception("Error in request")
            if response.status_code != 200:
                print("error: " + str(response.json()
                      ["error"]) + "\nmessage: " + response.json()["message"])
                raise Exception(response.json()["message"])
        except Exception as ex:
            print("Exception: " + str(ex))
            exit(1)

        data = RecognizeLanguageResult(response.json())
        if (len(data.get_languages()) > 0):
            result = data.get_languages()[0]

            returnJson = {
                "language": result.get_language(),
                "confidence": result.get_weight()/9.5       # Max weight according to API
            }
            
            return returnJson
        else:
            return None

    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn

        text = text.encode('utf-8')
        return self.predict(text)


if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = LanguageDetector(keys['intellexer']['key'])
    text = "Γεια"

    res = model.predict(text)
    print(res)
