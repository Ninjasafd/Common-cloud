
"""
all sentiment services should return (not just print) something like:

{'negative': 0.0, 'neutral': 0.0, 'positive': 1.0}
"""

import json
import sys
from pprint import pprint
from os.path import join, dirname

from _clarifai.sentiment import Sentiment as Clarifai_Sentiment
from _google.sentiment import Sentiment as Google_Sentiment
from _meaning_cloud.sentiment import Sentiment as MeaningCloud_Sentiment
from _microsoft.sentiment import Sentiment as Microsoft_Sentiment
from _ibm.sentiment import Sentiment as IBM_Sentiment
# from _yonder
from _komprehend.sentiment import Sentiment as Komprehend_Sentiment
# from _intellexer.
from _dandelion.sentiment import Sentiment as Dandelion_Sentiment
from _monkeylearn.sentiment import Sentiment as MonkeyLearn_Sentiment
from _lettria.sentiment import _Sentiment as Lettria_Sentiment
from _uclassify.sentiment import Sentiment as Uclassify_Sentiment


from _common import (
    SERVICES,
    CLARIFAI,
    GOOGLE,
    MICROSOFT,
    IBM,
    KOMPREHEND,
    LETTRIA,
    MEANING_CLOUD,
    KOMPREHEND,
    DANDELION,
    MONKEYLEARN,
    LETTRIA,
    UCLASSIFY
)
sentiment_services =[
    CLARIFAI,
    GOOGLE,
    MICROSOFT,
    IBM,
    KOMPREHEND,
    LETTRIA,
    MEANING_CLOUD,
    KOMPREHEND,
    DANDELION,
    MONKEYLEARN,
    LETTRIA,
    UCLASSIFY]

score_type = [
    GOOGLE, 
    IBM,
    MEANING_CLOUD,
    DANDELION,
    MONKEYLEARN
]


def sentiment_available_services():
    return sentiment_services

def get_score_type():
    return score_type


def sentiment_factory(service, keys):
    if service == CLARIFAI:
        api_key = keys['clarifai']['api-key']
        user_id = keys['clarifai']['user-id']
        app_id = keys['clarifai']['app-id']
        model_id = keys['clarifai']['model-id']
        return Clarifai_Sentiment(api_key, user_id, app_id, model_id)
    elif service == GOOGLE:
        return Google_Sentiment(keys['google'])
    elif service == MICROSOFT:
        return Microsoft_Sentiment(keys['microsoft']['sentiment'])
    elif service == IBM:
        return IBM_Sentiment(keys['ibm']["sentiment"])
    elif service == MEANING_CLOUD:
        return MeaningCloud_Sentiment(keys['meaning_cloud'])
    elif service == KOMPREHEND:
        return Komprehend_Sentiment(keys['komprehend'])
    elif service == DANDELION:
        return Dandelion_Sentiment(keys['dandelion'])
    elif service == MONKEYLEARN:
        return MonkeyLearn_Sentiment(keys['monkeylearn'])
    elif service == LETTRIA:
        return Lettria_Sentiment(keys['lettria'])
    elif service == UCLASSIFY:
        return Uclassify_Sentiment(keys['uclassify'])


def Sentiment(service, keys):
    return sentiment_factory(service, keys)


if __name__ == "__main__":
    with open(join(dirname(__file__), 'keys.json'), 'r') as f:
        keys = json.load(f)

    # Command Line Call
    if (len(sys.argv)-1) >= 2:
        try:
            modelname = sys.argv[1]
            text = sys.argv[2]
            model = Sentiment(modelname.lower(), keys)
            y = model(text)
            print(y)
        except:
            print("Something went wrong")
    
    # Manual function calls
    else:
        # model = Sentiment("clarifai", keys)           # {positive, neutral, negative}   1
        # # model = Sentiment("google", keys)             # {score, score}
        # # model = Sentiment("microsoft", keys)            # {positive, neutral, negative}  1
        # # model = Sentiment("ibm", keys)                # {type, score}     2
        # # model = Sentiment("meaning_cloud", keys)      # {score, type}     2
        # # model = Sentiment("komprehend", keys)         # {positive, neutral, negative}        1
        # # model = Sentiment("dandelion", keys)          # {score, type}      2
        # # model = Sentiment("monkeylearn", keys)        # {score, type}      2
        # # model = Sentiment("lettria", keys)            # {type, score}   1
        # # model = Sentiment("uclassify", keys)            # {positive, negative}

        # y = model("This is not very good")
        # pprint(y)

        text = "Tesco Abandons Video-Streaming Ambitions in Blinkbox Sale"
        for service in sentiment_services:
            model = Sentiment(service, keys)
            y = model(text)
            print(service, ": ", y)


