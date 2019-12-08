# -*- coding=utf-8 -*-

from datetime import *
from urlparse import urljoin

from django.db import transaction
from django.db.models import F, Q

from utils.errcode import *
from utils.parameter import *
from utils.tools import get_type_user, BusinessException, gen_url_with_fname, url, getpages
from utils.type_helper import datetime2str
from utils.utils_time import get_cycletime_from_date_type, get_time_perform
from applications.common.services import get_current_sys_domain, get_uc_static_file_path, get_classes_by_role, get_classes_by_turple
from applications.contacts.services import get_contact_book, collect_stu
from applications.moment.models import *


def qs_new(user):
    # 获取联系人列表
    contactlist = get_contact_book(user, flat=True, except_me=False)
    values_str = ''
    for each in contactlist:
        values_str = values_str + ',(' + each['account_id'] + ',' + each['user_type_id'] + ',' + each['school_id'] + ')'
    values_str = values_str.strip(',')
    return MomentBase.objects.all().extra(where=['(`account_id`,`user_type`,`user_school_id`) in (%s)' % values_str])


def qs_school(user):
    return MomentBase.objects.filter(user_school=user.school, schoolcircle__is_del=FALSE_INT)


def qs_class(user, class_id):
    return MomentBase.objects.filter(classcircle__clazz__id=int(class_id), classcircle__is_del=FALSE_INT)


def qs_person(user, account_id, user_type, school_id):
    account_id = int(account_id) if account_id else user.id
    user_type = int(user_type) if user_type else user.type
    school_id = int(school_id) if school_id else user.school.id
    return MomentBase.objects.filter(account_id=account_id, user_type=user_type, user_school=school_id)


def get_moments(original_qs, user, last_moment_id, page, size, moment_types, keyword, time_scope):
    result = dict()
    result_list = []

    time_start_and_end = get_cycletime_from_date_type(time_scope)
    dt_start = time_start_and_end['startdate']
    dt_end = time_start_and_end['enddate']

    qs = original_qs.filter(create_time__gte=dt_start, create_time__lte=dt_end).distinct().order_by('-create_time')
    if keyword:
        # 目前搜索关键字支持发圈子人和正文
        qs = qs.filter(Q(content__contains=keyword) | Q(user_name__contains=keyword))
    if last_moment_id:
        qs = qs.filter(id__lt=last_moment_id)

    if moment_types:
        moment_type_list = [int(each) for each in moment_types.strip(',').split(',')]
        qs = qs.filter(moment_type__in=moment_type_list)

    moment_list = list(qs)
    filtered_list = list()
    # 如果不是老师不能看到指定为“仅教师可见”的请假动态
    if user.type != USER_TYPE_TEACHER:
        for i, each in enumerate(moment_list):
            if each.moment_type == MOMENT_TYPE_DAYOFF and \
                MomentDayoff.objects.filter(moment=each).first().is_visible_for_teacher == TRUE_INT:
                filtered_list.append(each)
    # 如果不是相应学生的家长，不能看到指定为“仅相关学生家长可见”的评价动态
    for i, each in enumerate(moment_list):
        if each.moment_type == MOMENT_TYPE_EVALUATE:
            evaluate = MomentEvaluate.objects.filter(moment=each).first()
            if evaluate.type == MOMENT_EVALUATE_CAI and evaluate.is_visible_for_parent_related == TRUE_INT:
                if user.type != USER_TYPE_PARENT:
                    filtered_list.append(each)
                else:
                    evaluate_stu = MomentEvaluateStudent.objects.filter(moment=each, moment_evaluate=evaluate)
                    stu_list = [evalu_stu.student for evalu_stu in evaluate_stu]
                    my_stu_list = [ps.student for ps in ParentStudent.objects.filter(parent__account=user, del_flag=TRUE_INT)]
                    is_to_me = True if len(set(stu_list).intersection(my_stu_list)) > 0 else False
                    if not is_to_me:
                        filtered_list.append(each)

    final_list = [each for each in moment_list if each not in filtered_list]
    cnt = len(final_list)  # 总数量
    num_pages, cur_start, cur_end = getpages(cnt, page, size)
    moments_cur = final_list[cur_start:cur_end]

    for each in moments_cur:
        moment = get_onemoment(each, user, MOMENT_FROM_LIST)
        if moment:
            result_list.append(moment)

    result["list"] = result_list
    result["max_page"] = num_pages
    result["total"] = cnt
    return result


