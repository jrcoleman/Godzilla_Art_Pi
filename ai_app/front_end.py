# General libraries
import json
import logging
# Flask libaries
from flask import Flask, render_template, request, url_for, flash, redirect
# Celery libraries
from tasks import local, api

private_conf_f = open('private_conf.json')
private_conf = json.load(private_conf_f)
private_conf_f.close()

flower_addr = private_conf['flower_addr']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    prompt = request.form['prompt']
    method = request.form.get('method')
    if not prompt:
       return render_template('index.html', submit_message=f"No prompt set. No request submitted.", flower_addr=flower_addr)
    if method == "local":
      res = local.delay(prompt)
    elif method == "api":
      res = api.delay(prompt)
    else:
      return render_template('index.html', submit_message=f"Incorrect method. No request submitted.", flower_addr=flower_addr)
    return render_template('index.html', submit_message=f"New {method} request submitted. State: {res.state} Id: {res.id}", flower_addr=flower_addr)
  return render_template('index.html', submit_message="", flower_addr=flower_addr)

if __name__ == '__main__':
  app.run()
