# -*- coding=utf-8 -*-

import os

# 系统错误码前缀
SYSTEM_CODE = 7

# root
DB_ADMIN = 'root'

# 本系统包含的对外服务
SYSTEM_NAME = 'interact'
SYSTEM_DESC = u'互动平台'
SERVICE_SYSTEM_SPLIT_CHAR = '@'

SECRET_KEY = '0f$@gun=@7es+9t%m%u7xl$g&kqar$ptt-xpc99lkdn6j_fmjn'

WSGI_APPLICATION = 'interact.wsgi.application'

ROOT_URLCONF = 'interact.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

TEMP_DIR = os.path.join(BASE_DIR, 'temp')

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

MEDIA_PATH_PUBLIC = 'media/public/'  # 公开的media文件
MEDIA_PATH_PROTECT = 'media/protected/'  # 私有的media文件


ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'user_center.Account'

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'applications.bizlog',
    'applications.swagger',
    'applications.message',
    'applications.contacts',
    'applications.android_ios',
    'applications.common',
    'applications.moment',
    'applications.notification',
    'applications.user_center',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'applications.bizlog.record.LogMiddleware',
)

# 本地认证结合CAS认证
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SUIT_CONFIG = {
    'ADMIN_NAME': u'华校互动平台数据管理',
    'HEADER_DATE_FORMAT': '',
    'HEADER_TIME_FORMAT': 'H:i',
    'MENU_OPEN_FIRST_CHILD': True,
    'LIST_PER_PAGE': 50,
    'MENU': (
        {'app': 'common', 'label': u'通用', 'models': ('SysImage', 'SysVoice', 'SysVideo', 'SysFile', 'GlobalPara')},
        {'app': 'android_ios', 'label': u'安卓和ios', 'models': ('MobileDef', 'MobileService', 'MobileHistory')},
        {'app': 'contacts', 'label': u'通讯录'},
        {'app': 'moment', 'label': u'圈子'},
        {'app': 'notification', 'label': u'通知'},
    )
}

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

