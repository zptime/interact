# -*- coding=utf-8 -*-

from utils.tools import get_type_user, url
from applications.common.services import get_current_sys_domain, get_uc_static_file_path
from applications.message.const import *
from applications.message.tasks import send_msg
from applications.moment.models import *


def send_star_msg(star, user):
    moment = star.moment
    receiver = '%d,%d,%d' % (moment.account.id, moment.user_type, moment.user_school.id)

    typeuserlike = get_type_user(user.id, user.type, user.school.id)

    head = {
        "account_id": user.id,  # 账号
        "user_type_id": user.type,  # 用户类型
        "school_id": user.school.id,  # 学校
        "username": typeuserlike.full_name,  # 姓名
        "avatar": get_uc_static_file_path(typeuserlike.image_url),  # 头像
        "content": "赞了我",
        "create_time": star.create_time.strftime("%Y-%m-%d %H:%M:%S"),  # 点赞时间
    }

    typeusermoment = get_type_user(moment.account.id, moment.user_type, moment.user_school.id)

    voice_url = ""
    image_url = ""
    file_url = ""
    video_url = ""
    video_cover_url = ""
    description = ""
    content = ""
    deadline = ""

    momentvoices = MomentAttachVoice.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
    if momentvoices:
        momentvoice = momentvoices.first()
        voice_url = url(get_current_sys_domain(), momentvoice.voice.voice_url)

    if moment.moment_type == MOMENT_TYPE_IMAGE:
        momentattachs = MomentAttachImage.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentattach = momentattachs.first()
        if momentattachs:
            # 如果没有缩略图，表明该原图不需要压缩，则缩略图就是原图，同时原图置空；如果有缩略图，则返回缩略图和原图
            if momentattach.image.image_thumb_url:
                image_url = url(get_current_sys_domain(), momentattach.image.image_thumb_url)
            else:
                image_url = url(get_current_sys_domain(), momentattach.image.image_original_url)
            # image_url = get_moment_file_url(get_current_sys_domain(), momentattach.image.image_thumb_url)
            description = "上传了%d张图片" % momentattachs.count()
        else:
            image_url = ''
            description = "发布了文字动态"
        content = moment.content

    if moment.moment_type == MOMENT_TYPE_VIDEO:
        momentattachs = MomentAttachVideo.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentattach = momentattachs.first()
        if momentattachs:
            video_url = url(get_current_sys_domain(), momentattach.video.video_converted_url)
            video_cover_url = url(get_current_sys_domain(), momentattach.video.video_snapshot_url)
            description = "上传了视频"
        else:
            video_url = ''
            video_cover_url = ''
            description = "发布了视频动态"
        content = moment.content

    if moment.moment_type == MOMENT_TYPE_FILE:
        momentattachs = MomentAttachFile.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentattach = momentattachs.first()
        if momentattachs:
            file_url = url(get_current_sys_domain(), momentattach.file.file_url)
            description = "上传了%d个文件" % momentattachs.count()
        else:
            file_url = ''
            description = "发布了附件动态"
        content = moment.content

    if moment.moment_type == MOMENT_TYPE_VOTE:
        momentvotes = MomentVote.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentvote = momentvotes.first()
        description = "发布了投票"
        content = momentvote.vote_title
        deadline = "截止%s" % momentvote.vote_deadline.strftime("%Y-%m-%d %H:%M:%S")

    topic = {
        "moment_id": moment.id,  # 圈子ID
        "account_id": moment.account.id,  # 圈子发布者账号
        "user_type_id": moment.user_type,  # 圈子发布者用户类型
        "school_id": moment.user_school.id,  # 圈子发布者学校
        "username": typeusermoment.full_name,  # 圈子发布者姓名
        "avatar": get_uc_static_file_path(typeusermoment.image_url),  # 圈子发布者头像
        "moment_type": moment.moment_type,  # 0、照片，1、视频，2、附件，3、投票
        "voice_url": voice_url,  # 第一个语音地址
        "image_url": image_url,  # 第一张缩略图地址
        "file_url": file_url,  # 第一个文件地址
        "video_url": video_url,  # 视频地址
        "video_cover_url": video_cover_url,  # 视频封面地址
        "description": description,  # 描述
        "content": content,  # 正文，如果是投票则为投票title
        "deadline": deadline,  # 投票截止时间
        "reply": "",  # 回复内容，点赞时此字段为空，由于移动端要求返回去回复时一致，所以才加此字段
        "ref": dict(),  # 回复的评论，点赞时此字段为空，由于移动端要求返回去回复时一致，所以才加此字段
    }
    content = {
        "head": head,
        "topic": topic,
        "description": "%s赞了我" % typeuserlike.full_name,  # 消息列表中使用的描述信息
    }
    send_msg(receiver, MSG_CATEGORY_MOMENT_LIKE, content)


