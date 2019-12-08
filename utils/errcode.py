# -*- coding=utf-8 -*-

import json
from django.http import HttpResponse

from django.conf import settings


def code(err_code):
    """
        转换为全局唯一错误码
    """
    return settings.SYSTEM_CODE * 10000 + err_code

# 以下错误码由用户中心定义
# ERR_REQUESTWAY = [40006, u'请求方式错误']
# ERR_MODEL_NAME_ERR = [40025, u"模块名称不存在"]
# ERR_LOGIN_FAIL = [40003, u'用户名或密码错误']
# ERR_USER_NOTLOGGED = [40004, u'用户未登录']
# ERR_USER_AUTH = [40005, u'用户权限不够']
# ERR_ITEM_NOT_EXIST = [40007, u'记录不存在']

FAIL = [-1, u'失败']
SUCCESS = [0, u'完成']
RATE_LIMIT = [10, u'操作太频繁，请稍后再试']
API_DEPRECATED = [11, u'该接口已不再支持，请升级客户端版本']

TIME_ERROR = [3000, u'时间错误']
TIME_ERROR_START_END = [3001, u'开始时间不能晚于结束时间']
TIME_ERROR_FORMAT = [3002, u'时间格式错误']

AUTH_NEED_LOGIN = [40004, u'用户未登录或登录已过期']  # 同用户中心保持一致
AUTH_USER_TYPE_CRUSH = [40000, u'用户角色冲突，请重新登录']

REQUEST_WRONG_METHOD = [code(1000), u'请求方法错误']
REQUEST_INTERNAL = [code(1001), u'无法访问内部接口']
REQUEST_PARAM_ERROR = [code(1002), u'请求参数错误']
AUTH_WRONG_TYPE = [code(1003), u'无权限使用该功能']
AUTH_CONDITION_FAIL = [code(1004), u'由于系统限制, 无法使用该功能']
AUTH_SAME_SCHOOL = [code(1005), u'只能查看本校的相关信息']
AUTH_WRONG_SCHOOL = [code(1006), u'所在学校没有开通该功能']
USER_NOT_EXIST = [code(1007), u'用户不存在']
SCHOOl_NOT_EXIST = [code(1008), u'学校不存在']
CLASS_NOT_EXIST = [code(1009), u'班级不存在']
GROUP_NOT_EXIST = [code(1010), u'群组不存在']
INVITE_NOT_EXIST = [code(1011), u'加入群组的邀请不存在']
TEACHER_NOT_EXIST = [code(1012), u'教师不存在']
PARENT_NOT_EXIST = [code(1013), u'家长不存在']
STUDENT_NOT_EXIST = [code(1014), u'学生不存在']
CLIENT_NOT_EXIST = [code(1015), u'终端类型不存在']
PASSWORD_NOT_EXIST = [code(1016), u'密码不存在']
ROOT_FORBID = [code(1020), u'系统管理员不能访问该系统']
USERTYPE_NOT_EXIST = [code(1021), u'用户角色错误']
AUTH_TEACHER_LIST_CLASS_STU = [code(1022), u'不允许查看非任教班级的学生列表']
INVALID_IMAGE = [code(1040), u'不可识别的图片格式']
FILE_NOT_EXIST = [code(1041), u'文件不存在']
VOICE_NOT_EXIST = [code(1042), u'语音不存在']

APK_NAME_ERROR = [code(2000), u'文件名称和历史版本重复，请确认apk的名字是否正确（huaxiao_a.b.c_release.apk）']
NO_APK_ERROR = [code(2001), u'缺少上传apk包']
UNSUPPORT_TYPE_UPGRADE = [code(2002), u'暂不支持该设备在线升级']
NO_APK_FOUND = [code(2003), u'安装包apk不存在']
IOS_HAS_APK_ERROR = [code(2004), u'IOS更新不应上传apk包']

