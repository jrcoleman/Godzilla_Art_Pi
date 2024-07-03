from flask import Flask, request, abort
from PIL import Image
from io import BytesIO
import json
import logging
import time
# Waveshare Display Library
import epd7in5

# Variables
allowed_ext = ['png', 'jpg', 'jpeg', 'gif', 'tiff', 'bmp']
display_size = (800, 480)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def upload_to_display():
    logging.info("Image Uploaded")
    image_file = request.files['image']
    image_ext = image_file.filename.split('.')[-1]
    if image_file and image_ext in allowed_ext:
      logging.debug("Preparing Image")
      image = Image.open(BytesIO(image_file.read()))
      # Convert the image to black and white
      image_bw = image.convert("L")
      # Resize if necessary
      image_size = image_bw.size
      if image_size != display_size:
        logging.debug("Resizing Image")
        image_bw = image_bw.resize(display_size)
      # Initialize Display
      logging.debug("Initializing Display")
      epd = epd7in5.EPD()
      epd.init()
      # Displaying Image
      logging.debug("Displaying Image")
      epd.display(epd.getbuffer(image_bw))
      logging.debug("Sleeping Display")
      epd.sleep()
    else:
       logging.error("Upload Error")
       abort(400)
    time.sleep(30)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
  app.run()
