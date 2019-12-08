# -*- coding: utf-8 -*-

# '是'与'否'定义
from collections import namedtuple

TRUE_STR = '1'
FALSE_STR = '0'
TRUE_INT = 1
FALSE_INT = 0

# 用户类型
USER_TYPE_NONE = 0     # 未定义
USER_TYPE_STUDENT = 1  # 学生
USER_TYPE_TEACHER = 2  # 老师
USER_TYPE_PARENT = 4   # 家长
USER_TYPE_STUDENT_PARENT = 5   # 学生及家长
USER_TYPE_TEACHER_PARENT = 6   # 老师及家长
USER_TYPE_ALL = 7   # 老师/家长/学生
USER_TYPE_MAP = {USER_TYPE_NONE:u'未知', USER_TYPE_STUDENT:u'学生', USER_TYPE_TEACHER:u'老师', USER_TYPE_PARENT:u'家长'}

# 时段类型
DATE_TYPE_STUDYYEAR = 0  # 全部/学年  两个为同一参数，因为最长只能查一个学年的
DATE_TYPE_TODAY = 1  # 当天
DATE_TYPE_THISWEEK = 2  # 本周
DATE_TYPE_THISMONTH = 3  # 本月
DATE_TYPE_LASTMONTH = 4  # 上月
DATE_TYPE_THISSEASON = 5  # 本季度
DATE_TYPE_THISTERM = 6  # 本学期
DATE_TYPE_THISSCHOOLYEAR = 7  # 本学年

DATE_TYPE_DAY = 1  # 当天
DATE_TYPE_WEEK = 2  # 本周
DATE_TYPE_MONTH = 3  # 本月

TimeType = namedtuple('TimeType', ['DATE_STD', 'DATE_TRIM', 'DAY_STD', 'DAY_TRIM'])
TIME = TimeType(
    '%Y-%m-%d %H:%M:%S',
    '%y-%m-%d %H:%M:%S',
    '%Y-%m-%d',
    '%y-%m-%d',
)

# 移动设备代号
MOBILE_TYPE_APPLE_PHONE = 1
MOBILE_TYPE_APPLE_PAD = 2
MOBILE_TYPE_ANDROID_PHONE = 4
MOBILE_TYPE_ANDROID_PAD = 8
MOBILE_TYPE_ALL = 15

# 互动内容类型
MOMENT_TYPE_IMAGE = 0  # 照片互动
MOMENT_TYPE_VIDEO = 1  # 视频互动
MOMENT_TYPE_FILE = 2   # 附件互动
MOMENT_TYPE_VOTE = 3   # 投票互动
MOMENT_TYPE_MEDAL = 4   # 奖章互动
MOMENT_TYPE_DAYOFF = 5   # 请假互动
MOMENT_TYPE_EVALUATE = 6   # 评价互动
MOMENT_TYPE_NONE = 99   # 未定义

# 通知类型
NOTIFY_TYPE_NONE = USER_TYPE_NONE  # 未定义类型  (暂不支持)
NOTIFY_TYPE_TEACHER = USER_TYPE_TEACHER  # 老师通知  (暂不支持)
NOTIFY_TYPE_STUDENT = USER_TYPE_STUDENT  # 学生通知  (暂不支持)
NOTIFY_TYPE_PARENT = USER_TYPE_PARENT   # 家长通知
NOTIFY_TYPE_STU_PARENT = USER_TYPE_STUDENT_PARENT   # 学生和家长通知  (暂不支持)
NOTIFY_TYPE_ALL = USER_TYPE_ALL   # 所有人通知  (暂不支持)
NOTIFY_TYPE_MAP = {NOTIFY_TYPE_NONE: u'未定义类型', USER_TYPE_STUDENT: u'学生通知', NOTIFY_TYPE_PARENT: u'家长通知', NOTIFY_TYPE_STU_PARENT: u'学生和家长通知'}

NOTIFICATION_SCOPE_1 = 1  # 通知学生，仅家长可读
NOTIFICATION_SCOPE_2 = 2  # 通知学生，学生和家长可读
NOTIFICATION_SCOPE_3 = 3  # 通知家长，家长可读

NOTIFICATION_CLASS = 1
NOTIFICATION_HOMEWORK = 2
NOTIFICATION_MAP = {NOTIFICATION_CLASS: u'班级通知', NOTIFICATION_HOMEWORK: u'作业通知'}

# 支持语音类型
VOICE_TYPE_MP3 = 'MP3'
VOICE_TYPE_AMR = 'AMR'
VOICE_TYPE_WAV = 'WAV'

# 数据库字段配置
DB_URL_LEN_LIMIT = 500  # 数据表中URL最大长度


CHAT_BOOK_TEACHER_GRP = 'teacher'
CHAT_BOOK_STUDENT_GRP = 'student'
CHAT_BOOK_FAMILY_GRP = 'family'
CHAT_BOOK_CLUSTER_CLASS_GRP = 'clazz'
CHAT_BOOK_CLUSTER_CREATED_GRP = 'created'
CHAT_BOOK_CLUSTER_JOINED_GRP = 'joined'

CHAT_GRP_TYPE_CLASS = '1'  # 班级类群组  00
CHAT_GRP_TYPE_CREATE = '2'  # 创建的自定义群组  01
CHAT_GRP_TYPE_JOINED = '3'  # 加入的自定义群组  11

PEOPLE_RELATION_SELF = 0  # 自己
PEOPLE_RELATION_FRIEND = 1  # 通讯录中的好友
PEOPLE_RELATION_NONE = 2  # 陌生人

# 圈子类型
MOMENT_NEW = '0'  # 最新动态
MOMENT_SCHOOL = '1'  # 学校圈
MOMENT_CLASS = '2'  # 班级圈
MOMENT_MY = '3'  # 个人动态

# 圈子信息请求来源
MOMENT_FROM_LIST = 'list'  # 列表请求
MOMENT_FROM_DETAIL = 'detail'  # 详情请求

# 查询圈子动态列表时，显示的最大回复数量
MOMENT_MAX_REPLY = 3

MOMENT_EVALUATE_ZAN = 1
MOMENT_EVALUATE_CAI = 2


# 视频转码&压缩状态
VIDEO_CONVERT_STATUS_NONE = 0
VIDEO_CONVERT_STATUS_ING = 1
VIDEO_CONVERT_STATUS_SUCC = 2
VIDEO_CONVERT_STATUS_FAIL = 3

# 音频转码状态
VOICE_CONVERT_STATUS_NONE = 0
VOICE_CONVERT_STATUS_ING = 1
VOICE_CONVERT_STATUS_SUCC = 2
VOICE_CONVERT_STATUS_FAIL = 3

# 视频截图状态
VIDEO_SNAPSHOT_STATUS_NONE = 0
VIDEO_SNAPSHOT_STATUS_ING = 1
VIDEO_SNAPSHOT_STATUS_SUCC = 2
VIDEO_SNAPSHOT_STATUS_FAIL = 3

# 在global表中，移动端下载二维码的Key
MOBILE_DOWNLOAD_QRCODE_KEY_IN_DB = 'mobile_qrcode'

GROUP_MAX = 10

WECHAT_JUMP_NOTIFY = '/m/notice/parent/noticeDetail?notify_id={NOTIFY_ID}&sid={SCHOOL_ID}&from=weixin&fromGo=list'
