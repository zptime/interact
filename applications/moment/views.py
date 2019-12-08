# -*- coding=utf-8 -*-

import sys

from ratelimit.decorators import ratelimit

from applications.moment import services
from utils import net_helper
from utils.auth_check import validate
from services import *
from services_readonly import *
from utils.net_helper import *
from utils.tools import BusinessException, get_type_current_user

logger = logging.getLogger(__name__)


@validate('GET', authenticate=True)
def get_moment_list(request):
    """
    功能说明: 获取圈子动态列表
    """
    try:
        circle_type = get_parameter(request.GET.get('circle_type'), allow_null=False, default='0', para_intro=u'圈子类型')
        moment_types = get_parameter(request.GET.get('moment_type'), allow_null=True, default='',  para_intro=u'动态类型')

        # new added
        keyword = get_parameter(request.GET.get('keyword'), allow_null=True, default='', para_intro=u'搜索关键字')
        time_scope = get_parameter(request.GET.get('time_scope'), allow_null=True, default='0', para_intro=u'时间范围')

        account_id = get_parameter(request.GET.get('account_id'), allow_null=True, default='', para_intro=u'用户ID')
        user_type = get_parameter(request.GET.get('user_type'), allow_null=True, default='', para_intro=u'用户类型')
        school_id = get_parameter(request.GET.get('school_id'), allow_null=True, default='', para_intro=u'学校ID')
        class_id = get_parameter(request.GET.get('class_id'), allow_null=True, default='', para_intro=u'班级ID')
        last_moment_id = get_parameter(request.GET.get('last_id'), allow_null=True, para_intro=u'最后一个动态ID')
        page = get_parameter(request.GET.get('page'), allow_null=True, default='1', para_intro=u'页码')
        size = get_parameter(request.GET.get('size'), allow_null=True, default='', para_intro=u'每页数量')
        rows = get_parameter(request.GET.get('rows'), allow_null=True, default='', para_intro=u'每页数量')  # 同size，保持旧版本兼容
        size = size or rows
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)

    # if last_moment_id and page:
    #     dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": u"最后一个动态ID与页码不允许同时存在"}
    #     return response400(dict_resp)
    if circle_type == MOMENT_CLASS and not class_id:
        dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": u"查询班级圈时，班级ID必传"}
        return response400(dict_resp)

    function_map = {
        MOMENT_NEW: {'function': qs_new, 'parameter': (request.user, )},
        MOMENT_SCHOOL: {'function': qs_school, 'parameter': (request.user, )},
        MOMENT_CLASS: {'function': qs_class, 'parameter': (request.user, class_id, )},
        MOMENT_MY: {'function': qs_person, 'parameter': (request.user, account_id, user_type, school_id, )},
    }

    try:
        if circle_type not in function_map:
            raise BusinessException(REQUEST_PARAM_ERROR)
        function = function_map[circle_type]['function']
        parameter = function_map[circle_type]['parameter']
        qs = function(*parameter)
        data = get_moments(qs, request.user, last_moment_id, page, size, moment_types, keyword, time_scope)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)

    return response200({"c": SUCCESS[0], "m": SUCCESS[1], "d": data})


# deprecated
@validate('POST', authenticate=True)
@ratelimit(key='user_or_ip', rate='1/sec')
def moment_publish(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    logger.info('==========moment moment_publish start=========')
    try:
        content = get_parameter(request.POST.get('content'), allow_null=True, para_intro=u'动态文字内容', default='')
        moment_type = get_parameter(request.POST.get('moment_type'), allow_null=False, para_intro=u'互动类型')
        image_ids = get_parameter(request.POST.get('image_ids'), allow_null=True, para_intro=u'图片ID列表')
        file_ids = get_parameter(request.POST.get('file_ids'), allow_null=True, para_intro=u'文件ID列表')
        voice_ids = get_parameter(request.POST.get('voice_ids'), allow_null=True, para_intro=u'语音ID列表')
        video_ids = get_parameter(request.POST.get('video_ids'), allow_null=True, para_intro=u'视频ID列表')
        vote_title = get_parameter(request.POST.get('vote_title'), allow_null=True, para_intro=u'投票主题', valid_check=MAX_LENGTH, length=2000)
        vote_num = get_parameter(request.POST.get('vote_num'), allow_null=True, para_intro=u'多选个数')
        vote_deadline = get_parameter(request.POST.get('vote_deadline'), allow_null=True, para_intro=u'投票截止')
        branches = get_parameter(request.POST.get('branches'), allow_null=True, para_intro=u'投票选项')
        is_to_school = get_parameter(request.POST.get('is_publish_to_school'), allow_null=True, para_intro=u'是否发学校圈')
        class_ids = get_parameter(request.POST.get('class_ids'), allow_null=True, para_intro=u'发班级ID列表')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        data = services.publish(
            request.user, content, moment_type, image_ids, file_ids, voice_ids, video_ids,
            vote_title, vote_num, vote_deadline, branches, is_to_school, class_ids)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": str(ipe)}
        return response400(dict_resp)

    dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1], "d": data}
    return response200(dict_resp)


