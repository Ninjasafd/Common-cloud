import json
import requests
from pprint import pprint

with open('keys.json', 'r') as f:
    keys = json.load(f)
key = keys['yonderlabs']

image_url =  "http://media.salon.com/2016/01/donald_trump69.jpg" 
image_url = "https://magazine.columbia.edu/sites/default/files/styles/wysiwyg_full_width_image/public/2020-02/FDR.jpg"
url = "https://api.yonderlabs.com/1.0/image/faceanalysis/fromURL?access_token={}"

#path = "@C:\\Users\\Stefan Larson\\Downloads\\fdr.jpg"
url = url.format(key)
r = requests.post(url, data={"url": image_url})
pprint(r)
print(r.json())
