# General Libraries
import logging
import requests
import json
import random
# Celery Libraries
from celery import Celery
from celery.schedules import crontab
# stable diffusion module
from stable_diffusion import gen_api_image, gen_local_image

# Display
display_url = 'http://raspberrypi.local:5000'

# Prompt Generation
godzilla_dict_f = open('godzilla.json')
godzilla_dict = json.load(godzilla_dict_f)
godzilla_dict_f.close()
monster_d = godzilla_dict['monster']
monster_l = list(monster_d.keys())
monster_w = [ monster_d[monster] for monster in monster_l ]
verb_d = godzilla_dict['verb']
verb_l = list(verb_d.keys())
verb_w = [ verb_d[verb]['w'] for verb in verb_l ]
style_d = godzilla_dict['style']
style_l = list(style_d.keys())
style_w = [ style_d[style] for style in style_l ]

# Initialize celery
app = Celery('tasks')
app.config_from_object('celeryconfig')

# Functions
def upload_image(image_path):
  files = {'image': open(image_path,'rb')}
  r = requests.post(display_url, files=files)
  logging.debug(f"Status: {r.status_code}. Text: {r.text}")

def create_godzilla_prompt():
  verb = random.choices(verb_l, verb_w)[0]
  monsters = random.choices(monster_l, monster_w, k=verb_d[verb]['max'])
  style = random.choices(style_l, style_w)[0]
  prompt = f"{monsters[0]} {verb} "
  if len(monsters) > 1:
    prompt+=f"{' and '.join(monsters[1:])} "
  prompt+=f"in the style of {style}."
  return prompt

# Tasks
@app.task
def local(prompt:str):
  logging.info("Starting API image generation request.")
  logging.info(f"Prompt: {prompt}")
  image_path = gen_local_image(prompt)
  upload_image(image_path)
  logging.info("API image generation request completed.")
  return "Success"

@app.task
def api(prompt:str):
  logging.info("Starting API image generation request.")
  logging.info(f"Prompt: {prompt}")
  image_path = gen_api_image(prompt)
  upload_image(image_path)
  logging.info("API image generation request completed.")
  return "Success"

@app.task
def godzilla():
  logging.info("Creating Godzilla prompt.")
  prompt = create_godzilla_prompt()
  return local.delay(prompt)


# Scheduled Tasks
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(minute=0, hour='6,8,10,12,14,16,18,20,22'),
    godzilla.s()
  )
