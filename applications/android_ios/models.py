# -*- coding=utf-8 -*-

from django.db import models

from applications.user_center.models import *
from utils.constant import *
from utils.utils_db import ManagerFilterDelete


class MobileHistory(models.Model):
    type = models.PositiveSmallIntegerField(u'设备类型',
        choices=((MOBILE_TYPE_APPLE_PHONE, u'iphone'),
                 (MOBILE_TYPE_APPLE_PAD, u'ipad'),
                 (MOBILE_TYPE_ANDROID_PHONE, u'android phone'),
                 (MOBILE_TYPE_ANDROID_PAD, u'android pad')))
    version = models.CharField(u'版本', max_length=20)
    url = models.CharField(u'版本下载路径', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    version_info = models.CharField(u'版本信息', max_length=800, blank=True, null=True)  # support html
    download_count = models.IntegerField(u'下载次数', default=0)  # 该版本总的下载次数
    upgrade_count = models.IntegerField(u'更新次数', default=0)   # 该版本更新安装次数
    create_time = models.DateTimeField(u'版本发布时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'mobile_history'
        verbose_name_plural = u'移动端历史版本表'
        verbose_name = u'移动端历史版本表'

    def __unicode__(self):
        return 'Version(%s)' % self.version


class MobileDef(models.Model):
    type = models.PositiveSmallIntegerField(u'设备',
        choices=((MOBILE_TYPE_APPLE_PHONE, u'iphone'),
                 (MOBILE_TYPE_APPLE_PAD, u'ipad'),
                 (MOBILE_TYPE_ANDROID_PHONE, u'android phone'),
                 (MOBILE_TYPE_ANDROID_PAD, u'android pad')))
    user_agent = models.CharField(u'http-user-agent关键字', max_length=500, blank=True, null=True)  #用逗号分割
    latest_version = models.CharField(u'当前最新版本', max_length=20)  # a.b.c
    latest_version_checksum = models.CharField(u'安装包校验', max_length=200, blank=True, null=True)
    latest_version_url = models.CharField(u'当前版本下载路径', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    support_version = models.CharField(u'服务器支持的最后版本', max_length=20)  # a.b.c  低于此版本需强制更新
    version_info = models.CharField(u'版本信息', max_length=800, blank=True, null=True) # support html
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'mobile_version'
        verbose_name_plural = u'移动端下载表'
        verbose_name = u'移动端下载表'

    def __unicode__(self):
        return 'LatestVersion(%s)' % self.latest_version


class MobileService(models.Model):
    code = models.CharField(u'关键字', max_length=100, blank=True, null=True)
    support_user_type = models.PositiveSmallIntegerField(u'支持用户类型', default=USER_TYPE_ALL)
    support_device = models.PositiveSmallIntegerField(u'支持移动端设备', default=MOBILE_TYPE_ALL)
    login_url = models.CharField(u'登录地址', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    logout_url = models.CharField(u'登出地址', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    is_heartbeat = models.PositiveSmallIntegerField(u'是否需要心跳', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    heartbeat_interval = models.CharField(u'心跳周期（秒）', max_length=10, blank=True, null=True)
    heartbeat_url = models.CharField(u'心跳地址', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    para = models.CharField(u'参数(json)', max_length=2000, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'mobile_service'
        verbose_name_plural = u'移动端服务定义表'
        verbose_name = u'移动端服务定义表'

    def __unicode__(self):
        return 'MobileService(%s)' % self.code



class SmsCode(models.Model):
    mobile = models.CharField(u"手机号", max_length=30)
    code = models.CharField(u"短信验证码", max_length=30, blank=True, null=True)
    timestamp = models.CharField(u"短信验证码生成时间戳", default="", max_length=30, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.IntegerField(u'是否删除', default=FALSE_INT, choices=((TRUE_INT, u"是"), (FALSE_INT, u"否")))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = "mobile_smscode"
        verbose_name = u'移动端验证码'
        verbose_name_plural = u'移动端验证码'

    def __unicode__(self):
        return 'SmsCode(%s:%s)' % (self.mobile, self.code)