LOG_PATH_DJANGO = os.path.join(BASE_DIR + '/log/', 'django.log')
LOG_PATH_COMMAND = os.path.join(BASE_DIR + '/log/', 'command.log')
LOG_PATH_DB = os.path.join(BASE_DIR + '/log/', 'db.log')
LOG_PATH_USERCENTER = os.path.join(BASE_DIR + '/log/', 'usercenter.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_PATH_DJANGO,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 'request_handler': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(BASE_DIR + '/log/', 'django.log'),
        #     'maxBytes': 1024 * 1024 * 5,  # 5 MB
        #     'backupCount': 20,
        #     'formatter': 'standard',
        # },
        'django_command': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_PATH_COMMAND,
            'formatter': 'standard',
        },
        'django.db.backends_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_PATH_DB,
            'formatter': 'standard',
        },
        'sync_user_data': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_PATH_USERCENTER,
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
        },
        'applications': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django_command': {
            'handlers': ['django_command', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'applications.user_center': {
            'handlers': ['sync_user_data', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_S3_USE_SSL = False
from boto.s3.connection import OrdinaryCallingFormat
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

CAS_VERSION = "3"
CAS_IGNORE_REFERER = True
CAS_CREATE_USER = False

# 用户中心相关参数
REQUEST_CONNECTION_TIMEOUT_SECONDS = 30
SERVICE_USER_CENTER = "user_center"
SERVICE_USER_CENTER_BUCKET = "school_center"
USER_CENTER_S3_HOST=''
API_USER_CENTER_LIST_SUBNET = "/open/list/subnet"
API_USER_CENTER_DETAIL_UPDATE_TIME = "/open/detail/update_time"
API_USER_CENTER_LIST_ITEMS = "/open/list/items"
API_USER_CENTER_CALL_API = "/open/call/api"
API_USER_CENTER_APP_REFRESH_ITEM = "/user_center/api/refresh/item"

# 同步用户中心哪些数据库表
MODEL_SYNC_FROM_USER_CENTER = ["Subnet", "School", "Grade", "Class", "Account", "Student", "Parent", "ParentStudent", "Title", "Teacher", "TeacherClass", "Subject", "TeacherSubject", "Service", "SchoolService", "Role", "UserRole", "Textbook", "TeacherTextbook", "SchoolTextbook"]


FFMPEG = '/usr/local/ffmpeg/bin/ffmpeg'

CHUNKED_UPLOAD_PATH = os.path.join(BASE_DIR, "temp/chunked_upload")
CHUNKED_UPLOAD_ABSTRACT_MODEL = 'common_chunkedupload'

RATELIMIT_CACHE_PREFIX = 'ratelimit'

# 支持上传文件类型与大小
UPLOAD_IMAGE_EXTENSION = ('*',)
UPLOAD_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB
UPLOAD_VOICE_EXTENSION = ('*',)
UPLOAD_VOICE_SIZE = 20 * 1024 * 1024  # 20MB
UPLOAD_VIDEO_EXTENSION = ('mp4', 'mov',)
UPLOAD_VIDEO_SIZE = 200 * 1024 * 1024  # 200MB
UPLOAD_FILE_EXTENSION = ('*',)
UPLOAD_FILE_SIZE = 300 * 1024 * 1024  # 300MB

SESSION_COOKIE_AGE = 90 * 24 * 60 * 60

# 自定义HTTP请求消息头，用于移动设备标识客户端用户类型与学校
HTTP_HEADER_CURRENT_USER_TYPE = 'CURRENT_USER_TYPE'

# 是否使用环信认证注册接口，需要和环信服务端配置保持一致
HUANXIN_REGISTRY_AUTH = True

# 环信ID接口调用间隔时间，防止被环信限流（单位：秒）
SINGLE_OPERATOR_INTERVAL = 0.2
GROUP_OPERATION_INTERVAL = 0.3

# 环信ID注册接口，单次注册多少用户
REGISTER_HUANXIN_BULK_NUM_SINGLE = 120

# 环信ID注册接口，单次注册多少班级群组
REGISTER_HUANXIN_BULK_NUM_CLASS = 50

# 环信批量删除用户，单次数量限制
HUANXIN_BULK_DELETE_USER = 100

# 环信批量用户加入群组，单次数量限制
HUANXIN_BULK_MEMBER_ADD_ONCE = 50

# 环信获取所有群组一次获取个数
HUANXIN_GET_GROUPS_ONCE = 20

# 环信请求超时时间
HUANXIN_REQUEST_TIMEOUT = 20


# crop图片长宽
PICTURE_CROP_WIDTH = 200

# 宽大于多少的图片需要压缩
PICTURE_NEED_THUMB_WIDTH = 300

# 高大于多少的图片需要压缩
PICTURE_NEED_THUMB_HEIGHT = 650

# 体积大于多少的图片需要压缩（字节）
# PICTURE_NEED_THUMB_SIZE = 1024 * 200

# 缩略图 and 裁剪图 格式
PICTURE_THUMB_FORMAT = 'png'

# 多长时间媒体文件过期（秒）
MEDIA_EXPIRE_TIME = 60 * 60 * 24 * 10

# 安卓最新版本下载路径
ANDROID_APK_DOWNLOAD = 'api/mobile/android/download'
ANDROID_APK_DOWNLOAD_UPGRADE = 'api/mobile/android/upgrade/'
# ANDROID_APK_DOWNLOAD_UPGRADE = ANDROID_APK_DOWNLOAD + '?upgrade=yes'
IOS_DOWNLOAD = 'https://itunes.apple.com/us/app/%E5%8D%8E%E6%A0%A1/id1146697819?mt=8'

# 超级管理员的默认角色编号
SUPER_ADMIN_CODE = '1'

SMSCODE_EXPIRE_TIME = 10 * 60

# log record&report setting
LOG_CENTER = {
    'system_code': SYSTEM_NAME,
    'system_name': SYSTEM_CODE,
    'domain': 'http://127.0.0.1:8001',
    'table': 'interact_bizlog',
    'rotate_search': 1,
    'include': ('^/api/', ),
    'exclude': ('^/api/$', '^/api/docs/$', ),
    'long_request': {
        'threshold': 1000 * 2,
        'report_include': ('*', ),
        'report_exclude': ('^/api/common/upload/image', ),
    },
    'head_record_length': -1,
    'request_record_length': -1,
    'response_record_length': -1,
    'appendix1_func': '',
    'appendix2_func': ''
}

# 网易短信网关
APPKEY_EASY = '6ec1b164f7e047b0faad4e8c1f5e0a82'
APPSECRET_EASY = 'f198afbb3955'
TEMPLATEID_EASY = 3032443