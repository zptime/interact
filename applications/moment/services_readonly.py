# -*- coding=utf-8 -*-

from datetime import *

from django.db import transaction

from utils.tools import get_type_user, BusinessException, gen_url_with_fname, getpages
from utils.type_helper import datetime2str
from utils.utils_time import get_time_perform
from applications.common.services import get_current_sys_domain, get_uc_static_file_path, get_classes_by_turple
from applications.moment.models import *
from applications.moment.services import url, get_momentreply


@transaction.atomic
def get_moment_class_only_display(class_id, last_moment_id, page, size):
    """
        查询班级圈
    """
    result = dict()
    result_list = []

    if last_moment_id:
        moments_class = MomentBase.objects.filter(id__lt=last_moment_id, classcircle__clazz__id=class_id, is_del=FALSE_INT, classcircle__is_del=FALSE_INT).order_by('-create_time')
    else:
        moments_class = MomentBase.objects.filter(classcircle__clazz__id=class_id, is_del=FALSE_INT, classcircle__is_del=FALSE_INT).order_by('-create_time')

    cnt = moments_class.count()  # 总数量
    num_pages, cur_start, cur_end = getpages(cnt, page, size)
    moments_cur = moments_class[cur_start:cur_end]

    for momenteach in moments_cur:
        moment = get_onemoment_only_display(momenteach)
        if moment:
            result_list.append(moment)

    result["list"] = result_list
    result["max_page"] = num_pages
    result["total"] = cnt
    return result


