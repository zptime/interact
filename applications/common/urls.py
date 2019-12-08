# -*- coding=utf-8 -*-

from django.conf.urls import url
from django.views.generic import RedirectView
from applications.common.views import api_logout, api_user_verify, api_user_info, api_stu_info \
    , api_class_student_list, api_teachclass_add, api_teachclass_delete, api_upload_image, api_upload_voice \
    , api_upload_video, api_upload_file, api_school_class_list, api_user_class_list, api_wx_voice_fetch

urlpatterns = [
    url(r'^logout/?$', RedirectView.as_view(url='html/logout', permanent=False)),
    url(r'^api/common/logout/?$', api_logout),
    url(r'^api/common/user/verify/?$', api_user_verify),
    url(r'^api/common/user/info/?$', api_user_info),
    url(r'^api/common/stu/info/?$', api_stu_info),
    url(r'^api/common/class/student/list/?$', api_class_student_list),

    url(r'^api/common/class/list/?$', RedirectView.as_view(url='/api/common/school/class/list/', permanent=False)),
    url(r'^api/common/myclass/list/?$', RedirectView.as_view(url='/api/common/user/class/list/', permanent=False)),
    url(r'^api/common/myclass/simple/list/?$', RedirectView.as_view(url='/api/common/user/class/list/', permanent=False)),
    url(r'^api/common/teachclass/add/?$', api_teachclass_add),
    url(r'^api/common/teachclass/delete/?$', api_teachclass_delete),

    url(r'^api/common/upload/image/?$', api_upload_image),
    url(r'^api/common/upload/voice/?$', api_upload_voice),
    url(r'^api/common/upload/video/?$', api_upload_video),
    url(r'^api/common/upload/file/?$', api_upload_file),
    url(r'^api/common/wx/voice/fetch/?$', api_wx_voice_fetch),

    # V2
    url(r'^api/common/school/class/list/?$', api_school_class_list),
    url(r'^api/common/user/class/list/?$', api_user_class_list),


]
