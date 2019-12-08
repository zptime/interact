# -*- coding=utf-8 -*-
from django.conf.urls import url
from django.views.generic import RedirectView

from views import api_notification_inbox, api_notification_outbox, api_notification_detail, api_notification_read_list \
    , api_notification_receiver_detail, api_notification_outbox_delete, api_notification_inbox_delete, api_notification_read \
    , api_notification_unread, api_notification_publish, api_notification_remind

urlpatterns = [
    url(r'^api/notification/list/all/?$', RedirectView.as_view(url='/api/notification/inbox/', permanent=False)),
    url(r'^api/notification/list/issued/?$', RedirectView.as_view(url='/api/notification/outbox/', permanent=False)),
    url(r'^api/notification/receivers/list/?$', RedirectView.as_view(url='/api/notification/receiver/detail/', permanent=False)),
    url(r'^api/notification/delete/issued/?$', RedirectView.as_view(url='/api/notification/outbox/delete/', permanent=False)),
    url(r'^api/notification/delete/received/?$', RedirectView.as_view(url='/api/notification/inbox/delete/', permanent=False)),

    # V2

    url(r'^api/notification/inbox/?$', api_notification_inbox),  # 收件箱
    url(r'^api/notification/outbox/?$', api_notification_outbox),  # 发件箱
    url(r'^api/notification/detail/?$', api_notification_detail),  # 获取通知详情
    url(r'^api/notification/read/list/?$', api_notification_read_list),  # 阅读情况列表
    url(r'^api/notification/receiver/detail/?$', api_notification_receiver_detail),  # 获取通知接收者姓名列表
    url(r'^api/notification/outbox/delete/?$', api_notification_outbox_delete),  # 删除通知发布记录，删除后所有人不可见
    url(r'^api/notification/inbox/delete/?$', api_notification_inbox_delete),  # 删除通知接收记录，删除后仅个人不可见
    url(r'^api/notification/read/?$', api_notification_read),  # 阅读通知或标记通知为已读
    url(r'^api/notification/unread/?$', api_notification_unread),  # 标记通知为未读
    url(r'^api/notification/publish/?$', api_notification_publish),  # 发布通知
    url(r'^api/notification/remind/?$', api_notification_remind),  # 提醒未读人员
]
