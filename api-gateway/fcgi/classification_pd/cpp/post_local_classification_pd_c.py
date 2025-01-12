# Copyright (C) 2020 Intel Corporation


import requests
import json
import base64
import urllib.parse
import hashlib  ## python3
import time
import random
from collections import OrderedDict
import argparse
import sys

def main(args):
    #start_time = time.time()
    appkey = 'di6ik9b9JiYfImUB'

    f = open(args.image,"rb")
    base64_data = base64.b64encode(f.read())
    time_stamp = int(time.time())
    random_let = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',10))
    #print(random_let)

    params = OrderedDict()
    params['app_id'] = 2128571502
    params['image'] = base64_data
    params['nonce_str'] =time_stamp
    params['time_stamp'] = time_stamp
    query_string = urllib.parse.urlencode(params)
    query_string += '&app_key=' + appkey
    m = hashlib.md5(query_string.encode())
    sign = m.hexdigest().upper()
    params['sign'] = sign


    start_time = time.time()

    ## notice: must uset http_proxy, otherwise can not get link
    #url = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr';
    url= 'http://localhost:8080/cgi-bin/fcgi_classification_pd'
    res = requests.post(url,data=params)

    processing_time = time.time() - start_time


    if res.status_code == 200:
        print(res.content.decode('utf-8'))
        print("processing time is:", processing_time)
    else:
        print ("the error number is:", res.status_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "it's usage tip.", description = "help info.")
    parser.add_argument("-i", "--image", default = "./input_data/dog.jpg", help = "the path of the picture")

    args = parser.parse_args()
    main(args)
