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

user_emb_table = {} # "user": [emb]

user_profile_photo = {} #"user": "photo_url"

#hackbot = Hack_bot()
model = ModelEmb()


@app.route('/instagram_preprocessing/', methods=['GET', 'POST'])
def instagram_preprocessing():
    print("I got a file")
    print(request)
    instagram_login = utils.prepare_login(request)
    json_user_images_links = {
        "nm.tismoney": ["https://scontent-arn2-1.cdninstagram.com/vp/d823d5d55dee8c31dff13928b51fc99f/5C965EEF/t51.2885-19/s320x320/41105233_1812609548786318_770863607914168320_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/a05b4281cbd81433c49e620fea1ecc94/5C9B1DF8/t51.2885-15/sh0.08/e35/s640x640/43556265_948345168689036_2367865772941770752_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/fddc640533b5b38997a200e33e2debfd/5CA2FCF3/t51.2885-15/sh0.08/e35/s640x640/41449619_1794170000700220_4264116412768845824_n.jpg"],
        "nastiatolstun": ["https://scontent-arn2-1.cdninstagram.com/vp/89030f6caf72ee651eba481cd6b202e2/5CA12CE2/t51.2885-19/s320x320/40482427_2078359475559046_3340041571830595584_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/2dd1c5d6ad62b671d24623d039fd7046/5CAE345D/t51.2885-15/sh0.08/e35/p640x640/44600295_186845698920576_8509778804713339012_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/aec826cf6be643f342b30eda8ca0b1d7/5C999C7D/t51.2885-15/sh0.08/e35/p640x640/43914258_256833778327187_4891278425613460787_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/33af47676784264604c79fe56a5b05fa/5C95C64D/t51.2885-15/sh0.08/e35/s640x640/45754618_2233136490304606_2132765987628434534_n.jpg"],
        "ushakov.roma": ["https://scontent-arn2-1.cdninstagram.com/vp/71a1b4a63ffa01561f5f6e20b7bc3254/5C9A5D32/t51.2885-19/s150x150/14693933_671218896371000_288462776832098304_a.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/2ef3dd7c048004a55653e30164daae8e/5C8D39E4/t51.2885-15/sh0.08/e35/s640x640/43985247_138677503772423_1881834236909653291_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/e9eafce4256e58c1e5d0fd5a6390da91/5C947C40/t51.2885-15/sh0.08/e35/s640x640/42068933_331899987569953_6725643588537206289_n.jpg", "https://scontent-arn2-1.cdninstagram.com/vp/80bc707ea70f1d43ee1231d4dd347592/5C9A8B90/t51.2885-15/sh0.08/e35/s640x640/42003417_283527345593631_3434722517032611667_n.jpg"]
    }
    
    to_nn = []
    for folower_instagram_nickname in tqdm(json_user_images_links.keys()):
        user_profile_photo[folower_instagram_nickname] = json_user_images_links[folower_instagram_nickname][0]
        to_nn.append(json_user_images_links[folower_instagram_nickname][1:])
    
    model.update_urls(to_nn)    
    return jsonify({"sucsess": "ok"})

@app.route('/analyze_galery/', methods=['GET', 'POST'])
def analyze_galery():
    galery_image = utils.preprocess_galery_image()
    galery_embedding = model.run(galery_image).ravel()
    nicknames = np.array(list(user_emb_table.keys()))
    embeddings = np.array(list(user_emb_table.values()))
    ranks, probs = zip(model.recs(galery_embedding, embeddings))
    ranks = list(ranks); probs = list(probs);

    
    for 
    return jsonify({[
        [],
        []
    ]})

@app.route('/ping/', methods=['GET'])
def ping():
    return jsonify({"answer": "hello, world!"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)