def get_onemoment(momenteach, user, reqfrom):
    """
    获取单条动态信息
    """
    start_time = datetime.now()

    typeuser = get_type_user(momenteach.account.id, momenteach.user_type, momenteach.user_school_id)

    moment = dict()
    moment["moment_id"] = momenteach.id
    moment["username"] = typeuser.full_name if typeuser else u'该用户不存在或已删除'
    moment["account_id"] = momenteach.account.id
    moment["user_type_id"] = momenteach.user_type
    moment["user_type"] = USER_TYPE_MAP[momenteach.user_type]
    moment["moment_type"] = momenteach.moment_type
    moment["school_id"] = momenteach.user_school_id
    moment["avatar"] = get_uc_static_file_path(typeuser.image_url) if typeuser else ''
    moment["sex"] = typeuser.sex if typeuser else ''

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

    # 检查自己是否点赞
    moment["is_like"] = TRUE_STR \
            if MomentLike.objects.filter(
                    moment=momenteach, account=user, user_type=user.type, user_school=user.school) \
                .exists()  \
            else FALSE_STR

    moment["reply_count"] = momenteach.reply_count
    moment["has_voice"] = momenteach.has_voice
    moment["has_image"] = momenteach.has_image
    moment["has_video"] = momenteach.has_video
    moment["has_file"] = momenteach.has_file
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
                 "video_url": url(get_current_sys_domain(), moment_video.video.video_url), "video_type": moment_video.video.video_type,
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
    # 检查自己是否投票
    momentvoteusers = MomentVoteUser.objects.filter(vote_item__vote__moment=momenteach, account=user, user_type=user.type, user_school=user.school, is_del=FALSE_INT)
    if momentvoteusers:
        moment["is_vote"] = TRUE_STR
        momentvotechoice = momentvoteusers.first().vote_item
    else:
        moment["is_vote"] = FALSE_STR
        momentvotechoice = MomentVoteItem()
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
        # vote_items_list = MomentVoteItem.objects.filter(vote=rs_vote, is_del=FALSE_INT)
        vote_items_list = rs_vote.items.filter(is_del=FALSE_INT).order_by('sort')
        for vote_item_each in vote_items_list:
            if momentvotechoice == vote_item_each:
                isvote = TRUE_STR
            else:
                isvote = FALSE_STR
            vote_item = {"vote_item_id": vote_item_each.id, "branch": vote_item_each.branch, "count": vote_item_each.count, "isvote": isvote}
            vote_items.append(vote_item)
        vote["vote_items"] = vote_items
    moment["vote"] = vote

    # 评价类互动
    evaluate = dict()
    moment["evaluate"] = evaluate
    if momenteach.moment_type == MOMENT_TYPE_EVALUATE:
        evaluate_obj = MomentEvaluate.objects.filter(moment=momenteach).first()
        evaluate['type'] = str(evaluate_obj.type)
        evaluate['is_visible_for_parent_related'] = str(evaluate_obj.is_visible_for_parent_related)
        moment_evaluate_stu_qs = MomentEvaluateStudent.objects.filter(moment_evaluate=evaluate_obj, moment=momenteach)
        student_name_list = [each_evaluate_stu.student.full_name for each_evaluate_stu in moment_evaluate_stu_qs]
        evaluate['students'] = ','.join(student_name_list)

    # 请假类互动
    dayoff = dict()
    moment["dayoff"] = dayoff
    if momenteach.moment_type == MOMENT_TYPE_DAYOFF:
        dayoff_obj = MomentDayoff.objects.filter(moment=momenteach).first()
        dayoff['is_visible_for_teacher'] = str(dayoff_obj.is_visible_for_teacher)

    # 获取点赞列表,查询点动态列表时，不显示点赞列表，查询动态详情时，才显示。
    likes = []
    if reqfrom == MOMENT_FROM_DETAIL:
        rs_like = MomentLike.objects.filter(moment=momenteach, is_del=FALSE_INT).order_by('create_time')
        for rs_like_each in rs_like:
            typeuserlike = get_type_user(rs_like_each.account.id, rs_like_each.user_type, rs_like_each.user_school.id)
            like = {
                "account_id": rs_like_each.account.id,
                "user_type_id": rs_like_each.user_type,
                "school_id": rs_like_each.user_school.id,
                "username": typeuserlike.full_name,
            }
            likes.append(like)
    moment["like"] = likes

    # 获取回复列表,如果是查询列表，则显示前3条，如果是查询详情则全部显示。
    moment["reply"] = get_momentreply(momenteach, reqfrom)

    end_time = datetime.now()
    #logger.debug('Function Time  %s' % (str(end_time - start_time)))

    return moment


