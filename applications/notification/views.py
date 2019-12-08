# -*- coding=utf-8 -*-

import utils.net_helper

from utils.parameter import *
from utils.auth_check import *
from applications.notification.services import *

logger = logging.getLogger(__name__)


@validate(method="GET", usertype=(USER_TYPE_PARENT, ))
def api_notification_inbox(request):
    try:
        keyword = get_parameter(request.GET.get('keyword'), para_intro=u'搜索关键字', allow_null=True, default='')
        last_id = get_parameter(request.GET.get('last_id'), para_intro=u'最后一条通知的ID', allow_null=True, default=0)
        read_classify = get_parameter(request.GET.get('read_classify'), para_intro=u'看未读还是已读消息', allow_null=True, default='')
        type_classify = get_parameter(request.GET.get('type_classify'), para_intro=u'看哪一类消息', allow_null=True, default='')
        # page = get_parameter(request.GET.get('page', 1), para_intro=u'页码', allow_null=True)
        rows = get_parameter(request.GET.get('rows'), para_intro=u'每页数量', allow_null=True, default='10')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notification_info = inbox(request.user, keyword, read_classify, type_classify, last_id, rows)
        return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': notification_info})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="GET", usertype=(USER_TYPE_TEACHER, ))
def api_notification_read_list(request):
    # 该接口不分页
    try:
        notify_id = get_parameter(request.GET.get('notify_id'), para_intro=u'通知ID', valid_check=INTEGER_NONNEGATIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify = check_get_notify(notify_id)
        result = read_list(notify, request.user)
        return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="GET", usertype=(USER_TYPE_TEACHER, ))
def api_notification_outbox(request):
    try:
        keyword = get_parameter(request.GET.get('keyword', ''), para_intro=u'搜索关键字', allow_null=True)
        type_classify = get_parameter(request.GET.get('type_classify'), para_intro=u'看哪一类消息', allow_null=True, default='')
        last_id = get_parameter(request.GET.get('last_id', 0), para_intro=u'最后一条通知ID', allow_null=True)
        # page = get_parameter(request.GET.get('page', 1), para_intro=u'页码', allow_null=True)
        rows = get_parameter(request.GET.get('rows'), para_intro=u'每页数量', valid_check=INTEGER_POSITIVE, allow_null=True, default=10)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        result = outbox(request.user, keyword, type_classify, last_id, rows)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="GET", usertype=(USER_TYPE_TEACHER, USER_TYPE_PARENT))
def api_notification_detail(request):
    try:
        notify_id = get_parameter(request.GET.get('notify_id'), para_intro=u'通知ID', valid_check=INTEGER_NONNEGATIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify = check_get_notify(notify_id)
        result = detail(request.user, notify)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="GET")
def api_notification_receiver_detail(request):
    try:
        notify_id = get_parameter(request.GET.get('notify_id'), para_intro=u'通知ID', valid_check=INTEGER_NONNEGATIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify = check_get_notify(notify_id)
        result = receiver_detail(request.user, notify)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="POST", usertype=(USER_TYPE_TEACHER, ))
def api_notification_outbox_delete(request):
    try:
        notify_ids = get_parameter(request.POST.get('notify_ids', ''), para_intro=u'通知ID列表')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify_list = list()
        for each_str in notify_ids.strip(',').split(','):
            notify_list.append(check_get_notify(each_str))
        outbox_delete(request.user, notify_list)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="POST", usertype=(USER_TYPE_PARENT, ))
def api_notification_inbox_delete(request):
    try:
        notify_ids = get_parameter(request.POST.get('notify_ids', ''), para_intro=u'通知ID列表')
        is_clean_all = get_parameter(request.POST.get('is_clean_all', '0'),
                                            allow_null=True, default='0', para_intro=u'清空所有')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify_list = list()
        for each_str in notify_ids.strip(',').split(','):
            notify_list.append(check_get_notify(each_str))
        inbox_delete(request.user, notify_list, is_clean_all)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="POST", usertype=(USER_TYPE_PARENT, ))
def api_notification_read(request):
    try:
        notify_ids = get_parameter(request.POST.get('notify_ids', ''), para_intro=u'通知ID列表')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify_list = list()
        for each_str in notify_ids.strip(',').split(','):
            notify_list.append(check_get_notify(each_str))
        read(request.user, notify_list)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="POST", usertype=(USER_TYPE_PARENT, ))
def api_notification_unread(request):
    try:
        notify_ids = get_parameter(request.POST.get('notify_ids', ''), para_intro=u'通知ID列表')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify_list = list()
        for each_str in notify_ids.strip(',').split(','):
            notify_list.append(check_get_notify(each_str))
        unread(request.user, notify_list)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="POST", usertype=(USER_TYPE_TEACHER, ))
def api_notification_publish(request):
    try:
        content = get_parameter(request.POST.get('content'), para_intro=u'正文', allow_null=True)
        type = get_parameter(request.POST.get('type'), para_intro=u'通知类型')
        #每一个收通知用户用“accountid”、“usertype”、“schoolid”三元组表示，多个用户用分号分隔，例如：1,1,1;2,2,2
        receivers = get_parameter(request.POST.get('receivers'), para_intro=u'收通知用户', allow_null=True)
        file_ids = get_parameter(request.POST.get('file_ids', ''), para_intro=u'文件ID列表', allow_null=True)
        voice_ids = get_parameter(request.POST.get('voice_ids', ''), para_intro=u'语音ID列表', allow_null=True)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        file_list = list()
        if file_ids:
            for each in file_ids.strip(',').split(','):
                if each:
                    file_list.append(check_get_file(each))

        voice_list = list()
        if voice_ids:
            for each in voice_ids.strip(',').split(','):
                if each:
                    voice_list.append(check_get_voice(each))

        # 目前仅支持对学生发消息（仅家长可读）
        user_role_list = list()
        for each in receivers.strip(';').split(';'):
            account_id = int(each.split(',')[0])
            user_type = int(each.split(',')[1])
            school_id = int(each.split(',')[2])
            user_role = get_type_user(account_id, user_type, school_id)
            if not user_role or not isinstance(user_role, Student):
                raise BusinessException(NOTIFY_AVAI_CAN_SEND_TO_STUDENT)
            user_role_list.append(user_role)

        new_notify_detail = publish(request.user, content, file_list, voice_list, user_role_list, type)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': new_notify_detail})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)


@validate(method="POST", usertype=(USER_TYPE_TEACHER, ))
def api_notification_remind(request):
    try:
        notify_id = get_parameter(request.POST.get('notify_id', ''), para_intro=u'通知ID')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return net_helper.response_parameter_error(ihpe)
    try:
        notify = check_get_notify(notify_id)
        remind(request.user, notify)
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)

