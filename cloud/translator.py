import json
import sys
from pprint import pprint

from _google.translate import Translate as Google_Translate
from _ibm.translate import Translator as IBM_Translate
from _microsoft.translate import Translator as Microsoft_Translate
from _uclassify.translate import Translate as Uclassify_Translate

"""
Call is model("Text", target_language, source_language)

all services should return the following:

{
    "confidence" : <confidence>, 
    "output": "<translated text>",
    "source_language": "<source language>",
    "target_language": "<target language>"
}
"""

from _common import (
    SERVICES,
    GOOGLE,
    IBM,
    MICROSOFT,
    UCLASSIFY
)
translator_services = [
    GOOGLE,
    IBM,
    MICROSOFT,
    UCLASSIFY
    ]


def translator_available_services():
    return translator_services


def translate_factory(service, keys):
    if service == MICROSOFT:
        return Microsoft_Translate(keys['microsoft']['translate'])
    elif service == GOOGLE:
        return Google_Translate(keys['google'])
    elif service == IBM:
        return IBM_Translate(keys['ibm']['translate'])
    elif service == UCLASSIFY:
        return Uclassify_Translate(keys['uclassify'])


def Translate(service, keys):
    return translate_factory(service, keys)


if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)

    # Command Line Call
    if (len(sys.argv)-1) >= 4:
        try:
            modelname = sys.argv[1]
            text = sys.argv[2]
            source = sys.argv[3]
            target = sys.argv[4]
            model = Translate(modelname.lower(), keys)
            y = model(text, target=target)
            print(y)
        except:
            print("Something went wrong")
    
    else:

        
        text = "I love speaking many languages! I also like good food."

        for service in translator_services:
            model = Translate(service, keys)

            # This is for uclassify, which for some reason only translate from either
            # Swedish, spanish, or french to english. Also, it does not return a confidence score
            if service == UCLASSIFY:
                y = model("Yo soy bien. Como estas?", "en", "es")

            # Other services
            else:
                y = model(text, "es", "en")

            # Format
            # y = model(text, target_lang, src_lang)
            print(service, ": ", y)

        