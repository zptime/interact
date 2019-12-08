# -*- coding: utf-8 -*-

from Crypto.Cipher import AES

import os
import base64

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0 : -ord(s[-1])]
key = 'JAUC78GVS9B5VSC61M07ZP77'


def encode_AES(content):
    if isinstance(content, unicode):
        content = content.encode('utf-8')
    cipher = AES.new(key)
    encrypted = cipher.encrypt(pad(content))
    return encrypted.encode('hex')


def decode_AES(content):
    cipher = AES.new(key)
    return unpad(cipher.decrypt(content.decode('hex')))


def xor_crypt_string(data, key="58560e24317140589770c1af3bb2905c", encode=False, decode=False):
    from itertools import izip, cycle
    import base64
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored
