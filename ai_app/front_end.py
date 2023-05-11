# General libraries
import json
import logging
import shutil
# Flask libaries
from flask import Flask, render_template, request, url_for, flash, redirect
# Celery libraries
from tasks import local, api, godzilla, upload_image

private_conf_f = open('private_conf.json')
private_conf = json.load(private_conf_f)
private_conf_f.close()

flower_addr = private_conf['flower_addr']
output_path = private_conf['output_path']
image_name = private_conf['image_name']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    prompt = request.form['prompt']
    method = request.form.get('method')
    if not prompt and method != "godzilla":
       return render_template('index.html', submit_message=f"No prompt set. No request submitted.", flower_addr=flower_addr)
    if method == "local":
      res = local.delay(prompt)
    elif method == "api":
      res = api.delay(prompt)
    elif method == "godzilla":
      res = godzilla.delay()
    else:
      return render_template('index.html', submit_message=f"Incorrect method. No request submitted.", flower_addr=flower_addr)
    return render_template('index.html', submit_message=f"New {method} request submitted. State: {res.state} Id: {res.id}", flower_addr=flower_addr)
  return render_template('index.html', submit_message="", flower_addr=flower_addr)

@app.route('/image', methods=['GET'])
def image():
  image_path=f"{output_path}/{image_name}.png"
  shutil.copy(image_path, f"./static/{image_name}.png")
  return render_template('image.html', submit_message="", image_name=f"{image_name}.png")
if __name__ == '__main__':
  app.run()

@app.route('/resend')
def resend():
  image_path=f"{output_path}/{image_name}.png"
  upload_image(image_path)
  return redirect(url_for('index'))
