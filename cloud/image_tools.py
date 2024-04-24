import requests
from io import BytesIO
from PIL import Image, ImageDraw

TEST_URL = 'https://cdn4.vectorstock.com/i/1000x1000/17/43/finger-prints-vector-291743.jpg'

def _pil_im_from_url(url):
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    return im

def draw_bbox(im, boxes, color='red', width=3):
    """
    draws bounding boxes over image

    boxes is list of dict with:
        - 'left', 'top, 'right', 'bottom' coordinates
    """
    draw = ImageDraw.Draw(im)
    for box in boxes:
        draw.rectangle(((box['left'], box['top']), (box['right'], box['bottom'])),
                       outline=color,
                       width=width)
    return im

def draw_bbox_from_url(url, boxes, color='red', width=3):
    #r = requests.get(url)
    #im = Image.open(BytesIO(r.content))
    im = _pil_im_from_url(url)
    return draw_bbox(im, boxes, color, width)

def draw_points(im, points, color='red'):
    draw = ImageDraw.Draw(im)
    draw.point(points, fill=color)
    return im

def draw_points_from_url(url, points, color='red'):
    im = _pil_im_from_url(url)
    return draw_points(im, points, color)

def draw_polygon(im, points, color='red'):
    draw = ImageDraw.Draw(im)
    draw.polygon(points)
    return im

if __name__ == '__main__':
    url = TEST_URL
    draw_points_from_url(url, (50, 50)).show()
