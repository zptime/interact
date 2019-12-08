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


def get_usercenter_address():
    this_service = Service.objects.filter(code__in=['user_center', ]).first()
    url = urlparse(this_service.intranet_url)
    return '{uri.scheme}://{uri.netloc}'.format(uri=url)


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


def remote_request(domain, request_path, payload):
    try:
        response = requests.post(
            urljoin(domain, request_path),
            data=payload,
            timeout=REQUEST_TIMEOUT)
        return response_with_status(json.loads(response.text), response.status_code)
    except Exception as e:
        logger.exception(e)
        raise e



