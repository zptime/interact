# -*- coding=utf-8 -*-

from django.conf.urls import url
from django.views.generic import RedirectView

from applications.android_ios.views import api_mobile_heartbeat, api_mobile_service_list, api_mobile_version \
, api_mobile_update, api_mobile_qrcode_info, api_mobile_android_download, api_mobile_android_upgrade \
, api_mobile_passwd_forget_reset, api_mobile_passwd_retrieve, api_mobile_smscode_send, api_mobile_smscode_verify


urlpatterns = [
    url(r'^api/mobile/heartbeat/?$', api_mobile_heartbeat),
    url(r'^api/mobile/service/list/?$', api_mobile_service_list),
    url(r'^api/mobile/version/?$', api_mobile_version),
    url(r'^api/mobile/update/?$', api_mobile_update),
    url(r'^api/mobile/qrcode/info/?$', api_mobile_qrcode_info),
    url(r'^api/mobile/android/download/?$', api_mobile_android_download),
    url(r'^api/mobile/android/upgrade/(?P<fname>\S+)$', api_mobile_android_upgrade),

    url(r'^api/mobile/passwd/forget/reset/?$', api_mobile_passwd_forget_reset),
    url(r'^api/mobile/passwd/retrieve/?$', api_mobile_passwd_retrieve),
    url(r'^api/mobile/smscode/send/?$', api_mobile_smscode_send),
    url(r'^api/mobile/smscode/verify/?$', api_mobile_smscode_verify),

]
