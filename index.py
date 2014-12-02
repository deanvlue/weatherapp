from flask import Flask

import os

app = Flask(__name__)

@app.route("/")
def index():
  return "Hola mundo!"

@app.route("/goodbye/")
def goodbye():
  return "Goodbye!"

@app.route("/hello/<name>/<int:age>")
def hello(name,age):
  
  respuesta = ""

  if age == 42:
    respuesta="Ah parece que tienes la respuesta del universo y todo el pedo"  
  else:  
    respuesta= "Hello {} you little fucker you are {} years old".format(name, age)

  return respuesta


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
