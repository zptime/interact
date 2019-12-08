# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += [
    url(r'^user_center/', include('applications.user_center.urls')),
    url(r'^msg_center/', include('applications.message.urls')),
    url(r'', include('applications.android_ios.urls')),
    url(r'', include('applications.moment.urls')),
    url(r'', include('applications.notification.urls')),
    url(r'', include('applications.common.urls')),
    url(r'', include('applications.contacts.urls')),
]

# swagger
urlpatterns += patterns('applications.swagger.views',
    # url(r'^$', 'api_index'),
    url(r'^api/$', 'api_index'),
    url(r'^api/docs/$', 'api_docs'),
)

# page
urlpatterns += patterns('templates.html',
    url(r'^html/login$', 'page_login'),
    url(r'^html/logout$', 'page_logout'),
    url(r'^html/locallogin$', 'page_login_local'),

    url(r'^$', 'page_moment'),
    url(r'^html/moment$', 'page_moment'),
    url(r'^html/moment/detail$', 'page_moment_detail'),

    url(r'^html/mobile/download$', 'page_mobile_download'),
    url(r'^html/mobile/qrcode$', 'page_mobile_qrcode'),

    url(r'^html/board/moment$', 'page_board_class_moment'),

    url(r'^m', 'page_m_index'),
    # url(r'^m/moment/?$', 'page_m_moment'),
    # url(r'^m/contacts/?$', 'page_m_contacts'),
    # url(r'^m/notification/?$', 'page_m_notification'),
    url(r'^m/weixin/?$', 'page_weixin_test'),
    url(r'^MP_verify_jIjfmE2UW1zSOJPc.txt/?$', 'wx_get_verifyfile'),  # 微信域名验证
)

# page's favicon
urlpatterns += patterns('', (r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),)

urlpatterns += staticfiles_urlpatterns()   # static

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': os.path.join(settings.BASE_DIR, 'media'),}),
    )
