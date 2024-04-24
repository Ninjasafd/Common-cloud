"""
all speech-to-text services should return (not just print) something like:

{
    'confidence': <value>,
    'text': <Example text>
 }
"""

import json
import sys
from pprint import pprint

from _assembly_ai.stt import STT as Assembly_AI_STT
from _deepgram.stt import STT as Deepgram_STT
from _google.stt import STT as Google_STT
from _ibm.stt import STT as IBM_STT
from _microsoft.stt import STT as Microsoft_STT

from _common import (
    SERVICES,
    ASSEMBLY_AI,
    DEEPGRAM,
    GOOGLE,
    IBM,
    MICROSOFT,
)

def available_services():
    return SERVICES

def STT_factory(service, keys):
    if service == ASSEMBLY_AI:
        return Assembly_AI_STT(keys["assembly_ai"])
    elif service == DEEPGRAM:
        return Deepgram_STT(keys["deepgram"])
    elif service == GOOGLE:
        return Google_STT(keys["google"])
    elif service == IBM:
        return IBM_STT(keys["ibm"]['speech-to-text'])
    elif service == MICROSOFT:
        return Microsoft_STT(keys["microsoft"]['speech-to-text'])
    

def STT(service, keys):
    return STT_factory(service, keys)


if __name__ == "__main__":

    with open('keys.json', 'r') as f:
        keys = json.load(f)

     # Command Line Call
    if (len(sys.argv)-1) >= 2:
        try:
            modelname = sys.argv[1]
            filename = sys.argv[2]
            model = STT(modelname.lower(), keys)
            y = model(filename)
            print(y)
        except:
            print("Something went wrong")

    # 
    else:
        # model = STT("assembly_ai", keys)
        model = STT("deepgram", keys)      
        # model = STT("google", keys)
        # model = STT("microsoft", keys)        # Doesn't work Right Now
        # model = STT("ibm", keys)
        
        # Pass in the name of the file here
        fileName = "factory_test_files\\test.flac"
        y  = model(fileName)
        print(y)
