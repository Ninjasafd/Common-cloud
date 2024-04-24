import os
import sys
import json
import wave
from google.cloud import texttospeech

GOOGLE_ENV = 'GOOGLE_APPLICATION_CREDENTIALS'
DEF_LANG = "en-US"


class TTS:
    def __init__(self, api_key=None):
        self.api_key = api_key
        os.environ[GOOGLE_ENV] = api_key
        self.client = texttospeech.TextToSpeechClient()

    def transcribe(self, text, output_filename, synthesis_language):
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=synthesis_language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        # Below is the type of file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(output_filename, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
        return "Done"
    def __call__(self, text, output_filename, synthesis_language = DEF_LANG):
        return self.transcribe(text,output_filename, synthesis_language)

if __name__ == "__main__":
    text = sys.argv[1]
    outfile = sys.argv[2]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = TTS(keys['google'])
    f = model(text, outfile)
    print(f)
