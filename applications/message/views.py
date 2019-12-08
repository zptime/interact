# coding=utf-8

import json
import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from applications.message import helper
from applications.message.const import ERR_MSG_CONNECT_MSG_CENTER_FAIL, ERR_CODE_CONNECT_MSG_CENTER_FAIL
from applications.message.helper import _remote_call

logger = logging.getLogger(__name__)


@login_required
@require_POST
def api_msg_overview(request):
    """
        获取个人消息概览
    """
    payload = {
        'function_name': 'overview',
        'parameter': json.dumps({
            'user_id': str(request.user.id),
        }, ensure_ascii=False)
    }
    try:
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    return remote_response


@login_required
@require_POST
def api_msg_detail(request):
    payload = {
        'function_name': 'get_msg_detail',
        'parameter': json.dumps({
            'msg_id': request.POST.get('msg_id', ''),
            'user_id': str(request.user.id),
        }, ensure_ascii=False)
    }
    try:
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    return remote_response


@login_required
@require_POST
def api_msg_list(request):
    """
        获取指定channel的所有消息（分页）
        channel_code last_msg_id page_size user_id
    """
    payload = {
        'function_name': 'get_msg_list',
        'parameter': json.dumps({
            'user_id': str(request.user.id),
            'last_msg_id': request.POST.get('last_msg_id', '0'),
            'page_size': request.POST.get('page_size', '10'),
            'channel_code': request.POST.get('channel', ''),
        }, ensure_ascii=False)
    }
    try:
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    return remote_response


@login_required
@require_POST
def api_msg_delete(request):
    payload = {
        'function_name': 'delete_msg',
        'parameter': json.dumps({
            'msg_id': request.POST.get('msg_id', ''),
            'user_id': str(request.user.id),
        }, ensure_ascii=False)
    }
    try:
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    return remote_response


@login_required
@require_POST
def api_msg_deleteall(request):
    payload = {
        'function_name': 'delete_msg_all',
        'parameter': json.dumps({
            'channel_code': request.POST.get('channel', ''),
            'user_id': str(request.user.id),
        }, ensure_ascii=False)
    }
    try:
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    return remote_response


@login_required
@require_POST
def api_msg_read(request):
    payload = {
        'function_name': 'set_read_msg',
        'parameter': json.dumps({
            'channel_code': request.POST.get('channel', ''),
            'user_id': str(request.user.id),
        }, ensure_ascii=False)
    }
    try:
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    return remote_response


@login_required
@require_POST
def api_msg_pull(request):
    payload = {
        'function_name': 'get_channel_pull',
        'parameter': json.dumps({
            'user_id': str(request.user.id),
            'channel_code': request.POST.get('channel', ''),
            'timestamp': request.POST.get('timestamp', ''),
        }, ensure_ascii=False)
    }
    try:
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    return remote_response

