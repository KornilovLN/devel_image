#!/usr/bin/env python3

from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return "Привет, Flask!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    # Keep the container running
    while True:
        time.sleep(1)
