import os
import random
from multiprocessing.dummy import Pool as ThreadPool
from skimage import io, transform
import cv2
import numpy as np

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from glob import glob

import requests

def prepare_login(request):
    return request.args.to_dict()["login"]

def send_answer(answer):
    return {"text": answer}

def read_images(array_links, shape=(224, 224, 3)):
    results = np.array(list(map(lambda path: transform.resize(io.imread(path), shape), array_links)))
    return results

def shit_preprocess(urls):
    imgs = map(io.imread, urls)
    imgs = map(image.array_to_img, imgs)
    imgs = [img.resize((224, 224)) for img in imgs]
    imgs = map(image.img_to_array, imgs)
    imgs = map(preprocess_input, imgs)
    return np.array(list(imgs))

def run_instabot(nickname):
    dumps = list(map(lambda x: os.path.basename(x), glob("../instagram_parser/dumps/*")))
    print(dumps)
    if "{}.json".format(nickname) in dumps:
        return False
    return True
