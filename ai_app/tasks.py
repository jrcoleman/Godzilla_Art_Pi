# General Libraries
import time
import logging
# Celery Libraries
from celery import Celery
# stable diffusion module
from stable_diffusion import gen_api_image

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def local(prompt:str):
  time.sleep(60)
  return prompt

@app.task
def api(prompt:str):
  gen_api_image(prompt)
  return "Done"
