# -*- coding=utf-8 -*-

import imp
import logging
import os
import random
from urlparse import urljoin
from django.db import transaction
from django.db.models import F
from django.http import StreamingHttpResponse, Http404

from applications.android_ios.models import MobileDef, MobileHistory, MobileService, SmsCode
from applications.common.services import get_current_sys_domain
from utils import file_storage
from utils import net_helper
from utils import s3_storage
from utils import tools
from utils.errcode import *
from utils.file_storage import safe_folder
from utils.remote_call import remote_request, get_usercenter_address
from utils.sms import sendsms
from utils.tools import BusinessException, get_type_current_user
from applications.user_center.utils_realtime import get_password
from applications.common.models import *
from utils.utils_time import now

logger = logging.getLogger(__name__)


def get_mobile_version(mobile_type):
    mobile_ver = MobileDef.objects.filter(is_del=FALSE_INT, type=int(mobile_type)).first()
    if not mobile_ver:
        raise BusinessException(CLIENT_NOT_EXIST)

    version_url = mobile_ver.latest_version_url
    if (not version_url.startswith('http://')) and (not version_url.startswith('https://')):
        version_url = urljoin(get_current_sys_domain(), mobile_ver.latest_version_url)

    # 安卓手机下载更新包走统计接口
    if int(mobile_type) == MOBILE_TYPE_ANDROID_PHONE:
        apk_name = mobile_ver.latest_version_url[mobile_ver.latest_version_url.rfind('/')+1:]

        (shortname, extension) = os.path.splitext(apk_name)
        apk_name = '%s_%s%s' % (shortname, str(random.randint(1, 10000000)), extension)

        version_url = urljoin(get_current_sys_domain(), settings.ANDROID_APK_DOWNLOAD_UPGRADE + apk_name)

    checksum = mobile_ver.latest_version_checksum if mobile_ver.latest_version_checksum else ''

    ret_value = {
        'latest_version': str(mobile_ver.latest_version),
        'latest_version_url': version_url,
        'latest_version_checksum': checksum,
        'support_version': str(mobile_ver.support_version),
        'version_info': mobile_ver.version_info
    }
    return ret_value


def get_mobile_qrcode():
    # qrcode_obj = GlobalPara.objects.filter(is_del=FALSE_INT, key=MOBILE_DOWNLOAD_QRCODE_KEY_IN_DB).first()
    # if not qrcode_obj:
    #     url = ''
    # else:
    #     url = urljoin(get_current_sys_domain(), qrcode_obj.value)
    # return {
    #     'qrcode': url
    # }
    return urljoin(get_current_sys_domain(), 'media/public/packages/mobile.png')


@transaction.atomic
def update_mobile(type, latest_version, latest_pkg, version_info):
    mobile = MobileDef.objects.filter(is_del=FALSE_INT, type=int(type)).first()
    if not mobile:
        raise BusinessException(CLIENT_NOT_EXIST)

    checksum = ''

    if int(type) == MOBILE_TYPE_ANDROID_PHONE:
        if not latest_pkg:
            raise BusinessException(NO_APK_ERROR)

        relative_path = file_storage.gen_path(os.path.join(settings.MEDIA_PATH_PUBLIC, 'packages'), latest_pkg.name)

        if MobileHistory.objects.filter(url=relative_path).exists():
            raise BusinessException(APK_NAME_ERROR)

        if settings.USE_S3:
            checksum = s3_storage.get_operator().upload_file_obj(latest_pkg, relative_path)
        else:
            checksum = file_storage.save_file(latest_pkg, os.path.join(settings.BASE_DIR, relative_path))

        returned_url = urljoin(get_current_sys_domain(), mobile.latest_version_url)
    elif int(type) == MOBILE_TYPE_APPLE_PHONE:
        if latest_pkg:
            raise BusinessException(IOS_HAS_APK_ERROR)
        relative_path = settings.IOS_DOWNLOAD
        returned_url = relative_path
    else:
        raise BusinessException(UNSUPPORT_TYPE_UPGRADE)

    # 更新当前版本数据库
    mobile.latest_version = latest_version
    mobile.latest_version_url = relative_path
    mobile.latest_version_checksum = checksum
    mobile.version_info = version_info
    mobile.save()

    # 更新历史版本数据库
    MobileHistory.objects.create(type=int(type), version=latest_version, version_info=version_info, url=relative_path)

    return {
        'latest_version': mobile.latest_version,
        'latest_version_url': returned_url
    }


