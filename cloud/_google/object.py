import os
import json
from PIL import Image
from pprint import pprint
from google.cloud import vision

from cloud.image_tools import draw_polygon, draw_bbox

from _common import GOOGLE_ENV


def localize_objects_uri(uri):
    """Localize objects in the image on Google Cloud Storage
    Args:
    uri: The path to the file in Google Cloud Storage (gs://...)
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = uri

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))

def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    output = []
    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
        output.append({
            'confidence': object_.score,
            'label': object_.name,
            'poly': [(vertex.x, vertex.y) for vertex in object_.bounding_poly.normalized_vertices]
        })
    return output


class ObjectDetector:
    """
    off-the-shelf Google Cloud model
    """
    def __init__(self, api_key=None):
        print(api_key)
        print()
        self.api_key = api_key
        os.environ[GOOGLE_ENV] = api_key
    def predict_from_url(self, url):
        localize_objects_uri(url)
    def predict_from_file(self, filename):
        return localize_objects(filename)
    def __call__(self, path):
        return self.predict_from_file(path)

if __name__ == '__main__':
    with open('keys.json','r') as f:
        keys=json.load(f)
    import sys
    filename = sys.argv[1]
    model = ObjectDetector(keys['google'])
    objects = model(filename)
    pprint(objects)

    boxes = []
    for obj in objects:
        poly = obj['poly']

        im = Image.open(filename)

        w,h = im.size
        p = [] 
        for (a,b) in poly:
            p.append((a*w, b*h))
        left = poly[0][0]*w
        right = poly[1][0]*w
        top = poly[0][1]*h
        bottom = poly[2][1]*h
        boxes.append({'left': left, 'right': right, 'top': top, 'bottom': bottom})
    draw_bbox(im, boxes).show()