@validate('POST', authenticate=True)
@ratelimit(key='user_or_ip', rate='1/sec')
def moment_publish_basic(request):
    # 发送3个基本类型: 图片、视频、附件互动
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        content = get_parameter(request.POST.get('content'), allow_null=True, para_intro=u'文字内容', default='')
        moment_type = get_parameter(request.POST.get('moment_type'), allow_null=False, para_intro=u'互动类型')
        image_ids = get_parameter(request.POST.get('image_ids'), allow_null=True, para_intro=u'图片ID列表')
        file_ids = get_parameter(request.POST.get('file_ids'), allow_null=True, para_intro=u'文件ID列表')
        voice_ids = get_parameter(request.POST.get('voice_ids'), allow_null=True, para_intro=u'语音ID列表')
        video_ids = get_parameter(request.POST.get('video_ids'), allow_null=True, para_intro=u'视频ID列表')
        is_to_school = get_parameter(request.POST.get('is_publish_to_school'), allow_null=True, para_intro=u'是否发学校圈')
        class_ids = get_parameter(request.POST.get('class_ids'), allow_null=True, para_intro=u'发班级ID列表')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        moment_type = int(moment_type)
        if moment_type != MOMENT_TYPE_IMAGE and moment_type != MOMENT_TYPE_VIDEO and moment_type != MOMENT_TYPE_FILE:
            raise BusinessException(REQUEST_PARAM_ERROR)
        data = services.publish_basic(
            request.user, content, moment_type, image_ids, file_ids, voice_ids, video_ids, is_to_school, class_ids)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": str(ipe)}
        return response400(dict_resp)

    return response200({"c": SUCCESS[0], "m": SUCCESS[1], "d": data})


