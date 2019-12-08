# -*- coding=utf-8 -*-

import logging

from ratelimit.decorators import ratelimit

from utils import auth_check
from utils.auth_check import *
from utils.errcode import *
from utils.net_helper import response_exception, response_parameter_error
from utils.parameter import *
from utils.tools import log_request

from applications.common.services import get_class_member
from applications.contacts.services import get_grp_user_list, get_group_book, invite_user \
    , get_contact_book, delete_user, get_invite_available, dissolve_grp, grp_detail, create_grp, edit_grp, v2_get_invite_available

logger = logging.getLogger(__name__)


@validate('GET')
def api_book_contact(request):
    try:
        result = get_contact_book(request.user, flat=False, except_me=True)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('GET')
def api_book_group(request):
    try:
        result = get_group_book(request.user)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
def api_group_invite_deny(request):
    """
    该接口为V1老接口，V2不再支持
    """
    return response_exception(BusinessException(API_DEPRECATED))


@validate('POST')
def api_group_invite_status(request):
    """
    该接口为V1老接口，V2不再支持
    """
    return response_exception(BusinessException(API_DEPRECATED))


@validate('POST')
def api_group_invite_agree(request):
    """
    该接口为V1老接口，V2不再支持
    """
    return response_exception(BusinessException(API_DEPRECATED))


@validate('POST')
@ratelimit(key='user_or_ip', rate='1/3s')
def api_group_invite(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        group_id = get_parameter(request.POST.get('group_id'), para_intro=u'聊天群组ID', valid_check=INTEGER_POSITIVE)
        invite_users = get_parameter(request.POST.get('invite_users'), para_intro=u'邀请的账号', valid_check=USER_TUPLES)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        invite_who = tools.cut_last_char(invite_users).split(';')
        grp = auth_check.check_get_group(group_id)
        invite_user(request.user, grp, invite_who)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
def api_class_chatid(request):
    """
    该接口为V1老接口，V2不再支持
    """
    return response_exception(BusinessException(API_DEPRECATED))


@validate('POST')
def api_group_chatid(request):
    """
    该接口为V1老接口，V2不再支持
    """
    return response_exception(BusinessException(API_DEPRECATED))


@validate('POST')
def api_chatid(request):
    """
    该接口为V1老接口, V2不再支持, 为了兼容旧版APP，暂时返回虚构结构体
    """
    chat_id = {'chat_id': '000000'}
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': chat_id})
    # return response_exception(BusinessException(API_DEPRECATED))


@validate('POST')
def api_class_user_list(request):
    log_request(request)
    try:
        class_id = get_parameter(request.POST.get('class_id'), para_intro=u'班级ID', valid_check=INTEGER_POSITIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        clazz = auth_check.check_get_class(class_id)
        # 检查自己是否在同一所学校
        if request.user.school != clazz.school:
            raise BusinessException(NO_PRIVILEGE_TO_DETAIL_CLASS)

        result = get_class_member(clazz, flat=True)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
def api_group_user_list(request):
    try:
        group_id = get_parameter(request.POST.get('group_id'), para_intro=u'自定义群组ID', valid_check=INTEGER_POSITIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 仅支持教师操作群组
        if request.user.type != USER_TYPE_TEACHER:
            raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)
        group = auth_check.check_get_group(group_id)
        result = get_grp_user_list(group)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
def api_group_user_quit(request):
    """
    该接口为V1老接口，V2不再支持
    """
    return response_exception(BusinessException(API_DEPRECATED))


@validate('POST')
@ratelimit(key='user_or_ip', rate='1/3s')
def api_group_user_delete(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        group_id = get_parameter(request.POST.get('group_id'), para_intro=u'聊天群组ID', valid_check=INTEGER_POSITIVE)
        delete_users = get_parameter(request.POST.get('delete_users'), para_intro=u'删除的账号', valid_check=USER_TUPLES)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 仅支持教师操作群组
        if request.user.type != USER_TYPE_TEACHER:
            raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)
        group = auth_check.check_get_group(group_id)
        delete_who = tools.cut_last_char(delete_users).split(';')
        delete_user(request.user, group, delete_who)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


# deprecated
@validate('POST')
def api_group_invite_available(request):
    try:
        group_id = get_parameter(request.POST.get('group_id'),
                            para_intro=u'自定义群组ID', valid_check=INTEGER_POSITIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 仅支持教师操作群组
        if request.user.type != USER_TYPE_TEACHER:
            raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)
        group = auth_check.check_get_group(group_id)
        result = get_invite_available(group, request.user)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('GET')
def api_v2_group_invite_available(request):
    try:
        group_id = get_parameter(request.GET.get('group_id'), para_intro=u'自定义群组ID', valid_check=INTEGER_POSITIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        group = auth_check.check_get_group(group_id)
        teacher = get_type_current_user(request.user)
        if not isinstance(teacher, Teacher):
            raise BusinessException(AUTH_WRONG_TYPE)
        result = v2_get_invite_available(group, teacher)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
@ratelimit(key='user_or_ip', rate='1/5s')
def api_group_dissolve(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    log_request(request)
    try:
        group_id = get_parameter(request.POST.get('group_id'), para_intro=u'自定义群组ID')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 仅支持教师操作群组
        if request.user.type != USER_TYPE_TEACHER:
            raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)
        grp = auth_check.check_get_group(group_id)
        dissolve_grp(request.user, grp)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
def api_group_detail(request):
    try:
        group_ids = get_parameter(request.POST.get('group_ids'), para_intro=u'群组ID', valid_check=SEQUENCE_INT)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 仅支持教师操作群组
        if request.user.type != USER_TYPE_TEACHER:
            raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)
        result = grp_detail(group_ids, request.user)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
@ratelimit(key='user_or_ip', rate='1/5s')
def api_group_create(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        group_name = get_parameter(request.POST.get('group_name'), para_intro=u'群组名称')
        invite_users = get_parameter(request.POST.get('invite_users'), allow_null=True, default='')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 仅支持教师操作群组
        if request.user.type != USER_TYPE_TEACHER:
            raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)
        new_grp = create_grp(group_name, request.user)
        invite_who = tools.cut_last_char(invite_users).split(';')
        invite_user(request.user, new_grp, invite_who)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': {'group_id': str(new_grp.id)}})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


@validate('POST')
@ratelimit(key='user_or_ip', rate='1/5s')
def api_group_edit(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        group_id = get_parameter(request.POST.get('group_id'), para_intro=u'群组ID', valid_check=INTEGER_POSITIVE)
        group_name = get_parameter(request.POST.get('group_name'), para_intro=u'群组名称')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 仅支持教师操作群组
        if request.user.type != USER_TYPE_TEACHER:
            raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)
        group = auth_check.check_get_group(int(group_id))
        edit_grp(group, group_name, request.user)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


