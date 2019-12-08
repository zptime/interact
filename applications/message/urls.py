# -*- coding=utf-8 -*-

from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^api/msg/overview$', api_msg_overview),
    url(r'^api/msg/list$', api_msg_list),
    url(r'^api/msg/detail$', api_msg_detail),
    url(r'^api/msg/delete$', api_msg_delete),
    url(r'^api/msg/deleteall$', api_msg_deleteall),
    url(r'^api/msg/read$', api_msg_read),
    url(r'^api/msg/pull$', api_msg_pull),
]