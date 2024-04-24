"""
factory functions for language detector

{"
}
"""

"""
Should return something like 
{
    language : "en"
    confidence: 1.0
}
"""

import json
import sys
from pprint import pprint
from os.path import join, dirname

from _google.language import Language as Google_Language
from _microsoft.language import Language as Microsoft_Language
from _ibm.language import LanguageDetector as IBM_Language
from _monkeylearn.language import Language as MonkeyLearn_Language
from _dandelion.language import Language as Dandelion_Language
from _intellexer.language import LanguageDetector as Intellexer_Language
from _happi.language import LanguageDetector as Happi_Language
from _meaning_cloud.language import Language as MeaningCloud_Language
from _detectlanguage.language import Language as DetectLanguage_Language
# from _yonder import 
from _uclassify.language import Language as Uclassify_Language




from _common import (
    SERVICES,
    DANDELION,
    DETECTLANGUAGE,
    GOOGLE,
    HAPPI,
    IBM,
    INTELLEXER,
    MEANING_CLOUD,
    MICROSOFT,
    MONKEYLEARN,
    UCLASSIFY
)
language_detect_services = [DANDELION,
    DETECTLANGUAGE,
    GOOGLE,
    HAPPI,
    IBM,
    INTELLEXER,
    MEANING_CLOUD,
    MICROSOFT,
    MONKEYLEARN,
    UCLASSIFY]


def language_detect_available_services():
    return language_detect_services
    

def language_detector_factory(service, keys):
    if service == GOOGLE:
        return Google_Language(keys['google'])
    elif service == MICROSOFT:
        return Microsoft_Language(keys['microsoft']['language'])
    elif service == IBM:
        return IBM_Language(keys['ibm']['language'])
    elif service == INTELLEXER:
        return Intellexer_Language(keys['intellexer'])
    elif service == MONKEYLEARN:
        return MonkeyLearn_Language(keys['monkeylearn'])
    elif service == DANDELION:
        return Dandelion_Language(keys['dandelion'])
    elif service == HAPPI:
        return Happi_Language(keys['happi'])
    elif service == MEANING_CLOUD:
        return MeaningCloud_Language(keys['meaning_cloud'])
    elif (service == DETECTLANGUAGE):
        return DetectLanguage_Language(keys['detectlanguage'])
    elif (service == UCLASSIFY):
        return Uclassify_Language(keys['uclassify'])


def Language(service, keys):
    return language_detector_factory(service, keys)



if __name__ == "__main__":
    with open(join(dirname(__file__), 'keys.json'), 'r') as f:
        keys = json.load(f)

    # Command Line Call
    if (len(sys.argv)-1) >= 2:
        try:
            modelname = sys.argv[1]
            text = sys.argv[2]
            model = Language(modelname.lower(), keys)
            y = model(text)
            print(y)
        except:
            print("Something went wrong")


    # Manual function calls
    else:
        # y  = model("This is definitely English")
        # pprint(y)
        text = "[57] Den 24 oktober 2005 publicerade brittiska The Guardian en artikel med titeln â€Can you trust Wikipedia?â€ ('Kan man lita pÃ¥ Wikipedia?')"

        for service in language_detect_services:
            model = Language(service, keys)
            y = model(text)
            print(service, ": ", y)

