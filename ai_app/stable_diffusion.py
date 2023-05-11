# AI Model
from diffusers import StableDiffusionPipeline
# General
from PIL import Image
import logging
import json
import requests
from io import BytesIO
import time
import re

# Get Private Configuration
private_conf_f = open('private_conf.json')
private_conf = json.load(private_conf_f)
private_conf_f.close()

# Variables
model_local = "./stable-diffusion-2-1"
model_api = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
hf_token = private_conf['hf_token']
output_path = private_conf['output_path']
image_name = private_conf['image_name']

def save_image(image, prompt):
  image_latest = f"{output_path}/{image_name}.png"
  prompt_short = re.sub(r'\W+', '', prompt)[0 : 25]
  image_prompt = f"{output_path}/{image_name}_{prompt_short}.png"
  image.save(image_latest)
  image.save(image_prompt)
  return image_latest

def gen_api_image(prompt:str):
  payload = {
    "inputs": prompt,
    "parameters": {
      "width": 800,
      "height": 480,
      "guidance_scale": 5
    }
  }
  headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json",
    "Accept": "image/png"
  }
  retry = True
  while(retry): 
    logging.info("Requesting image.")
    response = requests.post(model_api, headers=headers, json=payload)
    logging.info("Response received.")
    logging.info(f"Status: {response.status_code}")
    logging.debug(f"Headers: {response.headers}")
    if response.status_code == 200:
      image = Image.open(BytesIO(response.content))
      retry = False
    elif response.status_code == 503:
      logging.info("503 Throttle. Waiting to resubmit.")
      time.sleep(30)
    else:
      logging.error(f"Request error: {response.text}")
      raise Exception("API Request Error.")
  return save_image(image, prompt)
def gen_local_image(prompt:str):
  pipe = StableDiffusionPipeline.from_pretrained(model_local, low_cpu_mem_usage=True)
  pipe.to("cpu")
  image = pipe(prompt, width=800, height=480, num_inference_steps=30).images[0]
  return save_image(image, prompt)
