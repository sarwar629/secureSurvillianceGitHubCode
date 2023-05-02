from flask import Flask, request
import requests
from app import app

#app.run(debug=True,port=5000)

#app = Flask(__name__)
#app = Flask(__name__)
if __name__ == '__main__':
   host="0.0.0.0"
   port="5000"
   debug=True
   #app.run()
   app.run(host, port, debug=False)