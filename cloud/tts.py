"""
all text-to-speech services should return a file:

"""

import sys
import json
from pprint import pprint

from _ibm.tts import TTS as IBM_TTS
from _google.tts import TTS as Google_TTS
from _microsoft.tts import TTS as Microsoft_TTS

from _common import (
    SERVICES,
    GOOGLE,
    IBM,
    MICROSOFT,
)
tts_services = [
    GOOGLE,
    IBM,
    MICROSOFT
]

def available_services():
    return SERVICES

def TTS_factory(service, keys):
    if service == GOOGLE:
        return Google_TTS(keys['google'])
    elif service == IBM:
        return IBM_TTS(keys["ibm"]['text-to-speech'])
    elif service == MICROSOFT:
        return Microsoft_TTS(keys["microsoft"]['text-to-speech'])
    

def TTS(service, keys):
    return TTS_factory(service, keys)


if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)

    # Command Line Call
    if (len(sys.argv)-1) >= 3:
        try:
            modelname = sys.argv[1]
            text = sys.argv[2]
            outfile_name = sys.argv[3]
            model = TTS(modelname.lower(), keys)
            y = model(text, outfile_name)
            print(y)
        except:
            print("Something went wrong")
    
    else:
        text = "Hi everyone. This is a test file"
        outfile_name = "factory_test_files\\output"
        type = ".wav"

        for service in tts_services:

            model = TTS(service, keys)
            y = model(text, outfile_name + service + type)
            print(service, ": ", y)
