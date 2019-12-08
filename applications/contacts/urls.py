# -*- coding=utf-8 -*-

from django.conf.urls import url
from django.views.generic import RedirectView
from applications.contacts.views import api_chatid, api_group_chatid, api_class_chatid \
, api_group_invite_status, api_group_invite_agree, api_group_invite_deny, api_group_user_quit \
, api_book_contact, api_book_group, api_group_invite_available, api_v2_group_invite_available \
, api_group_invite, api_class_user_list, api_group_user_list, api_group_user_delete \
, api_group_detail, api_group_create, api_group_edit, api_group_dissolve


urlpatterns = [
    # V1

    url(r'^api/chat/chatid/get/?$', api_chatid),   # 不再支持
    url(r'^api/chat/chatid/group/get/?$', api_group_chatid),   # 不再支持
    url(r'^api/chat/chatid/class/get/?$', api_class_chatid),   # 不再支持
    url(r'^api/chat/book/contact/?$', RedirectView.as_view(url='/api/contacts/book/person/', permanent=False)),
    url(r'^api/chat/book/cluster/?$', RedirectView.as_view(url='/api/contacts/book/group/', permanent=False)),
    url(r'^api/chat/group/users/invite/available/?$', RedirectView.as_view(url='/api/contacts/group/user/invite/available/', permanent=False)),
    url(r'^api/chat/group/users/invite/?$', RedirectView.as_view(url='/api/contacts/group/user/invite/', permanent=False)),
    url(r'^api/chat/group/users/invite/status/?$', api_group_invite_status),  # 不再支持
    url(r'^api/chat/group/users/invite/agree/?$', api_group_invite_agree),  # 不再支持
    url(r'^api/chat/group/users/invite/deny/?$', api_group_invite_deny),  # 不再支持
    url(r'^api/chat/class/users/list/?$', RedirectView.as_view(url='/api/contacts/class/user/list/', permanent=False)),
    url(r'^api/chat/group/users/list/?$', RedirectView.as_view(url='/api/contacts/group/user/list/', permanent=False)),
    url(r'^api/chat/group/users/delete/?$', RedirectView.as_view(url='/api/contacts/group/user/delete/', permanent=False)),
    url(r'^api/chat/group/users/quit/?$', api_group_user_quit), # 不再支持
    url(r'^api/chat/group/info/?$', RedirectView.as_view(url='/api/contacts/group/detail/', permanent=False)),
    url(r'^api/chat/group/create/?$', RedirectView.as_view(url='/api/contacts/group/create/', permanent=False)),
    url(r'^api/chat/group/edit/?$', RedirectView.as_view(url='/api/contacts/group/edit/', permanent=False)),
    url(r'^api/chat/group/dissolve/?$', RedirectView.as_view(url='/api/contacts/group/dissolve/', permanent=False)),

    # V2

    url(r'^api/contacts/book/person/?$', api_book_contact),
    url(r'^api/contacts/book/group/?$', api_book_group),
    url(r'^api/contacts/group/user/invite/available/?$', api_group_invite_available),
    url(r'^api/v2/contacts/group/user/invite/available/?$', api_v2_group_invite_available),
    url(r'^api/contacts/group/user/invite/?$', api_group_invite),
    url(r'^api/contacts/class/user/list/?$', api_class_user_list),
    url(r'^api/contacts/group/user/list/?$', api_group_user_list),
    url(r'^api/contacts/group/user/delete/?$', api_group_user_delete),
    url(r'^api/contacts/group/detail/?$', api_group_detail),
    url(r'^api/contacts/group/create/?$', api_group_create),
    url(r'^api/contacts/group/edit/?$', api_group_edit),
    url(r'^api/contacts/group/dissolve/?$', api_group_dissolve),
]