@validate('POST', authenticate=True)
@ratelimit(key='user_or_ip', rate='1/sec')
def moment_publish_vote(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        content = get_parameter(request.POST.get('content'), allow_null=True, para_intro=u'文字内容', default='')
        vote_title = get_parameter(request.POST.get('vote_title'), allow_null=True, para_intro=u'投票主题', valid_check=MAX_LENGTH, length=2000)
        vote_deadline = get_parameter(request.POST.get('vote_deadline'), allow_null=False, para_intro=u'投票截止时间')
        branches = get_parameter(request.POST.get('branches'), allow_null=True, para_intro=u'投票选项')
        is_to_school = get_parameter(request.POST.get('is_publish_to_school'), allow_null=True, para_intro=u'是否发学校圈')
        class_ids = get_parameter(request.POST.get('class_ids'), allow_null=True, para_intro=u'发班级ID列表')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        data = services.publish_vote(
                    request.user, content, vote_title, vote_deadline, branches, is_to_school, class_ids)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": str(ipe)}
        return response400(dict_resp)

    return response200({"c": SUCCESS[0], "m": SUCCESS[1], "d": data})


@validate('POST', authenticate=True)
@ratelimit(key='user_or_ip', rate='1/sec')
def moment_publish_evaluate(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        content = get_parameter(request.POST.get('content'), allow_null=True, para_intro=u'文字内容', default='')
        image_ids = get_parameter(request.POST.get('image_ids'), allow_null=True, para_intro=u'临时图片ID列表')
        voice_ids = get_parameter(request.POST.get('voice_ids'), allow_null=True, para_intro=u'临时语音ID列表')
        evaluate_type = get_parameter(request.POST.get('evaluate_type'), allow_null=True, para_intro=u'评价类型', default=str(MOMENT_EVALUATE_ZAN))
        evaluate_user_triples = get_parameter(request.POST.get('evaluate_user_triples'), allow_null=False, para_intro=u'评价的用户三元组（分号分隔）')
        evaluate_group_ids = get_parameter(request.POST.get('evaluate_group_ids'), allow_null=True, para_intro=u'评价的群组ID列表（逗号分隔）')
        evaluate_class_ids = get_parameter(request.POST.get('evaluate_class_ids'), allow_null=True, para_intro=u'评价的班级ID列表（逗号分隔）')
        is_visible_for_parent_related = get_parameter(request.POST.get('is_visible_for_parent_related'),
                                            allow_null=True, para_intro=u'仅相关家长可见', default=TRUE_STR)
        class_ids = get_parameter(request.POST.get('class_ids'), allow_null=True, default='', para_intro=u'发布到的班级ID列表')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        # 只有教师能发布评价互动
        if not isinstance(get_type_current_user(request.user), Teacher):
            raise BusinessException(MOMENT_EVALUATE_ONLY_AVAI_FOR_TEACHER)

        data = services.publish_evaluate(
                    request.user, content, image_ids, voice_ids, evaluate_type, evaluate_user_triples,
                    evaluate_group_ids, evaluate_class_ids, is_visible_for_parent_related, class_ids)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": str(ipe)}
        return response400(dict_resp)

    return response200({"c": SUCCESS[0], "m": SUCCESS[1], "d": data})


@validate('POST', authenticate=True)
@ratelimit(key='user_or_ip', rate='1/sec')
def moment_publish_dayoff(request):
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        content = get_parameter(request.POST.get('content'), allow_null=True, para_intro='文字内容', default='')
        image_ids = get_parameter(request.POST.get('image_ids'), allow_null=True, para_intro='临时图片ID列表')
        voice_ids = get_parameter(request.POST.get('voice_ids'), allow_null=True, para_intro='临时语音ID列表')
        is_visible_for_teacher = get_parameter(request.POST.get('is_visible_for_teacher'),
                                            allow_null=True, para_intro='仅教师可见', default=TRUE_STR)
        class_ids = get_parameter(request.POST.get('class_ids'), allow_null=False, para_intro='发布到的班级ID列表')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        # 只有家长可以发请假互动
        if not isinstance(get_type_current_user(request.user), Parent):
            raise BusinessException(MOMENT_DAYOFF_ONLY_AVAI_FOR_PARENT)

        data = services.publish_dayoff(
                    request.user, content, image_ids, voice_ids, is_visible_for_teacher, class_ids)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": str(ipe)}
        return response400(dict_resp)

    return response200({"c": SUCCESS[0], "m": SUCCESS[1], "d": data})


@validate('GET', authenticate=True)
def get_moment_detail(request):
    """
    功能说明: 获取圈子动态详情
    """
    logger.info('==========moment get_moment_detail start=========')
    try:
        moment_id = get_parameter(request.GET.get('moment_id'), allow_null=False, para_intro='动态ID')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)

    try:
        moment = MomentBase.objects.filter(pk=moment_id).first()
        data = services.get_onemoment(moment, request.user, MOMENT_FROM_DETAIL)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)

    dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1], "d": data}
    return response200(dict_resp)


@validate('POST', authenticate=True)
def moment_delete(request):
    """
    功能说明: 删除单个圈子动态
    """
    try:
        moment_id = get_parameter(request.POST.get('moment_id'), allow_null=False, para_intro='动态ID')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)

    try:
        services.moment_delete(request.user, moment_id)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)

    dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1]}
    return response200(dict_resp)


def rate_limit_moment_like_key(group, request):
    moment_id = request.POST.get('moment_id', '')
    return str(request.user.id) + '_' + str(moment_id)


@validate('POST', authenticate=True)
@ratelimit(key=rate_limit_moment_like_key, rate='1/sec')
def moment_like(request):
    """
    功能说明: 圈子动态点赞
    """
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        moment_id = get_parameter(request.POST.get('moment_id'), allow_null=False, para_intro='动态ID')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        data = services.moment_like(request.user, moment_id)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)

    return response200({"c": SUCCESS[0], "m": SUCCESS[1]})


@validate('POST', authenticate=True)
def moment_read(request):
    """
    功能说明: 圈子动态阅读，每个人只能阅读一次，再次阅读同一篇动态，次数并不会增加。
    """
    try:
        moment_id = get_parameter(request.POST.get('moment_id'), allow_null=False, para_intro=u'动态ID')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        services.moment_read(request.user, moment_id)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)

    return response200({"c": SUCCESS[0], "m": SUCCESS[1]})


