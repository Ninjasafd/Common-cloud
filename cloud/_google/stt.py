import os
import sys
import json
import wave
from google.cloud import speech

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

GOOGLE_ENV = 'GOOGLE_APPLICATION_CREDENTIALS'

class STT:
    """Transcribe the given audio file asynchronously."""
    def __init__(self, api_key=None):
        self.api_key = api_key
        os.environ[GOOGLE_ENV] = api_key
        self.client = speech.SpeechClient()
    def translate(self, audio_name):
        with open(audio_name, "rb") as audio_file:
            content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

        # Gets frame rate from the audio file
        hertz_rate = False
        # with wave.open(audio_name, "rb") as audio_file:
        #     hertz_rate = audio_file.getframerate()

        if hertz_rate != False:
            # Configuration of how to read in audio
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
                sample_rate_hertz=hertz_rate,
                language_code="en-US",
            )
        else:
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
                language_code="en-US",
            )


        operation = self.client.long_running_recognize(config=config, audio=audio)

        # Reading in files and checks for issues
        # print("Waiting for operation to complete...")
        response = operation.result(timeout=90)

        # Output
        for result in response.results:
            
            returnJson = {
                "text" : result.alternatives[0].transcript,
                "confidence" : result.alternatives[0].confidence
            }
            # print(u"Transcript: {}".format(result.alternatives[0].transcript, "\n"))
            # print("Confidence: {}".format(result.alternatives[0].confidence, "\n"))
            return returnJson
            
    def __call__(self, audio_file):
        if MOCKING_VAR:
            dummyReturn = {"confidence" : 1, 'text': "Dummy text"}
            return dummyReturn
        return self.translate(audio_file)
    



    
if __name__ == "__main__":
    audio_name = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)

    model = STT(keys['google'])
    model(audio_name)

    
