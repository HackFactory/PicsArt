import json
import os
import sys
from flask import Flask, request
from flask import jsonify

from tqdm import tqdm

sys.path.insert(0, "/home/ubuntu/PicsArt/")

import utils
from model import ModelEmb
from instagram_parser.hack_bot import Hack_bot

app = Flask(__name__)
app.config.from_object(__name__)

user_emb_table = {"user": "emb"}

user_profile_photo = {"user": "photo_url"}

hackbot = Hack_bot()
model = ModelEmb()

@app.route('/instagram_preprocessing/', methods=['GET', 'POST'])
def instagram_preprocessing():
    print("I got a file")
    print(request)
    instagram_login = utils.prepare_login(request)
    # json_user_images_links = hackbot.
    
    for folower_instagram_nickname in tqdm(json_user_images_links.keys():
        user_profile_photo[folower_instagram_nickname] = json_user_images_links[folower_instagram_nickname][0]
        images_links = json_user_images_links[folower_instagram_nickname][1:]
        images = utils.read_images(images_links)
        embedding = model.run(images)
        user_emb_table[folower_instagram_nickname] = embedding
            
    return jsonify({"sucsess": "ok"})

@app.route('/analyze_galery/', methods=['GET', 'POST'])
def analyze_galery():
    return jsonify({"sucsess": "ok"})

@app.route('/ping/', methods=['GET'])
def ping():
    return jsonify({"answer": "hello, world!"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)