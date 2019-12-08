# -*- coding=utf-8 -*-

from django.db import transaction
from django.db.models import Q, F

from applications.common.services import *
from applications.message.helper import *
from applications.message.tasks import *
from applications.message.const import MSG_CATEGORY_NOTIFY_RECEIVE, MSG_CATEGORY_NOTIFY_HOMEWORK, MSG_CATEGORY_NOTIFY_CLASS
from applications.notification.models import *
from utils.tools import *
from utils.utils_time import now


def inbox(user, keyword, read_classify, type_classify, last_id, rows):    # last_id是notifybase的id
    # 家长能看到所有发给自己孩子的通知
    parent = get_type_current_user(user)
    if not isinstance(parent, Parent):
        raise BusinessException(NOTIFY_AVAI_FOR_PARENT)

    my_children = ParentStudent.objects.filter(parent=parent, del_flag=FALSE_INT).values_list('student', flat=True)
    qs = NotifyUserStudent.objects.filter(student__in=my_children).order_by('-notify__id')
    if last_id and int(last_id) > 0:
        qs = qs.filter(notify__id__lt=int(last_id))
    if keyword:
        qs = qs.filter(notify__content__contains=keyword)
    if read_classify:
        read_classify_list = [int(each) for each in read_classify.strip(',').split(',')]
        if read_classify_list:
            qs = qs.filter(is_read__in=read_classify_list)
    if type_classify:
        type_classify_list = [int(each) for each in type_classify.strip(',').split(',')]
        if type_classify_list:
            qs = qs.filter(notify__type__in=type_classify_list)

    paged_list, result = paging_by_lastid(list(qs), rows)
    result_list = list()
    for each in paged_list:
        sender_account_id = each.notify.account.id
        sender_user_type = each.notify.user_type
        sender_school_id = each.notify.user_school.id
        sender_role = get_type_user(sender_account_id, sender_user_type, sender_school_id)
        result_list.append({
            'notify_id': str(each.notify.id),
            'sender_account_id': str(sender_account_id),
            'sender_user_type': str(sender_user_type),
            'sender_school_id': str(sender_school_id),
            'sender_username': str(sender_role.full_name),
            'sender_avatar': get_uc_static_file_path(sender_role.image_url),
            'create_time': each.notify.create_time.strftime('%Y-%m-%d %H:%M'),
            'type': str(each.notify.type),
            'type_desc': NOTIFICATION_MAP[each.notify.type],
            'content': each.notify.content,
            'is_read': str(each.is_read),
            'has_file': str(each.notify.has_file),
            'has_voice': str(each.notify.has_voice),
        })
    result['data_list'] = result_list
    return result


def check_get_notify(notify_id):
    if not notify_id:
        raise BusinessException(NOTIFY_NOT_EXIST)
    notify = NotifyBase.objects.filter(id=int(notify_id)).first()
    if not notify:
        raise BusinessException(NOTIFY_NOT_EXIST)
    return notify


def read_list(notify, user):
    def student_dict(stu):
        return {
            'account_id': str(stu.account.id),
            'user_type': str(USER_TYPE_STUDENT),
            'school_id': str(stu.school.id),
            'username': stu.full_name,
            'avatar': get_uc_static_file_path(stu.image_url),
        }
    who_read =  list()
    who_unread = list()
    qs = NotifyUserStudent.objects.filter(notify=notify)
    for each in qs:
        if each.is_read == TRUE_INT:
            who_read.append(student_dict(each.student))
        else:
            who_unread.append(student_dict(each.student))
    return {
        'who_read': who_read,
        'who_unread': who_unread,
    }


def name_brief(name_list):
    receiver_count = len(name_list)
    if receiver_count > 3:
        receiver_brief = u'%s、%s、%s等%s人' % (name_list[0], name_list[1], name_list[2], receiver_count)
    elif 0 < receiver_count <= 3:
        receiver_brief = u'、'.join(name_list)
    else:
        receiver_brief = u''
    return receiver_brief


def outbox(user, keyword, type_classify, last_id, rows):
    qs = NotifyBase.objects.filter(
            account=user, user_type=user.type, user_school=user.school).order_by('-id')
    if last_id and int(last_id) > 0:
        qs = qs.filter(id__lt=int(last_id))
    if keyword:
        qs = qs.filter(content__contains=keyword)
    if type_classify:
        type_classify_list = [int(each) for each in type_classify.strip(',').split(',')]
        if type_classify_list:
            qs = qs.filter(type__in=type_classify_list)

    paged_list, result = paging_by_lastid(list(qs), rows)
    result_list = list()
    for each in paged_list:
        qs_receiver = NotifyUserStudent.objects.filter(notify__id=int(each.id))
        name_list = [one_receiver.student.full_name for one_receiver in qs_receiver]
        receiver_brief = name_brief(name_list)

        result_list.append({
            'notify_id': str(each.id),
            'create_time': each.create_time.strftime('%Y-%m-%d %H:%M'),
            'type': str(each.type),
            'type_desc': NOTIFICATION_MAP[each.type],
            'content': each.content,
            'receiver_brief': receiver_brief,
            'has_file': str(each.has_file),
            'has_voice': str(each.has_voice),
        })
    result['data_list'] = result_list
    return result


