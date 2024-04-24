import json
import time
from pprint import pprint

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

TEST_URL = "https://raw.githubusercontent.com/MicrosoftDocs/" +\
            "azure-docs/master/articles/cognitive-services/" +\
            "Computer-vision/Images/readsample.jpg"
# TODO endpoint is specific to my account, need to change
DEFAULT_ENDPOINT = "https://ss-computer-vision.cognitiveservices.azure.com/"
DEFAULT_WAIT_TIME = 1


# TODO currently only supports url inputs; unclear if API supports files
# ... could upload file to storage blob
class OCR:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.api_key = api_key
        self.endpoint = endpoint
        self.client = ComputerVisionClient(
            endpoint,
            CognitiveServicesCredentials(self.api_key)
        )
    def _format_output(self, read_result):
        output = {'text': [], 'boxes': []}
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                output['text'].append(line.text)
                output['boxes'].append(line.bounding_box)
        return output
    def predict_url(self, url):
        resp = self.client.read(url, raw=True)
        read_operation_location = resp.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]
        while True:
            read_result = self.client.get_read_result(operation_id)
            if read_result.status not in ["notStarted", "running"]:
                break
            time.sleep(DEFAULT_WAIT_TIME)
        return self._format_output(read_result)
    def __call__(self, url):
        return self.predict_url(url)


if __name__ == "__main__":
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = OCR(keys['microsoft']['ocr'])
    y = model.predict_url(TEST_URL)
    pprint(y)
