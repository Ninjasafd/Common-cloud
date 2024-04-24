import json
from pprint import pprint
from os.path import join, dirname

from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# TODO endpoints should be configurable
DEFAULT_ENDPOINT = "https://api.us-south.language-translator.watson.cloud.ibm.com/instances/0d194040-bc50-4a4b-9a37-2ce0fa30c75b"
DEFAULT_VERSION = "2018-05-01"

with open(join(dirname(__file__), 'language_map.json'), 'r', encoding='utf-8') as f:
    LANGUAGES = json.load(f)

def _get_lang(lang):
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    elif lang in LANGUAGES.values():
        return lang
    else:
        return False


class Translator:
    def __init__(self, api_key, version=DEFAULT_VERSION):
        authenticator = IAMAuthenticator(api_key)
        self._translator = LanguageTranslatorV3(
            authenticator=authenticator,
            version=version)
        self._translator.set_service_url(DEFAULT_ENDPOINT)
    def languages(self):
        return self._translator.list_languages().get_result()
    def translate(self, text, target, source):
        
        _src = None     # Default this to English
        _dst = _get_lang(target)
        if (source != None):
            _src = _get_lang(text)
        
        translation = self._translator.translate(text=text, source =None, target = _dst).get_result()

        returnJson = {
            "output" : translation["translations"][0]['translation'],
            "source_language" : _src,
            "target_language" : _dst,
            "confidence" : translation['detected_language_confidence']
        }
        return returnJson
    def __call__(self, text, target, source=None):
        return self.translate(text, target, source)

if __name__ == '__main__':
    """
    python translator.py 'I like listening to YouTube' en es
    """
    import sys
    text = sys.argv[1]
    dst = sys.argv[2]
    src = sys.argv[3]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = Translator(keys['ibm']['translate'])
    y = model(text, dst, src)
    pprint(y)
