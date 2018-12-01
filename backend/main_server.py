import json
import os
import sys
from flask import Flask, request
from flask import jsonify

import utils

app = Flask(__name__)
app.config.from_object(__name__)

user_emb_table = {"user": [embedding]}


@app.route('/instagram_preprocessing/', methods=['GET', 'POST'])
def instagram_preprocessing():
    print("I got a file")
    print(request)
    instagram_login = utils.prepare_login(request)
    
    return jsonify({"sucsess": "ok"})

@app.route('/analyze_galery/', methods=['GET', 'POST'])
def analyze_galery():
    return jsonify({"sucsess": "ok"})

@app.route('/ping/', methods=['GET'])
def ping():
    return jsonify({"answer": "hello, world!"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)