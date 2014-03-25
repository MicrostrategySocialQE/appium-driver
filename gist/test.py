import re
import requests
import json
import types
import os

def take_screenshot( pic_name):
    paths = pic_name.split("/")
    path = os.getcwd()
    for t in paths[:-1]:
        path = '/'.join([path, t])
        if not os.path.exists(path):
            os.mkdir(path)


take_screenshot("/test1/test2/test3/aaa.png")