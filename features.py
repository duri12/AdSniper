"""
How to add a feature :
    1. all the features functions MUST get a request or a response object
    2. all the features functions MUST  return the object with whatever changes .
    3. you can get up to 2 more user inputs from the gui just add params to the function .
    4. if a function has more than 3 parameters (the request/response and 2 more params) it will not be called
    5. when working with images the best and fastest images are png and as small as possible.
    that is why there is a library called to_png with functions to convert some image types to png .
    6. to add your function to the right places in adblock.py and gui_adblocker.py
"""

import os
import re
import cv2
import numpy as np
import time
import subprocess
import files.to_png as to_png

CONVERTION = {
    "gif": to_png.gif2png,
    "png": to_png.svg2png,
    "jpeg": to_png.jpeg2png
}

IMG_TYPE = {
    "png": "png",
    "jpeg": "jpeg",
    "svg+xml": "svg",
    "gif": "gif"
}


def inject_img(responce_obj, path):
    """
    get the response and an img
    and injects the img
    input: the path to the image and the response object
    out : the response object
    """
    if "image" in responce_obj.content_type:
        img = open(path, "rb").read()
        responce_obj.content__length = len(img)
        responce_obj.content = img
        file_extension = os.path.splitext(path)[1]
        responce_obj.content_type = "image/" + file_extension[1::]
    return responce_obj


def css_feature(responce_obj, file_path):
    """"
    get a path to css file and apply to the html page
    input:the css file path and the response obj
    output: the
    """
    with open(file_path, "r") as css:
        content = css.read()
        content = re.sub(r'\t', '', content)
        content = re.sub(r'\n', '', content)
        if responce_obj.content is not None and "text" in responce_obj.content_type:
            decoded_content = responce_obj.content.decode(encoding='UTF-8')
            if "</head>" in decoded_content:
                decoded_content = decoded_content.replace("</head>", "<style>" + content + "</style></head>")
                responce_obj.content = decoded_content.encode(encoding='UTF-8')
    return responce_obj


def should_block_suppurted(obj_responce, path, type):
    """"
    get a path to script , the response object and the type
    if the img should be block. modify the response to a blocked response
    else do not change the request .
    input : the response object , the path to the file and the file typr
    output: modified response object
    """
    if "image" in obj_responce.content_type:
        decoded = cv2.imdecode(np.frombuffer(obj_responce.content, np.uint8), -1)
        epoch = str(time.time())
        cv2.imwrite("/home/eyal/Desktop/adblock/images/" + epoch + "." + type, decoded)
        subprocess.Popen("python3.8 " + path + " /home/eyal/Desktop/adblock/images/" + epoch + "." + type,
                         shell=True)
        os.remove("/home/eyal/Desktop/adblock/images/" + epoch + "." + type)
        with open("/home/eyal/Desktop/adblock/files/to_block", "r") as f:
            cond = f.readline()
        if cond == "True":
            obj_responce.response_code = 20
            obj_responce.content = b"BLOCKED."
            obj_responce.content_type = "text/html"
    return obj_responce


def block_img_by_condition(obj_responce, path):
    """"
    saves all the images and checks for condition ,
    in case of a True block img
    removes all files  to cleanup .
    :params: the response object and the file path
    :returns: the response object
    """
    content_type = obj_responce.content_type.split("/")[1]
    if content_type in IMG_TYPE.keys():
        if content_type in CONVERTION:
            path = CONVERTION[content_type](path)
        obj_responce = should_block_suppurted(obj_responce, path, IMG_TYPE[content_type])
    return obj_responce


def find_and_replace(obj_responce, option1, option2):
    """"
    search in the html for a key word. (option 1)
    if the work is found replace it with the other work (option 2)
    input : the response object , the keyword to change (option 1) and the keyword to change to (option 2)
    output : the response object
    """
    if "text/html" in obj_responce.content_type and type(obj_responce.content) == type(
            "".encode(encoding='UTF-8')):
        obj_responce.content = obj_responce.content.decode(encoding='UTF-8').replace(option1, option2).encode(
            encoding='UTF-8')
    return obj_responce
