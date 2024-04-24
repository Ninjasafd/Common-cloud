import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

DEFAULT_ENDPOINT = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/6790bdbf-24bf-4099-85ad-f69981c25e3c'


# FOrmats and then returns the json with the data 
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        self.data = None

    def on_data(self, data):
        self.data = data
        
    def getData(self):
        # If we want to return all of the data, uncomment the next line
        # return self.data

        # Otherwise we only return the necessary "text" and "confidence" fields
        temp = self.data['results'][0]["alternatives"][0]
        
        returnJson = {
            "text" : temp['transcript'],
            "confidence" : temp['confidence']
        }
        return returnJson

# API call and algorithm
class STT:
    def __init__(self, api_key):
        authenticator = IAMAuthenticator(api_key)
        self._stt = SpeechToTextV1(authenticator=authenticator)
        self._stt.set_service_url(DEFAULT_ENDPOINT)
        self.Callback = MyRecognizeCallback()

    def synthesize(self, audio_name):
        with open(audio_name,
              'rb') as audio_file:
            audio_source = AudioSource(audio_file)
            self._stt.recognize_using_websocket(
                audio=audio_source,
                content_type='audio/flac',       #'audio/wav'
                recognize_callback = self.Callback,
                model='en-US_BroadbandModel',
        )
        return self.Callback.getData()
    def __call__(self, audio_name):
        if MOCKING_VAR:
            dummyReturn = {"confidence" : 1, 'text': "Dummy text"}
            return dummyReturn
        return self.synthesize(audio_name)




if __name__ == '__main__':
    
    import sys
    audio_name = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f) 
    model = STT(keys['ibm']['speech-to-text'])
    model = model(audio_name)
    # print(model)

    
