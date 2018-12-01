import os
import random

import requests

def prepare_login(request):
    return request.args.to_dict()["login"]

def send_answer(answer):
    return {"text": answer}