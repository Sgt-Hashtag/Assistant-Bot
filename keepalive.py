from flask import Flask
from threading import Thread

app = Flask('')
#running on a separate thread than bot so that both run at the same Time
@app.route('/')
def home():
  return "Hello. I am Alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target = run)
  t.start()