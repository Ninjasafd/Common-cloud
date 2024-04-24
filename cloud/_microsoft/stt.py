import azure.cognitiveservices.speech as speechsdk
import json
import os

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

def flac2wav(path):
    import soundfile
    import numpy

    wav_file = path
    audio, sr = soundfile.read(wav_file)
    tempName = "tempFile.wav"
    soundfile.write(tempName, audio, sr, 'PCM_16')
    return tempName

class STT:
    def __init__(self, api_key):
        # set up translation parameters: source language and target languages
        self.translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription = api_key, 
            region = "eastus",
            speech_recognition_language ='en-US',
            target_languages = ('en'),
            )
        self.translation_config.output_format = speechsdk.OutputFormat(1)
            
    def synthesize(self, audioFileName, fileType = "flac"):
        audio_config = speechsdk.audio.AudioConfig(filename=audioFileName)
        

        recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config= self.translation_config, audio_config=audio_config)
        result = recognizer.recognize_once()

        # Prints if recognize speech
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            
            ret = json.loads(result.json)

            returnJson = {
                'text': result.text,
                'confidence': ret['Confidence']
            }
            
            return returnJson

        return None
    def __call__(self, audio_name):
        if MOCKING_VAR:
            dummyReturn = {"confidence" : 1, 'text': "Dummy text"}
            return dummyReturn
        # return 
        tempFile = flac2wav(audio_name)
        returnData = self.synthesize(tempFile)
        os.remove(tempFile)
        return returnData

       



if __name__ == '__main__':
    import sys
    audio_name = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    fd = STT(keys['microsoft']['speech-to-text'])
    fd = fd(audio_name)
    print(fd)