@validate('POST', authenticate=True)
@ratelimit(key='user_or_ip', rate='1/sec')
def moment_reply(request):
    """
    功能说明: 圈子动态回复
    """
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        moment_id = get_parameter(request.POST.get('moment_id'), allow_null=False, para_intro=u'动态ID')
        ref_id = get_parameter(request.POST.get('ref_id'), allow_null=True, para_intro=u'被回复的评论ID')
        content = get_parameter(request.POST.get('content'), allow_null=False, para_intro=u'评论内容', valid_check=MAX_LENGTH, length=1500)
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        data = services.moment_reply(request.user, moment_id, ref_id, content)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)

    dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1], "d": data}
    return response200(dict_resp)


@validate('POST', authenticate=True)
@ratelimit(key='user_or_ip', rate='1/sec')
def moment_vote(request):
    """
    功能说明: 圈子动态投票
    """
    if getattr(request, 'limited', False):
        return net_helper.response_ratelimit()
    try:
        # moment_id = get_parameter(request.POST.get('moment_id'), allow_null=False, para_intro='动态ID')
        vote_item_id = get_parameter(request.POST.get('vote_item_id'), allow_null=True, para_intro='投票选择支ID')
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)
    try:
        services.moment_vote(request.user, vote_item_id)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)

    dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1]}
    return response200(dict_resp)


@validate('POST', internal=True, authenticate=False)
def api_internal_proxy(request):
    try:
        pkg_name = get_parameter(request.POST.get('pkg_name'), para_intro=u'包名')
        function_name = get_parameter(request.POST.get('function_name'), para_intro=u'功能名')
        parameter = get_parameter(request.POST.get('parameter'), allow_null=True, default='', para_intro=u'参数')
        internal_interfaces = (
            'moment_publish',
            'get_teacher_class_list',
        )
        if function_name not in internal_interfaces:
            raise InvalidHttpParaException(u'不支持访问该方法')
    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    logger.info('receive internal-call ' + function_name)
    logger.info('PARA: ' + parameter)

    try:
        # pkg_name = 'applications.msg_center.services'
        if not pkg_name:
            pkg_name = 'applications.moment.services'
        __import__(pkg_name)
        function_call = getattr(sys.modules[pkg_name], function_name)
        para_dict = json.loads(parameter)
        if para_dict:
            result = function_call(**para_dict)
        else:
            result = function_call()
        dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1], "d": result or ''}
        logger.info('response for internal-call ' + function_name)
        logger.info(dict_resp)
        return response200(dict_resp)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)


# ----------------------------------------- 以下是测试和演示接口 -----------------------------------------

@validate('GET', authenticate=True)
def api_api(request):
    """
    功能说明: 测试
    """
    logger.info('==========moment api_api start=========')
    momentbase = MomentBase.objects.filter(pk=1)
    logger.debug('1')
    print 'momentbase True' if momentbase else 'momentbase False'
    momentbasefirst = MomentBase.objects.filter(pk=100).first()
    print 'momentbasefirst True' if momentbasefirst else 'momentbasefirst False'
    dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1], "d": "测试数据"}
    return response200(dict_resp)


def get_moment_list_only_display(request):
    # 用于光谷一小电子班牌展示圈子
    logger.info('==========moment get_moment_list_only_display start=========')
    try:
        class_id = get_parameter(request.GET.get('class_id'), allow_null=False, para_intro=u'班级ID')
        last_moment_id = get_parameter(request.GET.get('last_id'), allow_null=True, para_intro=u'最后一个动态ID')
        page = get_parameter(request.GET.get('page'), allow_null=True, default='1', para_intro=u'页码')
        size = get_parameter(request.GET.get('size'), allow_null=True, default='10', para_intro=u'每页数量')
        rows = get_parameter(request.GET.get('rows'), allow_null=True, default='10', para_intro=u'每页数量')
        rows = size or rows
    except InvalidHttpParaException as ipe:
        logger.exception(ipe)
        return response_parameter_error(ipe)

    if last_moment_id and page:
        dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": REQUEST_PARAM_ERROR[1], "d": "最后一个动态ID与页码不允许同时存在"}
        return response400(dict_resp)

    try:
        data = get_moment_class_only_display(class_id, last_moment_id, page, rows)
        dict_resp = {"c": SUCCESS[0], "m": SUCCESS[1], "d": data}
        return response200(dict_resp)
    except BusinessException as e:
        dict_resp = {"c": e.code, "m": e.msg}
        return response200(dict_resp)