HUANXIN_GRP_IN_APPLY_FAIL = [code(2101), u'申请群组聊天ID失败']
AGREE_IN_GROUP_FAIL_DUE_TO_NO_CHATID = [code(2102), u'无法加入聊天群组']
GROUP_NO_CHATID = [code(2103), u'群组无可用聊天ID']
HUANXIN_USER_ADDIN_GRP_FAIL = [code(2104), u'用户加入聊天群组失败']
CREATE_GRP_FAIL_DUE_TO_NO_CHATID = [code(2105), u'无法创建群组(创建者无可用聊天ID)']
EDIT_GRP_FAIL = [code(2106), u'修改群组名称失败']
CANNOT_CONTROL_NON_SELFCREATE_GRP = [code(2107), u'不能操作非自己创建的群组']
NO_PRIVILEGE_TO_DETAIL_CLASS = [code(2109), u'没有权限查询该班级详情']
DUP_GROUP_NAME_IN_SCHOOL = [code(2110), u'群组名称重复']
CREATOR_CANNOT_QUIT_GROUP = [code(2111), u'不能退出自己创建的群组']
ONLY_MEMBER_CAN_QUIT_GROUP = [code(2112), u'只有群组成员才可以退出群组']
CREATE_GRP_MAX = [code(2113), u'您已经创建了太多群组']
CHAT_GRP_APPLY_DUP_HANDLE = [code(2114), u'已经处理过该邀请']
GRP_NAME_NOT_SUPPORT_EMOJI = [code(2115), u'群组名称不支持emoji表情']
NOT_STUDENT = [code(2116), u'该用户不是学生']
ONLY_TEACHER_CAN_HANDLE_GRP = [code(2117), u'仅支持教师操作群组']
ONLY_STUDENT_CAN_ADDIN_GRP = [code(2118), u'仅支持让学生加入群组']

ADD_TEACHCLASS_UC_FAIL = [code(2120), u'向学校管理中心增加任教班级失败']
DEL_TEACHCLASS_UC_FAIL = [code(2121), u'向学校管理中心删除任教班级失败']

SMSCODE_NOT_EXIST = [code(2501), u'短信验证码不存在']
SMSCODE_EXPIRED = [code(2502), u'短信验证码已经过期，请重新发送']
SMSCODE_NOT_MATCH = [code(2503), u'短信验证码错误']
SMSCODE_SEND_FAIL = [code(2504), u'发送短信验证码失败']

NOTIFY_AVAI_FOR_PARENT = [code(3001), u'该功能仅学生家长可以使用']
NOTIFY_NOT_EXIST = [code(3002), u'通知不存在']
NOTIFY_AVAI_CAN_SEND_TO_STUDENT = [code(3003), u'当前版本仅支持向学生发通知']
NOTIFY_SUPPORT_TYPE_ERROR1 = [code(3004), u'当前版本仅支持班级通知和作业通知']

WX_GET_ACCESS_TOKEN_FAIL = [code(4001), u'获取微信access_token失败']
WX_FETCH_VOICE_FAIL = [code(4002), u'从微信下载语音素材失败']
WX_UPLOAD_VOICE_FAIL = [code(4003), u'上传微信语音素材到服务器失败']

MOMENT_GET_FAIL = [code(5001), u'获取圈子信息失败']
MOMENT_DELETE_FAIL = [code(5002), u'删除圈子动态失败']
MOMENT_LIKE_FAIL = [code(5003), u'圈子动态点赞失败']
MOMENT_READ_FAIL = [code(5004), u'圈子动态阅读失败']
MOMENT_PUBLISH_NOCONTENT = [code(5005), u'未输入任何内容，无法提交']
MOMENT_NORECORD = [code(5006), u'本页无记录']
MOMENT_WRONG_MOMENTID = [code(5007), u'错误的动态编码']
MOMENT_WRONG_REPLYID = [code(5008), u'错误的评论编码']
MOMENT_WRONG_VOTEID = [code(5009), u'错误的投票项编码']
MOMENT_VOTE_DEAD = [code(5010), u'投票已截止']
MOMENT_VOTE_REPEAT = [code(5011), u'请勿重复投票']
MOMENT_CANNOT_REPLYSELF = [code(5012), u'不允许回复自己的评论']
MOMENT_VOTE_TITLE_NULL = [code(5013), u'投票主题不允许为空']
MOMENT_VOTE_DEADLINE_NULL = [code(5014), u'投票截止时间不允许为空']
MOMENT_EVALUATE_ONLY_AVAI_FOR_TEACHER = [code(5015), u'只有教师能发布评价互动']
MOMENT_DAYOFF_ONLY_AVAI_FOR_PARENT = [code(5016), u'只有家长可以发请假互动']
MOMENT_NOT_EXIST = [code(5017), u'圈子动态不存在']
MOMENT_NO_PRIVELEGE = [code(5018), u'无权限处理此圈子动态']
MOMENT_VOTE_BRANCH_FORMAT_ERR = [code(5019), u'投票选择枝为空或格式错误']
MOMENT_EVALUATE_NON_AIM = [code(5020), u'缺少评价对象']





