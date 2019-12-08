# -*- coding=utf-8 -*-

from django.conf import settings
from django.contrib import auth

from utils.auth_check import *
from utils.constant import *
from utils.errcode import *
from utils.net_helper import response_exception, response_parameter_error
from utils.parameter import *
from utils.tools import *
from applications.common import services

logger = logging.getLogger(__name__)


@validate('POST', authenticate=False)
def api_logout(request):
    auth.logout(request)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})


# @validate('GET')
# def api_myclass_simple_list(request):
#     try:
#         role = tools.get_type_current_user(request.user)
#         if not role:
#             raise BusinessException(USER_NOT_EXIST)
#         if isinstance(role, Teacher):
#             result = services.get_class_by_teacher(role.id)
#         else:
#             result = services.get_classes_by_account(request.user, verbose=False)
#     except Exception as e:
#         logger.exception(e)
#         return response_exception(e)
#     return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET')
def api_user_class_list(request):
    try:
        result = services.get_classes_by_account(request.user)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST')
def api_teachclass_add(request):
    try:
        class_ids = get_parameter(request.POST.get('class_ids'), para_intro=u'班级ID')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    class_id_list = [int(each) for each in class_ids.split(',')]
    classes = list(Class.objects.filter(del_flag=FALSE_INT, id__in=class_id_list))
    teacher = tools.get_type_current_user(request.user)
    if not teacher or not services.is_teacher(teacher):
        return net_helper.response400({'c': USER_NOT_EXIST[0], 'm': USER_NOT_EXIST[1]})
    try:
        services.add_teach_relation(teacher, classes)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})


@validate('POST')
def api_teachclass_delete(request):
    try:
        class_ids = get_parameter(request.POST.get('class_ids'), para_intro=u'班级ID')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    class_id_list = [int(each) for each in class_ids.split(',')]
    classes = list(Class.objects.filter(del_flag=FALSE_INT, id__in=class_id_list))
    teacher = tools.get_type_current_user(request.user)
    if not teacher or not services.is_teacher(teacher):
        return net_helper.response400({'c': USER_NOT_EXIST[0], 'm': USER_NOT_EXIST[1]})
    try:
        services.delete_teach_relation(teacher, classes)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})


@validate('GET', usertype=(USER_TYPE_TEACHER,))
def api_school_class_list(request):
    school = request.user.school
    result = services.get_classes_in_school(school)
    log_response(request, result)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', usertype=(USER_TYPE_TEACHER,))
def api_class_student_list(request):
    log_request(request)
    try:
        class_id = get_parameter(request.POST.get('class_id'), para_intro=u'班级ID', valid_check=INTEGER_NONNEGATIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    # 权限校验： 判断老师是否任教这个班
    query_class = Class.objects.filter(del_flag=FALSE_INT, id=int(class_id)).first()
    if not query_class:
        return net_helper.response400({'c': CLASS_NOT_EXIST[0], 'm': CLASS_NOT_EXIST[1]})
    teacher = tools.get_type_user(request.user.id, USER_TYPE_TEACHER, request.user.school.id)
    if not teacher:
        return net_helper.response400({'c': USER_NOT_EXIST[0], 'm': USER_NOT_EXIST[1]})

    try:
        result = services.get_class_member(query_class, exclude_teacher=True)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


def api_user_verify(request):
    """
        验证请求所包含用户是否已经登录
    """
    if request.user.is_authenticated():
        return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1]})
    else:
        return net_helper.response403({'c': FAIL[0], 'm': FAIL[1]})


