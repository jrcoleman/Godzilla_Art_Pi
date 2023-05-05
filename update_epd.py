from PIL import Image
import logging
# Waveshare Display Library
from waveshare_epd import epd7in5_V2_fast

display_size = (800, 480)

# Open Image
image = Image.open("test_image.png")
# Convert the image to black and white
image_bw = image.convert("L")
# Resize if necessary
image_size = image_bw.size
if image_size != display_size:
  logging.info("Resizing Image")
  image_bw = image_bw.resize(display_size)

# Initialize Display
epd = epd7in5_V2_fast.EPD()
logging.info("Initializing Display")
epd.init()
# epd.Clear() # JC Note: is it necessary to clear epd or will the epd.display work without it?
# Displaying Image
logging.info("Displaying Image")
epd.display(epd.getbuffer(image_bw))
logging.info("Sleeping Display")
epd.sleep()
