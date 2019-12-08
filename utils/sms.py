# coding=utf8
import hashlib
import httplib
import json
import logging
import os
import random
import string
import urllib
import time

from django.conf import settings

from utils.errcode import SMSCODE_SEND_FAIL
from utils.tools import BusinessException


def sendsms(mobile):
    def get_nonce(length):
        """
             get不可重复字符串
        """
        # 不可重复字符串
        random_str = ''.join(random.sample(string.ascii_letters, length))
        return  random_str

    # get the current time str use timestamp
    def get_curtime_str():
        now = time.time()
        curtime = int(now)
        return str(curtime)

    # get the sha1 hexcode string : AppSecret + Nounce + Curtime
    def get_sha1_code(AppSecret, Nonce, Curtime):
        sha1obj = hashlib.sha1()
        sha1obj.update(AppSecret + Nonce + Curtime)
        sha1code = sha1obj.hexdigest()
        return sha1code

    result = dict()
    if not mobile:
        raise BusinessException(SMSCODE_SEND_FAIL)

    AppKey = settings.APPKEY_EASY
    AppSecret = settings.APPSECRET_EASY
    templateid = settings.TEMPLATEID_EASY

    Nonce_16 = get_nonce(16)
    Curtime = get_curtime_str()
    CheckSum = get_sha1_code(AppSecret, Nonce_16, Curtime)

    data = {"mobile":mobile,
            "templateid":templateid,
            }

    data = urllib.urlencode(data)

    headers = {"AppKey":AppKey,
               "Content-Type":'application/x-www-form-urlencoded',
               "CurTime":Curtime,
               "CheckSum":CheckSum,
               "Nonce":Nonce_16,
               }

    # get the verify code from remote
    conn = httplib.HTTPSConnection("api.netease.im")

    conn.request('POST', '/sms/sendcode.action', data, headers)
    r1 = conn.getresponse()
    data1 = r1.read()
    conn.close()
    data1 = json.loads(data1, 'utf-8')
    code = ''
    if data1['code'] == 200:
        code = data1['obj']
        msg = data1['msg']
        result['thirdcode'] = data1['obj']
        result['thirdmsg'] = data1['msg']
        result['timestamp'] = Curtime
    else:
        raise BusinessException(SMSCODE_SEND_FAIL)
    return result