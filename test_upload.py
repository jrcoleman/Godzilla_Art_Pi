import requests

url = 'http://raspberrypi.local:5000'

files = {'image': open('ai_output.png','rb')}

r = requests.post(url, files=files)

print(f"Status Code: {r.status_code}")
print(f"Text {r.text}")