def get_momentreply(momenteach, reqfrom):
    """
    获取回复列表,如果是查询列表，则显示前3条，如果是查询详情则全部显示。
    """
    replys = []
    rs_reply = MomentReply.objects.filter(moment=momenteach, is_del=FALSE_INT).order_by('create_time')
    if reqfrom == MOMENT_FROM_LIST:
        reply_count = len(rs_reply)
        if len(rs_reply) < MOMENT_MAX_REPLY:
            start_idx = 0
        else:
            start_idx = len(rs_reply) - MOMENT_MAX_REPLY
        rs_reply = rs_reply[start_idx:reply_count]
    for rs_reply_each in rs_reply:
        reply = get_onereply(rs_reply_each)
        replys.append(reply)
    return replys


def get_onereply(rs_reply_each):
    """
    获取单个回复
    """
    ref = dict()
    if rs_reply_each.ref:
        typeuserref = get_type_user(rs_reply_each.ref.account.id, rs_reply_each.ref.user_type, rs_reply_each.ref.user_school.id)
        ref = {
            "ref_id": rs_reply_each.ref.id,
            "account_id": rs_reply_each.ref.account.id,
            "user_type_id": rs_reply_each.ref.user_type,
            "school_id": rs_reply_each.ref.user_school.id,
            "username": typeuserref.full_name,
            "avatar": get_uc_static_file_path(typeuserref.image_url),
            "create_time": datetime2str(rs_reply_each.ref.create_time),
        }
    typeuserreply = get_type_user(rs_reply_each.account.id, rs_reply_each.user_type, rs_reply_each.user_school.id)
    reply = {
        "reply_id": rs_reply_each.id,
        "account_id": rs_reply_each.account.id,
        "user_type_id": rs_reply_each.user_type,
        "school_id": rs_reply_each.user_school.id,
        "username": typeuserreply.full_name,
        "avatar": get_uc_static_file_path(typeuserreply.image_url),
        "content": rs_reply_each.content,
        "create_time": datetime2str(rs_reply_each.create_time),
        "ref": ref,
    }
    return reply


def circle_share(moment, is_to_school, class_ids):
    # 分享到学校圈
    if is_to_school and (str(is_to_school) == TRUE_STR):
        MomentCircleSchool.objects.create(moment=moment)

    # 分享到班级圈
    if class_ids:
        classes_list = class_ids.strip(',').split(',')
        for class_each in classes_list:
            myclass = Class.objects.filter(id=class_each, del_flag=False).first()
            if myclass:
                MomentCircleClass.objects.create(moment=moment, clazz=myclass)


