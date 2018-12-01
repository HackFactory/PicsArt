import json
import os
import sys
from flask import Flask, request
from flask import jsonify

from tqdm import tqdm

sys.path.insert(0, "/home/ubuntu/PicsArt/")

import utils
from model import ModelEmb
#from instagram_parser.hack_bot import Hack_bot

app = Flask(__name__)
app.config.from_object(__name__)

user_emb_table = {"user": "emb"}

user_profile_photo = {"user": "photo_url"}

#hackbot = Hack_bot()
model = ModelEmb()


@app.route('/instagram_preprocessing/', methods=['GET', 'POST'])
def instagram_preprocessing():
    print("I got a file")
    print(request)
    instagram_login = utils.prepare_login(request)
    json_user_images_links = {
        "nm.tismoney": ["https://scontent-arn2-1.cdninstagram.com/vp/d823d5d55dee8c31dff13928b51fc99f/5C965EEF/t51.2885-19/s320x320/41105233_1812609548786318_770863607914168320_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/a05b4281cbd81433c49e620fea1ecc94/5C9B1DF8/t51.2885-15/sh0.08/e35/s640x640/43556265_948345168689036_2367865772941770752_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/fddc640533b5b38997a200e33e2debfd/5CA2FCF3/t51.2885-15/sh0.08/e35/s640x640/41449619_1794170000700220_4264116412768845824_n.jpg"]
    }
    #json_user_images_links = hackbot.
    for folower_instagram_nickname in tqdm(json_user_images_links.keys()):
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