import json
import requests as req

TEST_OCR_URL = 'https://www.moderatecontent.com/img/sample_text.png'
#TEST_OCR_URL = 'https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg'

_ROOT = 'https://api.moderatecontent.com/'

with open('_languages.json', 'r') as f:
    _LANGS = json.load(f)

class OCR:
    def __init__(self, api_key):
        self.endpoint = _ROOT + 'ocr/?lang={}&key=' + api_key + '&url='
    def predict(self, url, language='eng'):
        assert language in _LANGS # TODO handle failures better... or check error code in output
        url = self.endpoint.format(language) + url
        resp = req.get(url)
        return resp.json()
    def __call__(self, url, language='eng'):
        return self.predict(url, language)

if __name__ == '__main__':
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    ocr = OCR(keys['moderate_content'])
    y = ocr(TEST_OCR_URL)
    print(y)
