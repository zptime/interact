# -*- coding: utf-8 -*-

import logging
import random
from urlparse import urljoin

from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render
from django_cas_ng import views as cas_views
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.decorators import login_required

from applications.android_ios.models import MobileDef
from applications.common.models import MOBILE_TYPE_APPLE_PHONE, MOBILE_TYPE_ANDROID_PHONE, Class
from applications.common.services import get_current_sys_domain
from utils.auth_check import validate
from utils.constant import FALSE_INT


logger = logging.getLogger(__name__)


def _prepare_ctx(request, html):
    ctx = {}
    if html == 'page_moment_detail':
        ctx = {
            'moment_id': request.GET.get('moment_id')
        }
    if html == 'page_mobile_download':
        iphone = MobileDef.objects.filter(is_del=FALSE_INT, type=MOBILE_TYPE_APPLE_PHONE).first()
        android_phone = MobileDef.objects.filter(is_del=FALSE_INT, type=MOBILE_TYPE_ANDROID_PHONE).first()
        ctx = {
            'ios_pkg': urljoin(get_current_sys_domain(), iphone.latest_version_url) if iphone else '',
            'android_pkg': urljoin(get_current_sys_domain(), settings.ANDROID_APK_DOWNLOAD + '?rand='+str(random.randint(1, 10000000))),
        }
    if html == 'page_board_class_moment':
        school_code = request.GET.get('school_code')
        grade_num = request.GET.get('grade_num')
        class_num = request.GET.get('class_num')
        clazz = Class.objects.filter(
            school__code=school_code, grade_num=int(grade_num), class_num=int(class_num), del_flag=FALSE_INT).first()
        ctx = {'class_id': clazz.id} if clazz else {'class_id': ''}
    return ctx


@login_required
def page_moment(request):
    ctx = _prepare_ctx(request, page_moment.__name__)
    return render(request, 'page/moment/index.html', ctx)


@login_required
def page_moment_detail(request):
    ctx = _prepare_ctx(request, page_moment_detail.__name__)
    return render(request, 'page/moment/detail.html', ctx)


def page_mobile_download(request):
    ctx = _prepare_ctx(request, page_mobile_download.__name__)
    return render(request, 'page/mobile/download.html', ctx)
 
    
def page_mobile_qrcode(request):
    ctx = _prepare_ctx(request, page_mobile_qrcode.__name__)
    return render(request, 'page/mobile/qrcode.html', ctx)


def page_logout(request):
    return cas_views.logout(request)


def page_login(request):
    return cas_views.login(request)


def page_login_local(request):
    ctx = _prepare_ctx(request, page_login_local.__name__)
    return render(request, 'common/login.html', ctx)


def page_board_class_moment(request):
    try:
        logger.info(request.get_full_path())
        ctx = _prepare_ctx(request, page_board_class_moment.__name__)
    except Exception as e:
        raise Http404
    return render(request, 'page/board/classmoment.html', ctx)


@login_required
def page_m_index(request):
    return render(request, 'mobile/index.html')


@login_required
def page_m_moment(request):
    return render(request, 'mobile/index.html')


@login_required
def page_m_contacts(request):
    return render(request, 'mobile/index.html')


@login_required
def page_m_notification(request):
    return render(request, 'mobile/index.html')


@login_required
def page_weixin_test(request):
    return render(request, 'mobile/index.html')


def wx_get_verifyfile(request):
    filedata = 'jIjfmE2UW1zSOJPc'
    response = HttpResponse(filedata)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="MP_verify_jIjfmE2UW1zSOJPc.txt"'
    return response