def send_reply_msg(user, content, momentreply, premomentreply):
    ref_id = premomentreply.id if premomentreply else None
    moment = momentreply.moment
    # 有人回复时，消息通知被回复主题的发布人
    # 有人回复我的回复时，消息通知被回复人及被回复的主题发布人。
    # 如果用户回复自己评论，则只发送一次
    if ref_id:
        if moment.account.id != premomentreply.account.id or moment.user_type != premomentreply.user_type or moment.user_school.id != premomentreply.user_school.id:
            # 当评论动态的回复时，如果动态是自己发送的，只对前一回复的用户进行消息提醒 ，不对自己进行消息提醒
            if moment.account.id == user.id and moment.user_type == user.type and moment.user_school.id == user.school.id:
                receiver = '%d,%d,%d' % (premomentreply.account.id, premomentreply.user_type, premomentreply.user_school.id)
            else:
                receiver = '%d,%d,%d;%d,%d,%d' % (
                moment.account.id, moment.user_type, moment.user_school.id, premomentreply.account.id, premomentreply.user_type, premomentreply.user_school.id)
        else:
            receiver = '%d,%d,%d' % (moment.account.id, moment.user_type, moment.user_school.id)
        msg_type = MSG_CATEGORY_MOMENT_REPLY_COMMENT
        typeuserref = get_type_user(premomentreply.account.id, premomentreply.user_type, premomentreply.user_school.id)
        ref = {
            "account_id": premomentreply.account.id,
            "user_type_id": premomentreply.user_type,
            "school_id": premomentreply.user_school.id,
            "username": typeuserref.full_name,
            "avatar": get_uc_static_file_path(typeuserref.image_url),
        }
    else:
        # 当直接评论动态，且动态是自己发送的时候，不对自己进行消息提醒
        if moment.account.id == user.id and moment.user_type == user.type and moment.user_school.id == user.school.id:
            return

        receiver = '%d,%d,%d' % (moment.account.id, moment.user_type, moment.user_school.id)
        msg_type = MSG_CATEGORY_MOMENT_REPLY_TOPIC
        ref = dict()

    typeuserreply = get_type_user(user.id, user.type, user.school.id)

    msgdescription = content + ''
    head = {
        "account_id": user.id,  # 账号
        "user_type_id": user.type,  # 用户类型
        "school_id": user.school.id,  # 学校
        "username": typeuserreply.full_name,  # 姓名
        "avatar": get_uc_static_file_path(typeuserreply.image_url),  # 头像
        "content": content,
        "create_time": momentreply.create_time.strftime("%Y-%m-%d %H:%M:%S"),  # 回复时间
    }

    typeusermoment = get_type_user(moment.account.id, moment.user_type, moment.user_school.id)

    voice_url = image_url = file_url = video_url = video_cover_url = description = content = deadline = ""

    momentvoices = MomentAttachVoice.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
    if momentvoices:
        momentvoice = momentvoices.first()
        voice_url = url(get_current_sys_domain(), momentvoice.voice.voice_url)

    if moment.moment_type == MOMENT_TYPE_IMAGE:
        momentattachs = MomentAttachImage.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentattach = momentattachs.first()
        if momentattachs:
            # 如果没有缩略图，表明该原图不需要压缩，则缩略图就是原图，同时原图置空；如果有缩略图，则返回缩略图和原图
            if momentattach.image.image_thumb_url:
                image_url = url(get_current_sys_domain(), momentattach.image.image_thumb_url)
            else:
                image_url = url(get_current_sys_domain(), momentattach.image.image_original_url)
            # image_url = get_moment_file_url(get_current_sys_domain(), momentattach.image.image_thumb_url)
            description = "上传了%d张图片" % momentattachs.count()
        else:
            image_url = ''
            description = "发布了文字动态"
        content = moment.content

    if moment.moment_type == MOMENT_TYPE_VIDEO:
        momentattachs = MomentAttachVideo.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentattach = momentattachs.first()
        if momentattachs:
            video_url = url(get_current_sys_domain(), momentattach.video.video_converted_url)
            video_cover_url = url(get_current_sys_domain(), momentattach.video.video_snapshot_url)
            description = "上传了视频"
        else:
            video_url = ''
            video_cover_url = ''
            description = "发布了视频动态"
        content = moment.content

    if moment.moment_type == MOMENT_TYPE_FILE:
        momentattachs = MomentAttachFile.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentattach = momentattachs.first()
        if momentattachs:
            file_url = url(get_current_sys_domain(), momentattach.file.file_url)
            description = "上传了%d个文件" % momentattachs.count()
        else:
            file_url = ''
            description = "发布了附件动态"
        content = moment.content

    if moment.moment_type == MOMENT_TYPE_VOTE:
        momentvotes = MomentVote.objects.filter(moment=moment, is_del=FALSE_INT).order_by('create_time')
        momentvote = momentvotes.first()
        description = "发布了投票"
        content = momentvote.vote_title
        deadline = "截止%s" % momentvote.vote_deadline.strftime("%Y-%m-%d %H:%M:%S")

    topic = {
        "moment_id": moment.id,  # 圈子ID
        "account_id": moment.account.id,  # 圈子发布者账号
        "user_type_id": moment.user_type,  # 圈子发布者用户类型
        "school_id": moment.user_school.id,  # 圈子发布者学校
        "username": typeusermoment.full_name,  # 圈子发布者姓名
        "avatar": get_uc_static_file_path(typeusermoment.image_url),  # 圈子发布者头像
        "moment_type": moment.moment_type,  # 0、照片，1、视频，2、附件，3、投票
        "voice_url": voice_url,  # 第一个语音地址
        "image_url": image_url,  # 第一张缩略图地址
        "file_url": file_url,  # 第一个文件地址
        "video_url": video_url,  # 视频地址
        "video_cover_url": video_cover_url,  # 视频封面地址
        "description": description,  # 描述
        "content": content,  # 正文，如果是投票则为投票title
        "deadline": deadline,  # 投票截止时间
        "ref": ref,
    }

    if ref_id:
        topic['reply'] = premomentreply.content
    else:
        topic['reply'] = ""

    content = {
        "head": head,
        "topic": topic,
        "description": "%s:%s" % (typeuserreply.full_name, msgdescription),  # 消息列表中使用的描述信息
    }

    status = send_msg(receiver, msg_type, content)