@transaction.atomic
def publish(user, content, moment_type, image_ids, file_ids, voice_ids, video_ids,
                   vote_title, vote_num, vote_deadline, branches, is_to_school, class_ids):
    """
    发布动态
    @deprecated  该接口已过期, 该接口一分为4, 暂时保留以前向兼容
    """
    if not (content or image_ids or file_ids or voice_ids or video_ids or vote_title or vote_num):
        raise BusinessException(MOMENT_PUBLISH_NOCONTENT)

    if moment_type == MOMENT_TYPE_VOTE:
        # 投票主题不允许为空
        if not vote_title:
            raise BusinessException(MOMENT_VOTE_TITLE_NULL)
        # 投票截止时间不允许为空
        if not vote_deadline:
            raise BusinessException(MOMENT_VOTE_DEADLINE_NULL)
        # 检查传入的是时间戳还是时间，如果是时间戳则自动转换为时间
        if vote_deadline.find(':') < 0:
            if len(vote_deadline) == 13:
                vote_deadline = datetime.fromtimestamp(float(vote_deadline) / 1000)
            else:
                vote_deadline = datetime.fromtimestamp(float(vote_deadline))
            print vote_deadline

    moment = MomentBase.objects.create(
                account=user, user_type=user.type, user_school=user.school,
                content=content, moment_type=moment_type, user_name=user.full_name,
                has_voice=TRUE_INT if voice_ids else FALSE_INT, has_image=TRUE_INT if image_ids else FALSE_INT,
                has_video = TRUE_INT if video_ids else FALSE_INT, has_file=TRUE_INT if file_ids else FALSE_INT)

    if voice_ids:
        voice_id_list = voice_ids.strip(',').split(',')
        for voice_each in voice_id_list:
            voiceupload = SysVoice.objects.filter(pk=voice_each, is_del=FALSE_INT).first()
            if voiceupload:
                MomentAttachVoice.objects.create(moment=moment, voice=voiceupload)

    if image_ids:
        image_id_list = image_ids.strip(',').split(',')
        for image_each in image_id_list:
            imageupload = SysImage.objects.filter(pk=image_each, is_del=FALSE_INT).first()
            if imageupload:
                MomentAttachImage.objects.create(moment=moment, image=imageupload)

    if video_ids:
        video_id_list = video_ids.strip(',').split(',')
        for video_each in video_id_list:
            videoupload = SysVideo.objects.filter(pk=video_each, is_del=FALSE_INT).first()
            if videoupload:
                MomentAttachVideo.objects.create(moment=moment, video=videoupload)

    if file_ids:
        file_id_list = file_ids.strip(',').split(',')
        for file_each in file_id_list:
            fileupload = SysFile.objects.filter(pk=file_each, is_del=FALSE_INT).first()
            if fileupload:
                MomentAttachFile.objects.create(moment=moment, file=fileupload)

    if moment_type == MOMENT_TYPE_VOTE:
        new_vote = MomentVote.objects.create(moment=moment, vote_title=vote_title, vote_deadline=vote_deadline)
        for branche_each in json.loads(branches):
            MomentVoteItem.objects.create(vote=new_vote, branch=branche_each['branch'], sort=branche_each['sort'])

    circle_share(moment, is_to_school, class_ids)

    # 发布完成后，将moment信息全部按LIST内的格式返回
    return get_onemoment(moment, user, MOMENT_FROM_LIST)


