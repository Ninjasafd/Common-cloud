import json

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#DEFAULT_ENDPOINT = 'https://api.us-east.text-to-speech.watson.cloud.ibm.com'

DEFAULT_ENDPOINT = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/2542e644-8c3c-4ac3-9bc6-e739239b12b7'


class TTS:
    def __init__(self, api_key):
        authenticator = IAMAuthenticator(api_key)
        self._tts = TextToSpeechV1(authenticator=authenticator)
        self._tts.set_service_url(DEFAULT_ENDPOINT)
    def synthesize(self, text, outfile, voice='en-US_AllisonV3Voice'):
        with open(outfile, 'wb') as aud:
            aud.write(
                self._tts.synthesize(
                    text,
                    voice=voice,
                    accept='audio/wav'
                ).get_result().content)
        return "Done"
    def __call__(self, text, outfile):
        return self.synthesize(text, outfile)

if __name__ == '__main__':
    """
    python ttx.py 'I like listening to YouTube'
    """
    import sys
    text = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = TTS(keys['ibm']['text-to-speech'])
    model(text, 'test.wav')
