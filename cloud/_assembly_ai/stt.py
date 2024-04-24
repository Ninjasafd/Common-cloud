import sys
import json
import time
import requests
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

DEFAULT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
DEFAULT_UPLOAD = "https://api.assemblyai.com/v2/upload"
DEFAULT_CHUNK_SIZE = 5242880

STATUS_ERROR = "error"
STATUS_COMPLETE = "completed"
STATUS_PROCESSING = "processing"
STATUS_QUEUED = "queued"

WAIT_SECONDS = 3

TEST_URL = 'https://bit.ly/3yxKEIY'

def _wait(t=WAIT_SECONDS):
    time.sleep(t)

def _read_file(filename, chunk_size=DEFAULT_CHUNK_SIZE):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

class STT:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.api_key = api_key
        self.endpoint = endpoint
    def _push_audio_url(self, url):
        _json = {"audio_url": url}
        headers = {
            "authorization": self.api_key,
            "content-type": "application/json"
        }
        resp = requests.post(self.endpoint, json=_json, headers=headers).json()
        _id = resp.get('id', None)

        return _id
    def _push_audio_file(self, path, chunk_size=DEFAULT_CHUNK_SIZE):
        headers = {'authorization': self.api_key}
        resp = requests.post(
            DEFAULT_UPLOAD,
            headers=headers,
            data=_read_file(path)
        ).json()
        upload_url = resp['upload_url']
        return upload_url
    def _get_result(self, _id):
        _url = self.endpoint + '/' + str(_id)
        headers = {"authorization": self.api_key}
        resp = requests.get(_url, headers=headers).json()
        return resp
    def transcribe_url(self, url):
        _id = self._push_audio_url(url) 
        result = self._get_result(_id)
        status = result['status']
        while status != STATUS_COMPLETE:
            if status == STATUS_ERROR:
                print('assembly ai API returned \'error\' status')
                return None
            elif status == STATUS_PROCESSING or status == STATUS_QUEUED:
                # print(status)
                _wait()
                result = self._get_result(_id)
                status = result['status']
        if status == STATUS_COMPLETE:
            # return result
            returnJson = {
                "text" : result["text"],
                "confidence" : result["confidence"]
            }
            return returnJson
    def transcribe_file(self, path):
        _url = self._push_audio_file(path)
        return self.transcribe_url(_url)
    def __call__(self, path):
        if MOCKING_VAR:
            dummyReturn = {"confidence" : 1, 'text': "Dummy text"}
            return dummyReturn
        return self.transcribe_file(path)

if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = STT(keys['assembly_ai'])
    filename = sys.argv[1]
    y = model(filename)
    #y = model.transcribe_url(TEST_URL)
    pprint(y)
