import json
import requests
from PIL import Image
from pprint import pprint

from cloud.image_tools import draw_bbox

regions = ['mx', 'us-ca']


class ALPR:
    def __init__(self, api_key):
        self.api_key = api_key
        self._url = 'https://api.platerecognizer.com/v1/plate-reader/'
    def predict(self, filename):
        with open(filename, 'rb') as fp:
            response = requests.post(
               self._url,
               data=dict(regions=regions),
               files=dict(upload=fp),
                headers={'Authorization': 'Token {}'.format(self.api_key)}
            )
        return response.json()
    def __call__(self, filename):
        return self.predict(filename)

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    model = ALPR(keys['plate_recognizer'])
    results = model(filename)
    pprint(results)

    im = Image.open(filename)

    coords = []
    for result in results['results']:
        bbox = result['box']
        coords.append({
            'top': bbox['ymin'],
            'bottom': bbox['ymax'],
            'left': bbox['xmin'],
            'right': bbox['xmax']
        })
    draw_bbox(im, coords).show()
