from flask import Flask, render_template, request, url_for, flash, redirect
from stable_diffusion import gen_api_image

app = Flask(__name__)

@app.route('/')
def index():
  args = request.args
  prompt = request.form['prompt']
  method = request.form.get('method')
  return render_template('index.html')

if __name__ == '__main__':
  app.run()