import sys
import json

import azure.cognitiveservices.speech as speechsdk

# TODO this is my specific endpoint and should not be hard-coded
DEF_ENDPOINT = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
DEF_LOCATION = "eastus"
DEF_VOICE = "en-US-GuyNeural"
DEF_LANG = "en-US"


class TTS:
    def __init__(self, api_key, location=DEF_LOCATION):
        self.api_key = api_key
        self.location = location
        self._config = speechsdk.SpeechConfig(
            subscription=api_key,
            region=location
        )
    def predict(
            self,
            text,
            output_filename,
            synthesis_language=DEF_LANG,
            synthesis_voice=DEF_VOICE
        ):
        self._config.speech_synthesis_language = synthesis_language
        self._config.speech_synthesis_voice_name = synthesis_voice
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_filename)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self._config,
            audio_config=audio_config
        )
        synthesizer.speak_text_async(text)
        return "Done"
    def __call__(
            self,
            text,
            output_filename,
            synthesis_language=DEF_LANG,
            synthesis_voice=DEF_VOICE
        ):
        return self.predict(text, output_filename, synthesis_language, synthesis_voice)

if __name__ == "__main__":
    text = sys.argv[1]
    outfile = sys.argv[2]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = TTS(keys['microsoft']['tts'])
    model(text, outfile)