@validate('POST')
def api_stu_info(request):
    try:
        account_id = get_parameter(request.POST.get('account_id'), para_intro=u'用户账号', allow_null=True)
        user_type_id = get_parameter(request.POST.get('user_type_id'), para_intro=u'用户类型ID', valid_check=INTEGER_POSITIVE, allow_null=True)
        school_id = get_parameter(request.POST.get('school_id'), para_intro=u'用户所在学校ID', valid_check=INTEGER_POSITIVE, allow_null=True)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        result = services.get_student_simple_info(request, account_id, user_type_id, school_id)
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST')
def api_user_info(request):
    try:
        account_id = get_parameter(request.POST.get('account_id'), para_intro=u'用户账号', allow_null=True)
        user_type_id = get_parameter(request.POST.get('user_type_id'), para_intro=u'用户类型ID', allow_null=True, valid_check=INTEGER_POSITIVE)
        school_id = get_parameter(request.POST.get('school_id'), para_intro=u'用户所在学校ID', allow_null=True, valid_check=INTEGER_POSITIVE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        # 查询自身信息(当前角色)
        if not account_id or account_id == '':
            user_info = services.get_my_info(request.user)
        else:
            # 查询他人信息
            if not user_type_id or not school_id:
                return net_helper.response400({'c': REQUEST_PARAM_ERROR[0], 'm': REQUEST_PARAM_ERROR[1]})
            if not is_in_same_school(request.user, school_id):
                return net_helper.response403({'c': AUTH_SAME_SCHOOL[0], 'm': AUTH_SAME_SCHOOL[1]})
            user_info = services.get_user_info(account_id, user_type_id, school_id)
    except Exception as e:
        logger.exception(e)
        return net_helper.response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': user_info})


@validate('POST')
def api_upload_image(request):
    try:
        is_secure = get_parameter(request.POST.get('is_secure'), allow_null=True, default='0', para_intro=u'是否需要认证访问', valid_check=INTEGER_NONNEGATIVE)
        image_file = get_parameter(request.FILES.get('image'), para_intro=u'图片文件', valid_check=IMAGE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        result = services.upload_image(image_file, request.user, '0')
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST')
def api_upload_voice(request):
    try:
        is_secure = get_parameter(request.POST.get('is_secure'), allow_null=True, default='0', para_intro=u'是否需要认证访问', valid_check=INTEGER_NONNEGATIVE)
        duration = get_parameter(request.POST.get('duration'), allow_null=True, default='0', para_intro=u'语音持续时长', valid_check=INTEGER_NONNEGATIVE)
        voice_file = get_parameter(request.FILES.get('voice'), para_intro=u'语音文件', valid_check=VOICE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    if not voice_file:
        return net_helper.response400({'c': REQUEST_PARAM_ERROR[0], 'm': REQUEST_PARAM_ERROR[1]})
    result = services.upload_voice(voice_file, duration, request.user, '0')
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST')
def api_wx_voice_fetch(request):
    try:
        media_id = get_parameter(request.POST.get('media_id'), allow_null=False, para_intro=u'微信语音ID')
        duration = get_parameter(request.POST.get('duration'), allow_null=True, default='0', para_intro=u'持续时长')
        access_token = get_parameter(request.POST.get('access_token'), allow_null=True, default='', para_intro=u'access_token')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    try:
        result = services.wx_voice_fetch(request, media_id, duration, access_token)
    except BusinessException as be:
        return response_exception(be)
    return HttpResponse(result, content_type='application/json')


@validate('POST')
def api_upload_video(request):
    try:
        is_secure = get_parameter(request.POST.get('is_secure'), allow_null=True, default='0', para_intro=u'是否需要认证访问', valid_check=INTEGER_NONNEGATIVE)
        video_duration = get_parameter(request.POST.get('duration'), allow_null=True, default='0', para_intro=u'视频持续时长', valid_check=INTEGER_NONNEGATIVE)
        video_file = get_parameter(request.FILES.get('video'), para_intro=u'视频文件', valid_check=VIDEO)
        video_width = get_parameter(request.POST.get('width'), para_intro=u'视频宽度', allow_null=True, default='0', valid_check=INTEGER_NONNEGATIVE)
        video_height = get_parameter(request.POST.get('height'), para_intro=u'视频高度', allow_null=True, default='0', valid_check=INTEGER_NONNEGATIVE)
        video_cover_image = get_parameter(request.FILES.get('snapshot'), para_intro=u'视频封面图片', valid_check=IMAGE, allow_null=True)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    result = services.upload_video(video_file, video_duration, video_width, video_height, video_cover_image, request.user, '0')
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST')
def api_upload_file(request):
    try:
        is_secure = get_parameter(request.POST.get('is_secure'), allow_null=True, default='0', para_intro=u'是否需要认证访问', valid_check=INTEGER_NONNEGATIVE)
        file_name = get_parameter(request.POST.get('file_name'), allow_null=True, default='', para_intro=u'文件名')
        file = get_parameter(request.FILES.get('file'), para_intro=u'附件文件', valid_check=FILE)
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)
    result = services.upload_file(file, request.user, '0', file_name=file_name)
    return net_helper.response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})

