# coding=utf-8
from urlparse import urljoin
import os
import requests
import logging
import json

from applications.user_center.agents import get_uc_internal_domain_list
from applications.user_center.utils import RoundTripDecoder
from utils.errcode import WX_FETCH_VOICE_FAIL, WX_GET_ACCESS_TOKEN_FAIL
from utils.tools import BusinessException


logger = logging.getLogger(__name__)


def get_access_token(school_id):
    from applications.common.services import domain_uc
    #从用户中心获取微信access_token，用户中心保证token不过期
    uc_url = os.path.join(get_uc_internal_domain_list()[0], 'get/access_token')
    logger.info('visit user_center %s to get access_token' % uc_url)
    response = requests.get(
        uc_url,
        stream=True,
        params={'sid': str(school_id)})
    response_dict = json.loads(response.text, cls=RoundTripDecoder)
    if response.status_code != 200 or 'c' not in response_dict or response_dict['c'] != 0:
        raise BusinessException(WX_GET_ACCESS_TOKEN_FAIL)
    return response_dict['d']


def fetch(user, media_id, token=None):
    # 从微信服务器下载
    access_token = token or get_access_token(user.school.id)
    payload = {
        'access_token': access_token,
        'media_id': str(media_id),
    }
    response = requests.get(
        'http://api.weixin.qq.com/cgi-bin/media/get',
        stream=True,
        params=payload)
    logger.info('fetch media %s from weixin, response_code: %s, response_head: %s' % (media_id, response.status_code, response.headers))
    if response.status_code != 200:
        raise BusinessException(WX_FETCH_VOICE_FAIL)
    elif 'errcode' in response.content:
        logger.error('fetch media %s fail, reason: %s' % (media_id, response.content))
        raise BusinessException(WX_FETCH_VOICE_FAIL)
    else:
        return response
