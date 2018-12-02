import json
import os
import sys
from flask import Flask, request
from flask import jsonify

import numpy as np
import cv2

from tqdm import tqdm

sys.path.insert(0, "/home/ubuntu/PicsArt/")

import utils
from model import RankModel
from instagram_parser.hack_bot import Hack_bot

from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)
app.config.from_object(__name__)

nicknames_list = []

user_emb_table = {} # "user": [emb]

user_profile_photo = {} #"user": "photo_url"

hackbot = Hack_bot()
model = RankModel()


@app.route('/instagram_preprocessing/', methods=['GET', 'POST'])
def instagram_preprocessing():
    print("I got a file")
    print(request)
    instagram_login = utils.prepare_login(request)
    if utils.run_instabot(instagram_login):
        #json_user_images_links = hackbot.get_json_profile(instagram_login)
        json_user_images_links = {}
    else:
        with open("../instagram_parser/dumps/{}.json".format(instagram_login)) as f:
            json_user_images_links = json.load(f)
    
    print(json_user_images_links.keys())
    to_nn = []
    global user_emb_table
    global user_profile_photo
    global nicknames_list
    user_profile_photo = {}
    user_emb_table = {}
    nicknames_list = []
    
    for folower_instagram_nickname in tqdm(json_user_images_links.keys()):
        if len(json_user_images_links[folower_instagram_nickname]) > 1:
            user_profile_photo[folower_instagram_nickname] = json_user_images_links[folower_instagram_nickname][0]
            nicknames_list.append(folower_instagram_nickname)
            to_nn.append(json_user_images_links[folower_instagram_nickname][1:])

    model.update_urls(to_nn)    
    return jsonify({"sucsess": "ok"})

@app.route('/analyze_galery_test_recieve/', methods=['GET', 'POST'])
def analyze_galery_test_recieve():
    print(request.files)
    filestr = request.files['image'].read()
    nparr = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return jsonify({"image shape": list(img.shape)})

@app.route('/analyze_galery/', methods=['GET', 'POST'])
def analyze_galery():
    print(request.files)
    filestr = request.files['image'].read()
    nparr = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(img.shape)
    img = model.preprocess_image(img)
    print(img.shape)
    indexes, probs = model.recs(img, mode="emb")
    print(nicknames_list)
    ranked_nicknames = np.array(nicknames_list)[indexes]
    ranked_names = hackbot.get_names_from_niks(ranked_nicknames)
    #ranked_names = ranked_nicknames
    resp = []
    for nick, name, index, prob in zip(ranked_nicknames, ranked_names, indexes, probs):
        photo_url = user_profile_photo[nick]
        resp.append([photo_url, nick, name, prob])
    return jsonify(resp)

@app.route('/ping/', methods=['GET'])
def ping():
    return jsonify({"answer": "hello, world!"})

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host="0.0.0.0", port=8888, debug=False)