def get_onemoment_only_display(momenteach):
    """
        获取单条动态信息(仅用于展示)
    """
    typeuser = get_type_user(momenteach.account.id, momenteach.user_type, momenteach.user_school_id)
    moment = dict()
    moment["moment_id"] = momenteach.id
    moment["username"] = typeuser.full_name
    moment["account_id"] = momenteach.account.id
    moment["user_type_id"] = momenteach.user_type
    moment["user_type"] = USER_TYPE_MAP[momenteach.user_type]
    moment["moment_type"] = momenteach.moment_type
    moment["school_id"] = momenteach.user_school_id
    moment["avatar"] = get_uc_static_file_path(typeuser.image_url)
    moment["sex"] = typeuser.sex

    class_name = ''
    class_list = get_classes_by_turple(momenteach.account.id, momenteach.user_type, momenteach.user_school_id)
    if class_list and len(class_list) > 0:
        class_name = class_list[0]['class_name']
    moment["class"] = class_name

    moment["create_time"] = datetime2str(momenteach.create_time)  # .strftime("%Y-%m-%d %H:%I:%S")
    moment["create_time_perform"] = get_time_perform(datetime2str(momenteach.create_time))  # .strftime("%Y-%m-%d %H:%I:%S")
    moment["content"] = momenteach.content
    moment["read_count"] = momenteach.read_count
    moment["like_count"] = momenteach.like_count

    moment["reply_count"] = momenteach.reply_count
    moment["has_voice"] = momenteach.has_voice
    moment["has_image"] = momenteach.has_image
    moment["has_video"] = momenteach.has_video
    moment["has_file"] = momenteach.has_file
    if momenteach.append_attr:
        moment["append_attr"] = momenteach.append_attr
    else:
        moment["append_attr"] = ''

    # 获取语音列表
    voice_list = []
    moment_voice_list = MomentAttachVoice.objects.filter(moment=momenteach, is_del=FALSE_INT).order_by('create_time')
    for moment_voice in moment_voice_list:
        voice = {"voice_id": moment_voice.id, "voice_name": moment_voice.voice.voice_name,
                 "voice_size": moment_voice.voice.voice_size, "voice_duration": moment_voice.voice.voice_duration,
                 "voice_type": moment_voice.voice.voice_type, "voice_url": url(get_current_sys_domain(), moment_voice.voice.voice_url),
                 "voice_converted_url": url(get_current_sys_domain(), moment_voice.voice.voice_converted_url),
                 "voice_converted_status": str(moment_voice.voice.voice_converted_status)}
        voice_list.append(voice)
    moment["voices"] = voice_list

    # 获取图片列表
    image_list = []
    moment_image_list = MomentAttachImage.objects.filter(moment=momenteach, is_del=FALSE_INT).order_by('create_time')
    for moment_image in moment_image_list:
        # 如果没有缩略图，表明该原图不需要压缩，则缩略图就是原图，同时原图置空；如果有缩略图，则返回缩略图和原图
        if moment_image.image.image_thumb_url:
            image_thumb_url = url(get_current_sys_domain(), moment_image.image.image_thumb_url)
            image_original_url = url(get_current_sys_domain(), moment_image.image.image_original_url)
        else:
            image_thumb_url = url(get_current_sys_domain(), moment_image.image.image_original_url)
            image_original_url = url(get_current_sys_domain(), moment_image.image.image_original_url)
        image_crop_url = url(get_current_sys_domain(), moment_image.image.image_crop_url)
        image = {"image_id": moment_image.id, "image_name": moment_image.image.image_name,
                 "image_size": moment_image.image.image_size, "image_square": moment_image.image.image_square,
                 "image_original_url": image_original_url,
                 "image_thumb_url": image_thumb_url,
                 "image_crop_url": image_crop_url,
                 "image_type": moment_image.image.image_type,
                 "image_width": moment_image.image.image_square.split(',')[0],
                 "image_hight": moment_image.image.image_square.split(',')[1]}
        image_list.append(image)
    moment["images"] = image_list

    # 获取视频列表
    video_list = []
    moment_video_list = MomentAttachVideo.objects.filter(moment=momenteach, is_del=FALSE_INT).order_by('create_time')
    for moment_video in moment_video_list:
        video = {"video_id": moment_video.id, "video_name": moment_video.video.video_name,
                 "video_size": moment_video.video.video_size, "video_duration": moment_video.video.video_duration,
                 "video_url": url(get_current_sys_domain(), moment_video.video.video_url),
                 "video_type": moment_video.video.video_type,
                 "video_converted_url": url(get_current_sys_domain(), moment_video.video.video_converted_url),
                 "video_converted_status": moment_video.video.video_converted_status,
                 "video_cover_url": url(get_current_sys_domain(), moment_video.video.video_snapshot_url),
                 "video_square": moment_video.video.video_square,
                 "video_width": moment_video.video.video_square.split(',')[0],
                 "video_hight": moment_video.video.video_square.split(',')[1]}
        video_list.append(video)
    moment["videos"] = video_list

    # 获取文件列表
    file_list = []
    moment_file_list = MomentAttachFile.objects.filter(moment=momenteach, is_del=FALSE_INT).order_by('create_time')
    for moment_file in moment_file_list:
        myfile = {"file_id": moment_file.id, "file_name": moment_file.file.file_name,
                  "file_size": moment_file.file.file_size,
                  "file_url_with_fname": gen_url_with_fname(url(get_current_sys_domain(), moment_file.file.file_url), moment_file.file.file_name),
                  "file_url": url(get_current_sys_domain(), moment_file.file.file_url),
                  "file_type": moment_file.file.file_type}
        file_list.append(myfile)
    moment["files"] = file_list

    # 获取投票
    vote = dict()
    rs_votes = MomentVote.objects.filter(moment=momenteach, is_del=FALSE_INT).select_related().order_by('create_time')

    if rs_votes:
        rs_vote = rs_votes.first()
        if datetime.now() > rs_vote.vote_deadline:
            moment["is_voteexpire"] = TRUE_STR
        else:
            moment["is_voteexpire"] = FALSE_STR
        vote["vote_title"] = rs_vote.vote_title
        vote["vote_num"] = rs_vote.vote_num
        vote["vote_deadline"] = datetime2str(rs_vote.vote_deadline)
        vote["vote_statistics"] = rs_vote.vote_statistics
        vote_items = []
        vote_items_list = rs_vote.items.filter(is_del=FALSE_INT).order_by('sort')
        for vote_item_each in vote_items_list:
            vote_item = {"vote_item_id": vote_item_each.id, "branch": vote_item_each.branch, "count": vote_item_each.count}
            vote_items.append(vote_item)
        vote["vote_items"] = vote_items
    moment["vote"] = vote

    moment["like"] = []

    replys = get_momentreply(momenteach, MOMENT_FROM_LIST)
    moment["reply"] = replys

    return moment