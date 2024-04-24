"""
docs: https://ocr.space/OCRAPI
"""

import sys
import json
import requests
from pprint import pprint

DEFAULT_ENDPOINT = "https://api.ocr.space/parse/imageurl?apikey={}&url={}&language=eng"

TEST_URL = "http://i.imgur.com/fwxooMv.png"
TEST_PATH = "aristotle.jpg"


class OCR:
    def __init__(self, api_key):
        self.api_key = api_key
    def predict_url(self, url):
        # TODO there are more parameters to make available
        _url = DEFAULT_ENDPOINT.format(self.api_key, url)
        resp = requests.get(_url).json()
        return resp
    def predict_file(self, path):
        payload = {
            'apikey': self.api_key,
            'language': 'eng'
        }
        with open(path, 'rb') as f:
            resp = requests.post('https://api.ocr.space/parse/image',
                files={path: f},
                data=payload
            )
        return resp.json()

if __name__ == "__main__":
    filename = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = OCR(keys['ocr_space'])
    #y = model.predict_url(TEST_URL)
    y = model.predict_file(filename)
    pprint(y)
