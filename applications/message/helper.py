# -*- coding=utf-8 -*-

import json
import logging
from urlparse import urlparse, urljoin

import requests
from django.conf import settings
from django.http import HttpResponse

from applications.message.const import REQUEST_TIMEOUT
from applications.user_center.models import Service


logger = logging.getLogger(__name__)


MESSAGE_SYSTEM_NAME = 'message'


def get_message_sys_address():
    if getattr(settings, 'MC_INFORMAL_DOMAIN', None):
        domain = settings.MC_INFORMAL_DOMAIN
    else:
        this_service = Service.objects.filter(code__in=[MESSAGE_SYSTEM_NAME,]).first()
        parsed_uri = urlparse(this_service.intranet_url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def response200(result):
    """
        OK
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    

def response_with_status(result, x):
    """
        http with status code
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=x)


def _remote_call(payload):
    try:
        response = requests.post(
            urljoin(get_message_sys_address(), '/api/internal/proxy'),
            data=payload,
            timeout=REQUEST_TIMEOUT)
        return response_with_status(json.loads(response.text), response.status_code)
    except Exception as e:
        logger.exception(e)
        raise e