@transaction.atomic
def publish_basic(user, content, moment_type, image_ids, file_ids, voice_ids, video_ids, is_to_school, class_ids):
    if not (content or image_ids or file_ids or voice_ids or video_ids):
        raise BusinessException(MOMENT_PUBLISH_NOCONTENT)

    moment = MomentBase.objects.create(
                account=user, user_type=user.type, user_school=user.school,
                content=content, moment_type=moment_type, user_name=user.full_name,
                has_voice=TRUE_INT if voice_ids else FALSE_INT, has_image=TRUE_INT if image_ids else FALSE_INT,
                has_video = TRUE_INT if video_ids else FALSE_INT, has_file=TRUE_INT if file_ids else FALSE_INT)

    if voice_ids:
        voice_id_list = voice_ids.strip(',').split(',')
        for voice_each in voice_id_list:
            voiceupload = SysVoice.objects.filter(pk=voice_each, is_del=FALSE_INT).first()
            if voiceupload:
                MomentAttachVoice.objects.create(moment=moment, voice=voiceupload)

    if image_ids:
        image_id_list = image_ids.strip(',').split(',')
        for image_each in image_id_list:
            imageupload = SysImage.objects.filter(pk=image_each, is_del=FALSE_INT).first()
            if imageupload:
                MomentAttachImage.objects.create(moment=moment, image=imageupload)

    if video_ids:
        video_id_list = video_ids.strip(',').split(',')
        for video_each in video_id_list:
            videoupload = SysVideo.objects.filter(pk=video_each, is_del=FALSE_INT).first()
            if videoupload:
                MomentAttachVideo.objects.create(moment=moment, video=videoupload)

    if file_ids:
        file_id_list = file_ids.strip(',').split(',')
        for file_each in file_id_list:
            fileupload = SysFile.objects.filter(pk=file_each, is_del=FALSE_INT).first()
            if fileupload:
                MomentAttachFile.objects.create(moment=moment, file=fileupload)

    circle_share(moment, is_to_school, class_ids)

    # 发布完成后，将moment信息全部按LIST内的格式返回
    return get_onemoment(moment, user, MOMENT_FROM_LIST)


@transaction.atomic
def publish_vote(user, content, vote_title, vote_deadline, branches, is_to_school, class_ids):
    if not (content or vote_title):
        raise BusinessException(MOMENT_PUBLISH_NOCONTENT)
    # 投票主题不允许为空
    if not vote_title:
        raise BusinessException(MOMENT_VOTE_TITLE_NULL)
    # 投票截止时间不允许为空
    if not vote_deadline:
        raise BusinessException(MOMENT_VOTE_DEADLINE_NULL)
    # 检查传入的是时间戳还是时间，如果是时间戳则自动转换为时间
    if vote_deadline.find(':') < 0:
        if len(vote_deadline) == 13:
            vote_deadline = datetime.fromtimestamp(float(vote_deadline) / 1000)
        else:
            vote_deadline = datetime.fromtimestamp(float(vote_deadline))

    moment = MomentBase.objects.create(
                account=user, user_type=user.type, user_school=user.school, user_name=user.full_name,
                content=content, moment_type=MOMENT_TYPE_VOTE,
                has_voice=FALSE_INT, has_image=FALSE_INT, has_video=FALSE_INT, has_file=FALSE_INT)

    new_vote = MomentVote.objects.create(moment=moment, vote_title=vote_title, vote_deadline=vote_deadline)

    try:
        branch_list = json.loads(branches)
    except:
        raise BusinessException(MOMENT_VOTE_BRANCH_FORMAT_ERR)
    for branche_each in branch_list:
        MomentVoteItem.objects.create(vote=new_vote, branch = branche_each['branch'], sort = branche_each['sort'])

    circle_share(moment, is_to_school, class_ids)

    return get_onemoment(moment, user, MOMENT_FROM_LIST)


