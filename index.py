from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import send_file
import os, json, time, urllib2, io
import datetime
import qrcode
import cStringIO

app = Flask(__name__)

def get_weather(city):
  url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=10&mode=json&units=metric'.format(city)
  response =  urllib2.urlopen(url).read()
  return response

def genQR(data="test"):
  qr=qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size = 15,
        border = 3)
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image()
  return img

@app.route("/")
def index():
  search_city = request.args.get("searchcity")

  if not search_city:
    search_city = request.cookies.get("last_city")
  if not search_city:
    search_city="Mexico City"

  data = json.loads(get_weather(search_city))
  
  try:
    city = data['city']['name']
  except KeyError:
    return render_template("invalid_city.html", user_input=search_city)

  country = data['city']['country']
  forecast_list = []

  for d in data.get("list"):
    day = time.strftime('%d %B', time.localtime(d.get('dt')))
    mini = d.get('temp').get('min')
    maxi = d.get('temp').get('max')
    description = d.get('weather')[0].get('description')
    forecast_list.append((day,mini,maxi,description))
  
  response = make_response(render_template("index.html", forecast_list=forecast_list, city=city, country=country))

  if request.args.get("remember"):
    response.set_cookie("last_city","{},{}".format(city,country), expires=datetime.datetime.today()+ datetime.timedelta(365))

  return response

@app.route("/qr_img/")
def gen_qr_image():
  to_display = time.strftime('%Y%m%d%H%M%S%Z',time.localtime())
  img_buf=cStringIO.StringIO()
  img = genQR(data=to_display)
  img.save(img_buf,'PNG')
  img_buf.seek(0)
  #resp = make_response(image, 304)
  #resp.content_type="image/png"
  #resp.headers['Accept-Ranges']="bytes"
  #resp.headers['Access-Control-Allow-Origin']="*"
  #resp.headers['Content-Disposition']="inline; filename=\"none.png\""
  #resp.headers['Connection']="Keep-Alive"
  #resp.headers['Age']=0
  #resp.headers['Cache-Control']="max-age=300"
  #resp.headers['X-Cache']="HIT"
  #resp.headers['Content-Type']="image/png"
  return send_file(img_buf, mimetype='image/png')
  #return image 
  
@app.route("/qr/")
def gen_qr():
  qr_code=gen_qr_image()
  return render_template("qr.html", qr_code=qr_code)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