def mobile_android_download(is_upgrade=False):
    def read_local_file(file_path, chunk_size=512):
        with open(file_path, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    with transaction.atomic():
        android_phone = MobileDef.objects.filter(is_del=FALSE_INT, type=MOBILE_TYPE_ANDROID_PHONE).first()

        # 下载次数记录+1
        ver = android_phone.latest_version
        down_ver = MobileHistory.objects.filter(is_del=FALSE_INT, type=MOBILE_TYPE_ANDROID_PHONE, version=ver).first()
        if down_ver:
            down_ver.download_count = F('download_count') + 1
            if is_upgrade:
                down_ver.upgrade_count = F('upgrade_count') + 1
            down_ver.save()

        f_path = os.path.join(settings.BASE_DIR, android_phone.latest_version_url)
        shortname, ext = os.path.splitext(f_path[f_path.rfind('/')+1:])
        if settings.USE_S3:
            if not os.path.exists(f_path):
                # 如果文件夹不存在，则创建
                safe_folder(os.path.join(settings.BASE_DIR, os.path.join(settings.MEDIA_PATH_PUBLIC, 'packages')))

                logger.info('user wanna download apk, but we should transfer it from S3 to local disk')
                s3_storage.get_operator().download_file(android_phone.latest_version_url, f_path)
            else:
                logger.info('user download apk from local disk cache directly')
        else:
            if not os.path.exists(f_path):
                logger.error('not use S3, but cannot find android apk on local disk')
                raise Http404

        logger.info('user download apk: '+ shortname + ext)
        response = StreamingHttpResponse(read_local_file(f_path))
        response['Content-length'] = os.path.getsize(f_path)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(shortname + ext)
        return response


def get_mobile_service_list(user, mobile_type):
    mobile_services_all = MobileService.objects.filter(is_del=FALSE_INT) \
        .values('code', 'login_url', 'logout_url', 'is_heartbeat', 'support_user_type', 'support_device', 'heartbeat_interval', 'heartbeat_url', 'para')
    mobile_services_all_dict = {each_dict['code']: each_dict for each_dict in mobile_services_all}

    # 从用户中心获取该学校开通的所有应用
    services_from_uc = user.school.schoolservice_set.filter(del_flag=FALSE_INT)
    mobile_services = list()

    duplicate_codes = list()
    for each_service in services_from_uc:
        service_code = each_service.service.code

        # 分离service@system模式定义的服务
        pure_system = tools.split_system(service_code)
        if pure_system in duplicate_codes:
            continue
        duplicate_codes.append(pure_system)

        # 过滤掉不在移动端显示的应用、过滤掉不在该种设备上使用的应用
        if pure_system not in mobile_services_all_dict.keys() or \
            mobile_services_all_dict[pure_system]['support_device'] & int(mobile_type) == 0:
            continue

        # 非管理员看不到仅管理员可用的应用
        if mobile_services_all_dict[pure_system]['support_user_type'] == 0:
            teacher = get_type_current_user(user)
            if not isinstance(teacher, Teacher):
                continue
            current_service = Service.objects.filter(code=service_code, del_flag=FALSE_INT).first()
            super_role = Role.objects.filter(service=current_service, code=settings.SUPER_ADMIN_CODE, del_flag=FALSE_INT).first()
            is_sysadmin = UserRole.objects.filter(user=teacher, school=teacher.school, role=super_role, del_flag=FALSE_INT).exists()
            if not is_sysadmin:
                continue
        # 教师、家长、学生只能看到自己角色可见的应用
        else:
            if int(mobile_services_all_dict[pure_system]['support_user_type']) & user.type == 0:
                continue

        mobile_services.append({
            'service_code': pure_system,
            # 'service_name': each_service.service.name,
            'service_domain': net_helper.url_with_scheme_and_location(each_service.service.internet_url),
            'service_para': mobile_services_all_dict[pure_system]['para'],
            'login_url': mobile_services_all_dict[pure_system]['login_url'],
            'logout_url': mobile_services_all_dict[pure_system]['logout_url'],
            'service_is_heartbeat': str(mobile_services_all_dict[pure_system]['is_heartbeat']),
            'service_heartbeat_url': mobile_services_all_dict[pure_system]['heartbeat_url'],
            'service_heartbeat_interval': mobile_services_all_dict[pure_system]['heartbeat_interval']
        })
    return mobile_services


def smscheck_send(mobile):
    '''
        发送短信验证码
    '''
    result_dict = sendsms(mobile)
    logger.info('sms: %s' % result_dict)
    if 'thirdcode' not in result_dict or 'timestamp' not in result_dict:
        raise BusinessException(SMSCODE_SEND_FAIL)
    code = result_dict['thirdcode']
    timestamp = result_dict['timestamp']
    qs = SmsCode.objects.filter(mobile=mobile, is_del=FALSE_INT)
    if qs.exists():
        qs.update(code=str(code), timestamp=timestamp, update_time=now())
    else:
        SmsCode.objects.create(mobile=mobile, code=str(code), timestamp=timestamp)


def smscheck_verify(mobile, smscode):
    '''
        校验短信验证码
    '''
    import time
    code_saved = SmsCode.objects.filter(is_del=FALSE_INT, mobile=mobile).exclude(code=None).first()
    if not code_saved:
        raise BusinessException(SMSCODE_NOT_EXIST)

    if code_saved.timestamp:
        timestamp_saved = int(code_saved.timestamp)
        current_time = int(time.time())
        if timestamp_saved + settings.SMSCODE_EXPIRE_TIME < current_time:
            raise BusinessException(SMSCODE_EXPIRED)

    if code_saved.code != smscode:
        raise BusinessException(SMSCODE_NOT_MATCH)


def password_forget(mobile, smscode, new_passwd):
    smscheck_verify(mobile, smscode)
    account = Account.objects.filter(del_flag=FALSE_INT, mobile=mobile).first()
    if not account:
        raise BusinessException(USER_NOT_EXIST)
    payload = {
        'account_id': str(account.id),
        'new_password': str(new_passwd)
    }
    destiny = get_usercenter_address()
    logger.info('send reset password request to usercenter: %s' % destiny)
    return remote_request(destiny, '/open/reset/password', payload)


def password_retrieve(mobile, smscode):
    smscheck_verify(mobile, smscode)
    mod = imp.load_source('utils.utils_crypto', 'utils/utils_crypto.py')
    passwd_encryped = get_password(mobile)
    if not passwd_encryped:
        raise BusinessException(PASSWORD_NOT_EXIST)
    return mod.encode_AES(mod.xor_crypt_string(data=passwd_encryped, decode=True))