@transaction.atomic
def publish_evaluate(user, content, image_ids, voice_ids, evaluate_type,
                     user_triples, group_ids, clazz_ids, is_visible_for_parent_related, class_ids):
    if not (content or image_ids or voice_ids):
        raise BusinessException(MOMENT_PUBLISH_NOCONTENT)

    is_contains_image = TRUE_INT if image_ids else FALSE_INT
    is_contains_voice = TRUE_INT if voice_ids else FALSE_INT

    base = MomentBase.objects.create(
                account=user, user_type=USER_TYPE_TEACHER, user_school=user.school,
                content=content, user_name=user.full_name, moment_type=MOMENT_TYPE_EVALUATE,
                has_image=is_contains_image, has_voice=is_contains_voice)

    if voice_ids:
        voice_id_list = voice_ids.split(',')
        for voice_each in voice_id_list:
            voice_upload = SysVoice.objects.filter(pk=int(voice_each)).first()
            if voice_upload:
                MomentAttachVoice.objects.create(moment=base, voice=voice_upload)

    if image_ids:
        image_id_list = image_ids.split(',')
        for image_each in image_id_list:
            image_upload = SysImage.objects.filter(pk=int(image_each)).first()
            if image_upload:
                MomentAttachImage.objects.create(moment=base, image=image_upload)

    circle_share(base, None, class_ids)

    evaluate = MomentEvaluate.objects.create(
                moment=base, type=int(evaluate_type), is_visible_for_parent_related=int(is_visible_for_parent_related))

    evaluate_stus = collect_stu(user_triples, group_ids, clazz_ids)
    if len(evaluate_stus) <= 0:
        raise BusinessException(MOMENT_EVALUATE_NON_AIM)
    for each_stu in evaluate_stus:
        MomentEvaluateStudent.objects.create(moment=base, moment_evaluate=evaluate, student=each_stu)

    return get_onemoment(base, user, MOMENT_FROM_LIST)


@transaction.atomic
def publish_dayoff(user, content, image_ids, voice_ids, is_visible_for_teacher, class_ids):
    if not (content or image_ids or voice_ids):
        raise BusinessException(MOMENT_PUBLISH_NOCONTENT)

    is_contains_image = TRUE_INT if image_ids else FALSE_INT
    is_contains_voice = TRUE_INT if voice_ids else FALSE_INT

    base = MomentBase.objects.create(
                    account=user, user_type=USER_TYPE_PARENT, user_school=user.school,
                    user_name=user.full_name, content=content, moment_type=MOMENT_TYPE_DAYOFF,
                    has_image=is_contains_image, has_voice=is_contains_voice)

    if voice_ids:
        voice_id_list = voice_ids.split(',')
        for voice_each in voice_id_list:
            voice_upload = SysVoice.objects.filter(pk=int(voice_each)).first()
            if voice_upload:
                MomentAttachVoice.objects.create(moment=base, voice=voice_upload)

    if image_ids:
        image_id_list = image_ids.split(',')
        for image_each in image_id_list:
            image_upload = SysImage.objects.filter(pk=int(image_each)).first()
            if image_upload:
                MomentAttachImage.objects.create(moment=base, image=image_upload)

    circle_share(base, None, class_ids)

    MomentDayoff.objects.create(moment=base, is_visible_for_teacher=int(is_visible_for_teacher))

    return get_onemoment(base, user, MOMENT_FROM_LIST)


@transaction.atomic
def moment_delete(user, moment_id):
    """
    删除动态
    """
    moment = MomentBase.objects.filter(pk=moment_id, is_del=FALSE_INT).first()
    if not moment:
        raise BusinessException(MOMENT_NOT_EXIST)
    # 仅可删除自己发的动态
    if not (moment.account == user and moment.user_type == user.type and moment.user_school == user.school):
        raise BusinessException(MOMENT_NO_PRIVELEGE)

    # 删除动态所有的相关信息: 视频,音频,图片,投票,评价,请假等
    MomentAttachVoice.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentAttachImage.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentAttachVideo.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentAttachFile.objects.filter(moment=moment).update(is_del=TRUE_INT)
    momentvote = MomentVote.objects.filter(moment=moment).first()
    if momentvote:
        momentvoteitems = MomentVoteItem.objects.filter(vote=momentvote)
        momentvoteitems.update(is_del=TRUE_INT)
        MomentVoteUser.objects.filter(vote_item__in=momentvoteitems).update(is_del=TRUE_INT)
        momentvote.is_del = TRUE_INT
        momentvote.save()
    MomentEvaluateStudent.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentEvaluate.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentDayoff.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentLike.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentRead.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentReply.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentCircleSchool.objects.filter(moment=moment).update(is_del=TRUE_INT)
    MomentCircleClass.objects.filter(moment=moment).update(is_del=TRUE_INT)

    moment.is_del = TRUE_INT
    moment.save()


