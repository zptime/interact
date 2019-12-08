# -*- coding: utf-8 -*-

import json
from urlparse import urlparse

from django.http import HttpResponse

import platform

from django.utils import http

from utils.errcode import REQUEST_PARAM_ERROR

if 'Windows' in platform.system():
    import win_inet_pton
import socket
import binascii
import json
from applications.user_center.models import Subnet
from utils.constant import *
import logging


logger = logging.getLogger(__name__)


def response200(result):
    """
        OK
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def response_exception(exception, msg=''):
    from utils.tools import BusinessException
    if isinstance(exception, BusinessException):
        final_message = exception.msg
        if msg:
            final_message = u'%s, 原因: %s' % (msg, exception.msg)
        result = {'c': exception.code, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    else:
        final_message = u'请求失败'
        if msg:
            final_message = msg
        result = {'c': -1, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def response_ratelimit():
    from utils.errcode import RATE_LIMIT
    result = {'c': RATE_LIMIT[0], 'm': RATE_LIMIT[1]}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=403)


def response400(result):
    """
        bad request
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=400)


def response_parameter_error(exception):
    dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": exception.message}
    return response400(dict_resp)


def response403(result):
    """
        Fobbidden
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=403)


def response405(result):
    """
        Method not allowed
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=405)


def url_with_scheme_and_location(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def url_with_location(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def ip_in_subnet_list(ip_address, subnet_list):
    for subnet in subnet_list:
        if ip_in_subnetwork(ip_address, subnet):
            return True
    return False


def ip_in_subnetwork(ip_address, subnetwork):

    """
    Returns True if the given IP address belongs to the
    subnetwork expressed in CIDR notation, otherwise False.
    Both parameters are strings.

    Both IPv4 addresses/subnetworks (e.g. "192.168.1.1"
    and "192.168.1.0/24") and IPv6 addresses/subnetworks (e.g.
    "2a02:a448:ddb0::" and "2a02:a448:ddb0::/44") are accepted.
    """

    (ip_integer, version1) = ip_to_integer(ip_address)
    (ip_lower, ip_upper, version2) = subnetwork_to_ip_range(subnetwork)

    if version1 != version2:
        raise ValueError("incompatible IP versions")

    return (ip_lower <= ip_integer <= ip_upper)


def ip_to_integer(ip_address):

    """
    Converts an IP address expressed as a string to its
    representation as an integer value and returns a tuple
    (ip_integer, version), with version being the IP version
    (either 4 or 6).

    Both IPv4 addresses (e.g. "192.168.1.1") and IPv6 addresses
    (e.g. "2a02:a448:ddb0::") are accepted.
    """

    # try parsing the IP address first as IPv4, then as IPv6
    for version in (socket.AF_INET, socket.AF_INET6):

        try:
            ip_hex = socket.inet_pton(version, ip_address)
            ip_integer = int(binascii.hexlify(ip_hex), 16)

            return (ip_integer, 4 if version == socket.AF_INET else 6)
        except:
            pass

    raise ValueError("invalid IP address")


def subnetwork_to_ip_range(subnetwork):

    """
    Returns a tuple (ip_lower, ip_upper, version) containing the
    integer values of the lower and upper IP addresses respectively
    in a subnetwork expressed in CIDR notation (as a string), with
    version being the subnetwork IP version (either 4 or 6).

    Both IPv4 subnetworks (e.g. "192.168.1.0/24") and IPv6
    subnetworks (e.g. "2a02:a448:ddb0::/44") are accepted.
    """

    try:
        fragments = subnetwork.split('/')
        network_prefix = fragments[0]
        netmask_len = int(fragments[1])

        # try parsing the subnetwork first as IPv4, then as IPv6
        for version in (socket.AF_INET, socket.AF_INET6):

            ip_len = 32 if version == socket.AF_INET else 128

            try:
                suffix_mask = (1 << (ip_len - netmask_len)) - 1
                netmask = ((1 << ip_len) - 1) - suffix_mask
                ip_hex = socket.inet_pton(version, str(network_prefix))
                ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask
                ip_upper = ip_lower + suffix_mask

                return (ip_lower,
                        ip_upper,
                        4 if version == socket.AF_INET else 6)
            except:
                pass
    except:
        pass

    raise ValueError("invalid subnetwork")


def is_internal_request(request):
    subnet_list = list(Subnet.objects.filter(del_flag=FALSE_INT).values_list("cidr", flat=True))

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        remoteip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        remoteip = request.META['REMOTE_ADDR']

    if not ip_in_subnet_list(remoteip, subnet_list):
        return False
    else:
        return True



if __name__ == '__main__':
    pass

