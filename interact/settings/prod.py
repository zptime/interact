# -*- coding: utf-8 -*-

from base import *

SYS_DESC = u'互动系统生产环境'

DEBUG = False

LOGIN_URL='/html/login'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hx_interact',
        'USER': 'admin',
        'PASSWORD': 'fhcloud86Fh12#$',
        'HOST': '192.168.100.3',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
        'OPTIONS': {'charset':'utf8mb4'},
    },
    # school_center real-time DB for query
    'school_center': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'user_center',
        'USER': 'admin',
        'PASSWORD': 'Fh12#$',
        'HOST': '192.168.100.11',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,
    }

}

CAS_SERVER_URL = "http://sso.hbeducloud.com/sso/"

REDIS_URL = '192.168.100.3:6379'
REDIS_PASSWD = 'fhcloud86'
REDIS_LOCATION = 'redis://:%s@%s/' % (REDIS_PASSWD, REDIS_URL)
CELERY_BROKER_BACKEND = REDIS_LOCATION + '1'

AWS_ACCESS_KEY_ID = "9X99OHMSGA4ZJO0XZWIO"
AWS_SECRET_ACCESS_KEY = "tm92ArANm1fFeYFC9lXWqgVtTuMPoMfPjRKLljkf"
AWS_STORAGE_BUCKET_NAME = "interact_prod"
AWS_S3_HOST = "192.168.200.100"
AWS_S3_PORT = 8000

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION + '0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 10,  # in seconds
            "SOCKET_TIMEOUT": 10,  # in seconds
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

# 是否使用S3存储
USE_S3 = True

# 是否使用异步任务调度
USE_ASYNC = True

# 是否自动转码&压缩
IS_AUTO_CONVERT_AND_COMPRESS_MP4 = True

# 是否针对wav和amr格式自动转码
IS_AUTO_CONVERT_MOV_TO_MP3 = True

# 是否自动为视频截图
IS_AUTO_SNAPSHOT = True

# 是否启用消息机制
USE_MSG = True

USE_USER_CENTER_DB_LOGIN = True
