from flask import Flask
from flask import render_template
import os, json, time, urllib2

app = Flask(__name__)

def get_weather():
  url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=Mexico&cnt=10&mode=json&units=metric'
  response =  urllib2.urlopen(url).read()
  return response

@app.route("/")
def index():
  return get_weather() 


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
