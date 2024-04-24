import json
import requests as req
from io import BytesIO
#from PIL import Image, ImageDraw # TODO move these to a common image utility file
from PIL import Image

from cloud.image_tools import draw_bbox

#def draw_bbox(im, boxes):
#    draw = ImageDraw.Draw(im)
#    for box in boxes:
#        draw.rectangle(((box['left'], box['top']), (box['right'], box['bottom'])),
#                       outline='red',
#                       width=3)
#    im.show()

#URL = 'https://api.moderatecontent.com/face/?key={}&'.format()

TEST_FACES_URL = 'https://kjl.name/kleach-portrait.jpg'
TEST_FACES_URL = 'https://skysync-act-public.s3.us-east-2.amazonaws.com/images/_skysync_test/yoruba.jpg'

def _load_keys():
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    return keys

class FaceDetector:
    def __init__(self, api_key):
        # TODO figure out if these are the same in terms of face detection
        # ... the second one seems to run more models for gender, age, etc.
        # NOTE teh second url (via the example online) seems to be more precise
        #self.endpoint = 'https://api.moderatecontent.com/face/?key={}&'.format(api_key)
        self.endpoint = 'https://api.moderatecontent.com/moderate/?face=true&key={}&'.format(api_key)
    def detect_face(self, image_url):
        #url = URL.format(self.api_key)
        url = self.endpoint + 'url={}'.format(image_url)
        resp = req.get(url)
        return resp
    def __call__(self, image_url):
        return self.detect_face(image_url)


if __name__ == '__main__':
    keys = _load_keys()
    fd = FaceDetector(keys['moderate_content'])
    resp = req.get(TEST_FACES_URL)
    im = Image.open(BytesIO(resp.content))
    r = fd(TEST_FACES_URL)
    #print(r.json())
    #faces = r.json()['faces']
    faces = [item['face'] for item in r.json()['faces']]
    im = draw_bbox(im, faces)
    im.show()
    #print(r.json())
    #im.show()
