import sys
import json
from pprint import pprint

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

DEFAULT_ENDPOINT = "https://ss-computer-vision.cognitiveservices.azure.com/"


class ObjectDetector:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self._client = ComputerVisionClient(
            endpoint,
            CognitiveServicesCredentials(api_key)
        )
    def predict_url(self, url):
        results = self._client.detect_objects(url)
        return self._predict(results)
    def predict_file(self, filepath):
        local_image = open(filepath, 'rb')
        results = self._client.detect_objects_in_stream(local_image)
        return self._predict(results)
    def _predict(self, results):
        output = []
        for result in results.objects:
            left = result.rectangle.x
            right = left + result.rectangle.w
            top = result.rectangle.y
            bottom = top + result.rectangle.h
            box = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
            label = result.object_property
            confidence = result.confidence
            output.append({'bbox': box, 'label': label, 'confidence': confidence})
        return output
    def __call__(self, filepath):
        return self.predict_file(filepath)

if __name__ == "__main__":
    filename = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = ObjectDetector(keys['microsoft']['object-detection'])
    y = model(filename)
    pprint(y)
