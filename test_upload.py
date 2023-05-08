import requests
from PIL import Image

url = 'http://raspberrypi.local:5000'

image = Image.open('ai_output.png')

files = {'image': image.tobytes()}

r = requests.post(url, files=files)

print(f"Status Code: {r.status_code}")
print(f"Text {r.text}")