@transaction.atomic
def moment_like(user, moment_id):
    """
    圈子动态点赞
    """
    moment = MomentBase.objects.filter(pk=int(moment_id), is_del=FALSE_INT).first()
    if not moment:
        raise BusinessException(MOMENT_NOT_EXIST)

    momentlike, created = MomentLike.objects.update_or_create(
                    moment=moment, account=user, user_type=user.type, user_school=user.school,
                    defaults={'is_del': FALSE_INT})
    if created:
        # +1
        MomentBase.objects.filter(pk=moment_id, is_del=FALSE_INT).update(like_count=F('like_count') + 1)

        # 有人点赞时，消息通知被点赞主题的发布人
        # 如果点赞的人和动态发布人是同一人，则不发送消息
        if moment.account.id == user.id and moment.user_type == user.type and moment.user_school.id == user.school.id:
            pass
        else:
            # 暂时去掉发消息功能
            # send_star_msg(momentlike, user)
            pass


def moment_read(user, moment_id):
    """
    圈子动态阅读
    """
    moment = MomentBase.objects.filter(pk=moment_id, is_del=FALSE_INT).first()
    if not moment:
        raise BusinessException(MOMENT_NOT_EXIST)
    momentread, created = MomentRead.objects.get_or_create(
        moment=moment, account=user, user_type=user.type, user_school=user.school,
        defaults={'is_del': FALSE_INT})
    if created:
        MomentBase.objects.filter(pk=moment_id, is_del=FALSE_INT).update(read_count=F('read_count') + 1)


@transaction.atomic
def moment_reply(user, moment_id, ref_id, content):
    """
    圈子动态评论
    """
    moment = MomentBase.objects.filter(pk=moment_id, is_del=FALSE_INT).first()
    if not moment:
        raise BusinessException(MOMENT_NOT_EXIST)

    premomentreply = None
    if ref_id:
        premomentreply = MomentReply.objects.filter(pk=int(ref_id)).first()
        if not premomentreply:
            raise BusinessException(MOMENT_WRONG_REPLYID)

        # 不允许回复自己的评论
        if premomentreply.account.id == user.id and premomentreply.user_type == user.type and premomentreply.user_school.id == user.school.id:
            raise BusinessException(MOMENT_CANNOT_REPLYSELF)

    momentreply = MomentReply.objects.create(moment=moment, account=user, user_type=user.type,
                        user_school=user.school, ref=premomentreply, content=content, is_del=FALSE_INT)

    MomentBase.objects.filter(pk=moment_id, is_del=FALSE_INT).update(reply_count=F('reply_count') + 1)

    # 发消息（该功能暂时关闭）
    # send_reply_msg(user, content, momentreply, premomentreply)

    return get_onereply(momentreply)


@transaction.atomic
def moment_vote(user, vote_item_id):
    """
    圈子动态投票，一次只能投一票，暂不支持多选。
    """
    momentvoteitem = MomentVoteItem.objects.filter(pk=vote_item_id).first()
    if not momentvoteitem:
        raise BusinessException(MOMENT_WRONG_VOTEID)

    # 检查是否到期
    momentvote = momentvoteitem.vote
    if datetime.now() > momentvote.vote_deadline:
        raise BusinessException(MOMENT_VOTE_DEAD)

    momentvoteuser, created = MomentVoteUser.objects.get_or_create(
                account=user, user_type=user.type, user_school=user.school, vote_item=momentvoteitem, is_del=FALSE_INT)
    if created:
        MomentVoteItem.objects.filter(pk=vote_item_id).update(count=F('count') + 1)
        MomentVote.objects.filter(pk=momentvote.id).update(vote_statistics=F('vote_statistics') + 1)
    else:
        raise BusinessException(MOMENT_VOTE_REPEAT)




