# -*- coding=utf-8 -*-

from ratelimit.decorators import ratelimit

from django.conf import settings
from django.contrib import auth

from applications.android_ios.services import *
from utils.auth_check import *
from utils.constant import *
from utils.errcode import *
from utils.net_helper import response_exception, response_parameter_error
from utils.parameter import *
from utils.tools import *
from utils import net_helper


logger = logging.getLogger(__name__)


@validate('POST', authenticate=False)
def api_mobile_version(request):
    try:
        mobile_type = get_parameter(request.POST.get('mobile_type'), para_intro=u'移动端类型', valid_check=CHOICES,
            choices=(str(MOBILE_TYPE_APPLE_PHONE), str(MOBILE_TYPE_APPLE_PAD), str(MOBILE_TYPE_ANDROID_PHONE), str(MOBILE_TYPE_ANDROID_PAD)))
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        mobile_version_info = get_mobile_version(mobile_type)
        log_response(request, mobile_version_info)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': mobile_version_info})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('GET', authenticate=False)
def api_mobile_qrcode_info(request):
    try:
        result = get_mobile_qrcode()
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


# @validate('POST', authenticate=False)
# def api_mobile_qrcode_update(request):
#     try:
#         username = get_parameter(request.POST.get('username'), para_intro=u'用户名')
#         password = get_parameter(request.POST.get('password'), para_intro=u'密码')
#         qrcode = get_parameter(request.FILES.get('qrcode'), para_intro=u'二维码图片', valid_check=IMAGE)
#     except InvalidHttpParaException as ihpe:
#         logger.exception(ihpe)
#         return response_parameter_error(ihpe)
#     try:
#         if username != settings.DB_ADMIN:
#             raise BusinessException(AUTH_WRONG_TYPE)
#         user = auth.authenticate(username=username, password=password)
#         if not user or not user.is_active:
#             raise BusinessException(AUTH_WRONG_TYPE)
#
#         update_mobile_qrcode(qrcode)
#         return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
#     except Exception as e:
#         logger.exception(e)
#         return response_exception(e)


@validate('POST', authenticate=False)
def api_mobile_update(request):
    try:
        username = get_parameter(request.POST.get('username'), para_intro=u'用户名')
        password = get_parameter(request.POST.get('password'), para_intro=u'密码')
        type = get_parameter(request.POST.get('mobile_type'), para_intro=u'移动端类型',
            valid_check=CHOICES,
            choices=(str(MOBILE_TYPE_APPLE_PHONE), str(MOBILE_TYPE_APPLE_PAD), str(MOBILE_TYPE_ANDROID_PHONE), str(MOBILE_TYPE_ANDROID_PAD)))
        latest_version = get_parameter(request.POST.get('latest_version'), para_intro=u'最新版本号')
        version_info = get_parameter(request.POST.get('version_info'), para_intro=u'版本信息', allow_null=True, default='')
        latest_pkg = request.FILES.get('latest_pkg')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        if username != settings.DB_ADMIN:
            raise BusinessException(AUTH_WRONG_TYPE)
        user = auth.authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise BusinessException(AUTH_WRONG_TYPE)

        pure_ver_info = version_info.replace('\r','').replace('\n','').replace('\t','')
        result = update_mobile(type, latest_version, latest_pkg, pure_ver_info)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('GET', authenticate=False)
def api_mobile_android_download(request):
    return mobile_android_download(is_upgrade=False)


@validate('GET', authenticate=False)
def api_mobile_android_upgrade(request, fname):
    return mobile_android_download(is_upgrade=True)


@validate('POST', authenticate=False)
def api_mobile_heartbeat(request):
    if not request.user.is_anonymous():
        request.session.modified = True
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})


@validate('POST')
def api_mobile_service_list(request):
    try:
        mobile_type = get_parameter(request.POST.get('mobile_type'), para_intro=u'移动端类型', valid_check=CHOICES,
            choices=(str(MOBILE_TYPE_APPLE_PHONE), str(MOBILE_TYPE_APPLE_PAD), str(MOBILE_TYPE_ANDROID_PHONE), str(MOBILE_TYPE_ANDROID_PAD)))
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    mobile_services = get_mobile_service_list(request.user, mobile_type)
    log_response(request, mobile_services)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': mobile_services})


@validate('POST', authenticate=False)
def api_mobile_passwd_retrieve(request):
    try:
        mobile = get_parameter(request.POST.get('mobile'), para_intro=u'手机号',)
        smscode = get_parameter(request.POST.get('smscode'), para_intro=u'短信验证码')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        password = password_retrieve(mobile, smscode)
    except Exception as e:
        log_exception(e)
        return response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': {
        'password': password
    }})


@validate('POST', authenticate=False)
def api_mobile_passwd_forget_reset(request):
    try:
        mobile = get_parameter(request.POST.get('mobile'), para_intro=u'手机号',)
        smscode = get_parameter(request.POST.get('smscode'), para_intro=u'短信验证码',)
        new_passwd = get_parameter(request.POST.get('new_passwd'), para_intro=u'新的密码',)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        return password_forget(mobile, smscode, new_passwd)
    except Exception as e:
        log_exception(e)
        return response_exception(e)


@validate('GET', authenticate=False)
@ratelimit(key='user_or_ip', rate='5/24h')
def api_mobile_smscode_send(request):
    if getattr(request, 'limited', False):
        return response_ratelimit(msg=u'24小时之内短信验证码只能发送5次')
    try:
        mobile = get_parameter(request.GET.get('mobile'), para_intro=u'手机号',)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        smscheck_send(mobile)
        return response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST', authenticate=False)
@ratelimit(key='user_or_ip', rate='5/1m')
def api_mobile_smscode_verify(request):
    if getattr(request, 'limited', False):
        return response_ratelimit()
    try:
        smscode = get_parameter(request.POST.get('smscode'), para_intro=u'短信验证码')
        mobile = get_parameter(request.POST.get('mobile'), para_intro=u'手机号')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        smscheck_verify(mobile, smscode)
        return response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)