def detail(user, notify):
    user_role = get_type_current_user(user)
    is_admin_request = all(
        (notify.account.id == user.id , notify.user_type == user.type, notify.user_school.id == user.school.id))

    receiver_qs = NotifyUserStudent.objects.filter(notify=notify)
    receiver_list = [each_user_stu.student for each_user_stu in receiver_qs]
    # 当阅读详情时，系统自动标记该通知为已读,且阅读数加1
    if user_role in receiver_list:
        notify_stu = NotifyUserStudent.objects.filter(notify=notify, student=user_role).first()
        if notify_stu and notify_stu.is_read == FALSE_INT:
            notify_stu.is_read = TRUE_INT
            notify_stu.save()

    name_list = [stu.full_name for stu in receiver_list]
    receiver_brief = name_brief(name_list)

    file_attach = list()
    if notify.has_file:
        file_qs = NotifyAttachFile.objects.select_related().filter(notify=notify)
        for each_file in file_qs:
            file_attach.append({
                'file_id': each_file.id,
                'file_name': each_file.file.file_name,
                'file_size': each_file.file.file_size,
                'file_type': each_file.file.file_type,
                'file_url': urljoin(get_current_sys_domain(), each_file.file.file_url),
                'file_url_with_fname': gen_url_with_fname(
                        urljoin(get_current_sys_domain(), each_file.file.file_url), each_file.file.file_name)
            })

    voice_attach = list()
    if notify.has_voice:
        voice_qs = NotifyAttachVoice.objects.select_related().filter(notify=notify)
        for each_voice in voice_qs:
            voice_attach.append({
                "voice_id": str(each_voice.voice.id),
                "voice_name": each_voice.voice.voice_name,
                "voice_size": str(each_voice.voice.voice_size),
                "voice_duration": str(each_voice.voice.voice_duration),
                "voice_type": each_voice.voice.voice_type,
                "voice_url": url(get_current_sys_domain(), each_voice.voice.voice_url),
                "voice_converted_url": url(get_current_sys_domain(), each_voice.voice.voice_converted_url),
                "voice_converted_status": str(each_voice.voice.voice_converted_status)
            })
    sender_role = get_type_user(notify.account.id, notify.user_type, notify.user_school.id)
    return {
        'notify_id': str(notify.id),
        'sender_account_id': str(notify.account.id),
        'sender_user_type': str(notify.user_type),
        'sender_school_id': str(notify.user_school.id),
        'sender_username': str(sender_role.full_name),
        'sender_avatar': get_uc_static_file_path(user_role.image_url),
        'receiver_brief': receiver_brief,
        'create_time': notify.create_time.strftime('%Y-%m-%d %H:%M'),
        'type': str(notify.type),
        'type_desc': NOTIFICATION_MAP[notify.type],
        'content': notify.content,
        'read_count': str(NotifyUserStudent.objects.filter(notify=notify, is_read=TRUE_INT).count()),
        'files': file_attach,
        'voices': voice_attach,
    }


def receiver_detail(user, notify):
    username_list = list()
    qs = NotifyUserStudent.objects.filter(notify=notify)
    for each in qs:
        username_list.append(each.student.full_name)
    return {
        'name_list': username_list
    }


def outbox_delete(user, notify_list):
    for each in notify_list:
        if each.account_id != user.id or each.user_type != user.type or each.user_school_id != user.school_id:
            continue
        NotifyUserStudent.objects.filter(notify=each).update(is_del=TRUE_INT)
        each.is_del = TRUE_INT
        each.save()


def inbox_delete(user, notify_list, is_clean_all):
    parent = get_type_current_user(user)
    if not isinstance(parent, Parent):
        raise BusinessException(NOTIFY_AVAI_FOR_PARENT)
    my_children = ParentStudent.objects.filter(parent=parent, del_flag=FALSE_INT).values_list('student', flat=True)
    if is_clean_all == TRUE_STR:
        NotifyUserStudent.objects.filter(student__in=my_children).update(is_del=TRUE_INT)
    else:
        for each in notify_list:
            NotifyUserStudent.objects.filter(notify=each, student__in=my_children).update(is_del=TRUE_INT)


