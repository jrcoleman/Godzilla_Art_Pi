# General Libraries
import time
import logging
import requests
from PIL import Image
# Celery Libraries
from celery import Celery
# stable diffusion module
from stable_diffusion import gen_api_image, gen_local_image

# Variables
display_url = 'http://raspberrypi.local:5000'

# Initialize celery
app = Celery('tasks')
app.config_from_object('celeryconfig')

# Functions
def upload_image(image_path):
  files = {'image': open(image_path,'rb')}
  r = requests.post(display_url, files=files)
  logging.debug(f"Status: {r.status_code}. Text: {r.text}")

# Tasks
@app.task
def local(prompt:str):
  logging.info("Starting API image generation request.")
  image_path = gen_local_image(prompt)
  upload_image(image_path)
  logging.info("API image generation request completed.")
  return "Success"

@app.task
def api(prompt:str):
  logging.info("Starting API image generation request.")
  image_path = gen_api_image(prompt)
  upload_image(image_path)
  logging.info("API image generation request completed.")
  return "Success"