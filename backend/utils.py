import os
import random
from multiprocessing.dummy import Pool as ThreadPool
from skimage import io, transform
import cv2
import numpy as np

import requests

def prepare_login(request):
    return request.args.to_dict()["login"]

def send_answer(answer):
    return {"text": answer}

def read_images(array_links, shape=(224, 224, 3)):
    results = np.array(list(map(lambda path: transform.resize(io.imread(path), shape), array_links)))
    return results
