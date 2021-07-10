"""
How to add a feature :
    1. make sure to add the feature to the features.py file and follow the instructions there
    2. add the name of the name of the function to the REQUEST_FEATURES or RESPONSE_FEATURES down below .
        add the function like so :
            "feature name":function name,
        note : there is no () after the function name !!
    3. make sure to add the "feature name" to the gui_adblocker.py in the FEATURES list
"""

from features import *
import re2
import logging
from mitmproxy.script import concurrent
from mitmproxy import http
from inspect import signature
from adblockparser import AdblockRules
import classes
from glob import glob

# pre compile the regex to speed the matching

IMAGE_MATCHER = re2.compile(r"\.(png|jpe?g|gif)$")
SCRIPT_MATCHER = re2.compile(r"\.(js)$")
STYLESHEET_MATCHER = re2.compile(r"\.(css)$")

IMG_TYPE = {
    "png": "png",
    "jpeg": "jpeg",
    "svg+xml": "svg",
    "gif": "gif"
}

REQUEST_FEATURES = {  # your request feature come here <----------

}

RESPONSE_FEATURES = {  # your response feature come here <----------
    'css': css_feature,
    "inject img": inject_img,
    "block img by condition": block_img_by_condition,
    "find and replace": find_and_replace
}

rules = ""

LOG_LEVEL = {
    1: logging.debug,
    2: logging.info,
    3: logging.warning
}


def log(msg, level=1):
    """"
    log the msg based on the importance level
    input : the msg and the level of importance
    output: none
    """
    if level in LOG_LEVEL.keys():
        LOG_LEVEL[level](msg)


def combined(filenames):
    """
    Open and combine many files into a single generator
    input : list of file paths
    output : generator of all lines
    """
    for filename in filenames:
        with open(filename) as file:
            for line in file:
                yield line


def load_rules(blocklists):
    """
    creates the rules for the ad block parser
    make it use re2 and allocate space for it
    must get a generator
    input : list of file paths to the block lists
    output : the rules to the blocker
    """
    rules = AdblockRules(
        combined(blocklists),
        use_re2=True,
        max_mem=512 * 1024 * 1024
        # mem allocated to re2 for matching
    )
    return rules


def load_blocklist():
    """"
    get the blocklists from glob
    check if there is something in the blocklist dir
    print the lists
    and update the rules (and load it )
    input : none
    output: none
    """
    global rules
    blocklists = glob("blocklists/*")  # returns all files in blocklist

    if len(blocklists) == 0:
        print("Error, no blocklists found in 'blocklists/'. Please run the 'update-blocklists' script.")
        raise SystemExit

    else:
        print("* Available blocklists:")
        for block_list in blocklists:
            print("  |_ %s" % block_list)

    print("* Loading blocklists...")
    rules = load_rules(blocklists)
    print("")
    print("* Done! Proxy server is ready to go!")


load_blocklist()


@concurrent
def request(flow):
    """
    handle all the requests
    checks for the type (with re2)
    finds the need to apply  a feature and handle it .
    input : http flow
    output : none
    """
    global rules

    options = {'domain': flow.request.host, "image": IMAGE_MATCHER.search(flow.request.path),
               "script": SCRIPT_MATCHER.search(flow.request.path),
               "stylesheet": STYLESHEET_MATCHER.search(flow.request.path)}
    request_obj = classes.request(flow)
    if rules.should_block(flow.request.url, options):
        log("vvvvvvvvvvvvvvvvvvvv BLOCKED vvvvvvvvvvvvvvvvvvvvvvvvvvv\naccept: " + flow.request.headers.get(
            "Accept") + "\nblocked-url: " + flow.request.url + "\n""^^^^^^^^^^^^^^^^^^^^ BLOCKED "
                                                               "^^^^^^^^^^^^^^^^^^^^^^^^^^^",
            level=3)
        flow.response = http.HTTPResponse.make(  # create an http response
            200,
            b"BLOCKED.",
            {"Content-Type": "text/html"}
        )

    else:
        with open("/home/eyal/Desktop/adblock/files/feature.txt", 'r') as file:
            feature = file.readline()
            if feature in REQUEST_FEATURES.keys():
                request_obj = REQUEST_FEATURES[feature](request_obj)
    if request_obj is not None:
        update_the_request(request_obj, flow)


def update_the_request(obj, flow):
    """"
    get the request object and apply the changes to the flow request
    input : the request object and the flow
    output : none
    """
    list_of_req = obj.update_flow()
    flow.request.content = list_of_req[0]
    flow.request.url = list_of_req[1]


@concurrent
def response(flow):
    """"
    handle all the responses
    if a feature is applied make sure to direct the response object to the function .
    input : HTTP flow
    output : none
    """
    response_obj = classes.response(flow)
    with open("/home/eyal/Desktop/adblock/files/feature.txt", "r") as file:
        if os.stat("/home/eyal/Desktop/adblock/files/feature.txt").st_size != 0:
            feature_type = file.readline().strip()
            if feature_type in RESPONSE_FEATURES.keys():
                len_of_params = len(signature(RESPONSE_FEATURES[feature_type]).parameters.keys())
                if len_of_params == 1:
                    response_obj = RESPONSE_FEATURES[feature_type](response_obj)
                if len_of_params == 2:
                    response_obj = RESPONSE_FEATURES[feature_type](response_obj, file.readline().strip())
                if len_of_params == 3:
                    response_obj = RESPONSE_FEATURES[feature_type](response_obj, file.readline().strip(),
                                                                   file.readline().strip())

    if response_obj is not None:
        update_the_response(response_obj, flow)


def update_the_response(obj, flow):
    """"
    get the response object and apply the info to the response itself .
    input : response object and the flow
    output : none
    """
    list_for_response = obj.update_flow()
    flow.response.content = list_for_response[0]
    flow.response.headers["content-type"] = list_for_response[1]
    flow.response.headers["content-length"] = list_for_response[2]
    flow.response.headers["status-code"] = str(list_for_response[3])



