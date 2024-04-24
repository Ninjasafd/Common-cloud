import json
import asyncio
from pprint import pprint

from deepgram import Deepgram

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

# Asyncio is returning an error for some reason, this silences it
from functools import wraps
 
from asyncio.proactor_events import _ProactorBasePipeTransport
 
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper

_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
"""fix yelling at me error end"""

async def _transcribe_prerecorded(api_key, url):
    client = Deepgram(api_key)
    source = {'url': url}
    punct = {'punctuate': True}
    response = await client.transcription.prerecorded(source, punct)
    return json.dumps(response, indent=4)

async def _transcribe_prerecorded_file(api_key, path):
    client = Deepgram(api_key)
    punct = {'punctuate': True}
    with open(path, 'rb') as af:
        source = {'buffer': af, 'mimetype': 'audio/wav'}
        response = await client.transcription.prerecorded(source, punct)
        return json.dumps(response, indent=4)


class STT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Deepgram(self.api_key)
    def transcribe_url(self, url):
        response = asyncio.run(_transcribe_prerecorded(self.api_key, url))
        return response
    def transcribe_file(self, path):
        response = asyncio.run(_transcribe_prerecorded_file(self.api_key, path))
        responsejson = json.loads(response)

        tempdata = responsejson["results"]["channels"][0]["alternatives"][0]
        
        returnJson = {
            "confidence" : tempdata["confidence"],
            "text" : tempdata["transcript"]
        }

        return returnJson
    def __call__(self, info, option="File"):
        if MOCKING_VAR:
            dummyReturn = {"confidence" : 1, 'text': "Dummy text"}
            return dummyReturn
        try:
            if option == "File":
                return self.transcribe_file(info)
            elif option.lower() == "url":
                return self.transcribe_url(info)
            else:
                return None
        except:
            return None

if __name__ == '__main__':
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = STT(keys['deepgram'])
    test_url = 'https://www.signalogic.com/melp/HAVEnoise/orig/h_orig.wav'
    y = model.transcribe_url(test_url)
    pprint(y)
