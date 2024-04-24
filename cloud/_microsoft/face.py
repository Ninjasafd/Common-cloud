import json
import requests
from io import BytesIO
from PIL import Image
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

from cloud.image_tools import draw_bbox_from_url

DEFAULT_ENDPOINT = "https://ss-face-detector.cognitiveservices.azure.com/"

TEST_URL = 'https://kjl.name/kleach-portrait.jpg'

def _get_rectangle(face_dictionary):
    rect = face_dictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return {'left': left, 'top': top, 'right': right, 'bottom': bottom}


class FaceDetector:
    def __init__(self, api_key, endpoint=DEFAULT_ENDPOINT):
        self.api_key = api_key
        self._face_client = FaceClient(endpoint, CognitiveServicesCredentials(api_key))
        self._endpoint = endpoint
    def predict_url(self, url):
        detected = self._face_client.face.detect_with_url(
                        url=url, detection_model='detection_03')
        return detected
    def __call__(self, url):
        return self.predict_url(url)

if __name__ == '__main__':
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    fd = FaceDetector(keys['microsoft']['face-detection'])
    y = fd(TEST_URL)
    draw_bbox_from_url(TEST_URL, [_get_rectangle(y[0])]).show()
