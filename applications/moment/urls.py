# -*- coding=utf-8 -*-

from django.conf.urls import url
from views import get_moment_list, get_moment_list_only_display, get_moment_detail, moment_delete, moment_like \
, moment_read, moment_reply, moment_vote, moment_publish, moment_publish_basic, moment_publish_vote, moment_publish_dayoff \
, moment_publish_evaluate, api_internal_proxy

urlpatterns = [
    # url(r'^api/moment$', api_api),  # test
    url(r'^api/moment/dynamics/list/?$', get_moment_list),  # 获取圈子动态列表
    url(r'^api/moment/dynamics/showlist/?$', get_moment_list_only_display),  # 获取圈子动态列表(仅用于展示)
    url(r'^api/moment/dynamics/detail/?$', get_moment_detail),  # 获取圈子动态详细
    url(r'^api/moment/dynamics/delete/?$', moment_delete),  # 删除圈子动态
    url(r'^api/moment/dynamics/like/?$', moment_like),  # 点赞圈子动态
    url(r'^api/moment/dynamics/read/?$', moment_read),  # 阅读圈子动态
    url(r'^api/moment/dynamics/reply/?$', moment_reply),  # 回复圈子动态
    url(r'^api/moment/dynamics/vote/?$', moment_vote),  # 投票圈子动态

    url(r'^api/moment/dynamics/publish/?$', moment_publish),  # 该接口一分为4，暂时保留方便前向兼容
    url(r'^api/moment/dynamics/publish/basic/?$', moment_publish_basic),  # 发布语音、图片、视频、附件四类基础互动
    url(r'^api/moment/dynamics/publish/vote/?$', moment_publish_vote),    # 发布投票互动
    url(r'^api/moment/dynamics/publish/dayoff/?$', moment_publish_dayoff),   # 发布请假互动
    url(r'^api/moment/dynamics/publish/evaluate/?$', moment_publish_evaluate),  # 发布评价互动

    url(r'^api/internal/proxy/?$', api_internal_proxy),
]