def read(user, notify_list):
    # Notice: 当某家长有两个孩子收到同一个消息，家长read其中一条消息会同时将两条置为“已读”
    parent = get_type_current_user(user)
    if not isinstance(parent, Parent):
        raise BusinessException(NOTIFY_AVAI_FOR_PARENT)
    my_children = ParentStudent.objects.filter(parent=parent, del_flag=FALSE_INT).values_list('student', flat=True)
    for each in notify_list:
        NotifyUserStudent.objects.filter(notify=each, student__in=my_children).update(is_read=TRUE_INT)


def unread(user, notify_list):
    parent = get_type_current_user(user)
    if not isinstance(parent, Parent):
        raise BusinessException(NOTIFY_AVAI_FOR_PARENT)
    my_children = ParentStudent.objects.filter(parent=parent, del_flag=FALSE_INT).values_list('student', flat=True)
    for each in notify_list:
        NotifyUserStudent.objects.filter(notify=each, student__in=my_children).update(is_read=FALSE_INT)


def send_msg_homework(user, stu_list, content, notify):
    sender_role = get_type_current_user(user)
    msg_body = list()
    for each in stu_list:
        for each_parent_rela in ParentStudent.objects.select_related().filter(student=each, del_flag=FALSE_INT):
            msg_body.append({
                'account_id': str(each_parent_rela.parent.account.id),
                'user_type': str(USER_TYPE_PARENT),
                'school_id': str(each_parent_rela.parent.school.id),
                'description': u'%s老师布置了一份作业' % sender_role.full_name,
                'url': urljoin(get_current_sys_domain(),
                            WECHAT_JUMP_NOTIFY.format(NOTIFY_ID=str(notify.id), SCHOOL_ID=str(notify.user_school.id))),
                'child_name': each.full_name,
                'child_class': each.cls.class_name,
                'homework': content,
            })
    logger.info('send msg to msg_center, type: %s, detail: %s' % (MSG_CATEGORY_NOTIFY_HOMEWORK, msg_body))
    send_msg('', MSG_CATEGORY_NOTIFY_HOMEWORK, msg_body, api_version='2')


def send_msg_class(user, stu_list, content, notify):
    # 采用消息中心V2接口发消息
    sender_role = get_type_current_user(user)
    msg_body = list()
    for each in stu_list:
        for each_parent_rela in ParentStudent.objects.select_related().filter(student=each, del_flag=FALSE_INT):
            msg_body.append({
                'account_id': str(each_parent_rela.parent.account.id),
                'user_type': str(USER_TYPE_PARENT),
                'school_id': str(each_parent_rela.parent.school.id),
                'description': u'%s老师发布了一条通知' % sender_role.full_name,
                'url': urljoin(get_current_sys_domain(),
                            WECHAT_JUMP_NOTIFY.format(NOTIFY_ID=str(notify.id), SCHOOL_ID=str(notify.user_school.id))),
                'child_name': each.full_name,
                'child_class': each.cls.class_name,
                'detail': content,
                'sender': u'%s老师' % sender_role.full_name,
                'send_time': now(),
            })
    logger.info('send msg to msg_center, type: %s, detail: %s' % (MSG_CATEGORY_NOTIFY_CLASS, msg_body))
    send_msg('', MSG_CATEGORY_NOTIFY_CLASS, msg_body, api_version='2')


@transaction.atomic()
def publish(user, content, file_list, voice_list, user_role_list, type):
    if int(type) != NOTIFICATION_CLASS and int(type) != NOTIFICATION_HOMEWORK:
        raise BusinessException(NOTIFY_SUPPORT_TYPE_ERROR1)
    name_list = [each_stu.full_name for each_stu in user_role_list]
    new_notify = NotifyBase.objects.create(account=user, user_type=user.type, user_school=user.school,
            intro=name_brief(name_list), content=content, type=int(type),
            has_file=TRUE_INT if file_list else FALSE_INT, has_voice=TRUE_INT if voice_list else FALSE_INT)
    for each_file in file_list:
        NotifyAttachFile.objects.create(notify=new_notify, file=each_file)
    for each_voice in voice_list:
        NotifyAttachVoice.objects.create(notify=new_notify, voice=each_voice)
    for each_stu in user_role_list:
        NotifyUserStudent.objects.create(notify=new_notify, student=each_stu)

    # 发给学生的通知会知会家长
    if settings.USE_MSG:
        if int(type) == NOTIFICATION_HOMEWORK:
            send_msg_homework(user, user_role_list, content, new_notify)
        elif int(type) == NOTIFICATION_CLASS:
            send_msg_class(user, user_role_list, content, new_notify)
        else:
            pass

    return detail(user, new_notify)


def remind(user, notify):
    # 再次提醒未读的学生家长（发送微信模板消息和APP消息），限制频率，发布之后最多发1次
    pass
