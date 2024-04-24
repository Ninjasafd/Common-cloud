import os
import json
import google.auth
from google.cloud import translate

GOOGLE_ENV = "GOOGLE_APPLICATION_CREDENTIALS"

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")

class Language:
    def __init__(self, api_key, location="global", project_id=None):
        self.api_key = api_key
        if project_id is None:
            key_filename = os.path.basename(api_key).replace('.json', '')
            _project_id = '-'.join(key_filename.split('-')[:-1])
        else:
            _project_id = project_id
        # print()
        # print(_project_id)
        # print()
        self.parent = f"projects/{_project_id}/locations/{location}"
        # print(self.parent)
        os.environ[GOOGLE_ENV] = api_key
        # print(); print(google.auth.default())
        self.client = translate.TranslationServiceClient()
    def predict_string(self, text):
        response = self.client.detect_language(
                        content=text,
                        parent=self.parent,
                        mime_type="text/plain"
                    )
        # print((response.languages[0]).split())

        returnJson = {
            "language": response.languages[0].language_code,
            "confidence": response.languages[0].confidence
        }

        return returnJson
    def __call__(self, text):
        if (MOCKING_TEST == 'True'):
            dummyReturn = {'language': "English", 'confidence':0}
            return dummyReturn
        return self.predict_string(text)

if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    # print(keys)
    model = Language(keys['google'], location="us-central1")
    y = model('donde esta la biblioteca')
    print(y)
