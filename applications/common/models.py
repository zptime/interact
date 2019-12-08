# -*- coding=utf-8 -*-

from django.db import models

from applications.user_center.models import *
from utils.constant import *
from utils.utils_db import ManagerFilterDelete


class SysImage(models.Model):
    image_name = models.CharField(u'名称', max_length=100, blank=True, null=True)
    image_size = models.CharField(u'大小', max_length=10, default='0')  # 字节
    image_square = models.CharField(u'长宽', max_length=30, default='0,0')  # width,length
    image_original_url = models.CharField(u'原始图片URL', max_length=DB_URL_LEN_LIMIT)
    image_thumb_url = models.CharField(u'缩略图片URL', max_length=DB_URL_LEN_LIMIT, blank=True, null=True) # 缩略图
    image_crop_url = models.CharField(u'正方形裁剪图片URL', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)  # 裁剪图
    image_type = models.CharField(u'图片类型', max_length=100, default='')
    account = models.ForeignKey(Account, verbose_name=u'上传用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'上传用户的类型', default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'上传用户的学校')
    is_protected = models.PositiveSmallIntegerField(u'是否受保护', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_common_image'
        verbose_name_plural = u'图片表'
        verbose_name = u'图片表'

    def __unicode__(self):
        return '%d: %s' % (self.id, self.image_name)


class SysVoice(models.Model):
    voice_name = models.CharField(u'名称', max_length=100, blank=True, null=True)
    voice_size = models.CharField(u'大小', max_length=10, default='0')  # 字节
    voice_duration = models.CharField(u'时长', max_length=8, default='0')  # 秒
    voice_url = models.CharField(u'语音URL', max_length=DB_URL_LEN_LIMIT)
    voice_type = models.CharField(u'语音类型', max_length=100, default='')
    voice_converted_url = models.CharField(u'转码后URL', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    voice_converted_status = models.PositiveSmallIntegerField(u'转码状态', \
        choices=((VOICE_CONVERT_STATUS_NONE, u'未转码'),
                 (VOICE_CONVERT_STATUS_ING, u'正在转码'),
                 (VOICE_CONVERT_STATUS_SUCC, u'转码成功'),
                 (VOICE_CONVERT_STATUS_FAIL, u'转码失败')))
    account = models.ForeignKey(Account, verbose_name=u'上传用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'上传用户的类型',default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'上传用户的学校')
    is_protected = models.PositiveSmallIntegerField(u'是否受保护', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_common_voice'
        verbose_name_plural = u'语音表'
        verbose_name = u'语音表'

    def __unicode__(self):
        return '%d: %s' % (self.id, self.voice_name)


class SysVideo(models.Model):
    video_name = models.CharField(u'名称', max_length=100, blank=True, null=True)
    video_size = models.CharField(u'大小', max_length=10, default='0')  # 字节
    video_duration = models.CharField(u'时长', max_length=10, default='0')  # 秒
    video_url = models.CharField(u'视频原始URL', max_length=DB_URL_LEN_LIMIT)
    video_converted_url = models.CharField(u'压缩转码后URL', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    video_converted_status = models.PositiveSmallIntegerField(u'压缩转码状态', \
        choices=((VIDEO_CONVERT_STATUS_NONE, u'未压缩转码'),
                 (VIDEO_CONVERT_STATUS_ING, u'正在压缩转码'),
                 (VIDEO_CONVERT_STATUS_SUCC, u'压缩转码成功'),
                 (VIDEO_CONVERT_STATUS_FAIL, u'压缩转码失败')))
    video_snapshot_url = models.CharField(u'截图封面URL', max_length=DB_URL_LEN_LIMIT, blank=True, null=True)
    video_snapshot_status = models.PositiveSmallIntegerField(u'截图状态', \
        choices=((VIDEO_SNAPSHOT_STATUS_NONE, u'未服务器截图'),
                 (VIDEO_SNAPSHOT_STATUS_ING, u'正在服务器截图'),
                 (VIDEO_SNAPSHOT_STATUS_SUCC, u'服务器截图成功'),
                 (VIDEO_SNAPSHOT_STATUS_FAIL, u'服务器截图失败')))
    video_square = models.CharField(u'视频长宽', max_length=30, default='0,0')  # width,length
    video_type = models.CharField(u'视频类型', max_length=100, default='')
    account = models.ForeignKey(Account, verbose_name=u'上传用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'上传用户的类型',default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'上传用户的学校')
    is_protected = models.PositiveSmallIntegerField(u'是否受保护', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_common_video'
        verbose_name_plural = u'视频表'
        verbose_name = u'视频表'

    def __unicode__(self):
        return '%d: %s' % (self.id, self.video_name)


class SysFile(models.Model):
    file_name = models.CharField(u'名称', max_length=100, default='', )
    file_size = models.CharField(u'大小', max_length=10, default='0')  # 字节
    file_url = models.CharField(u'文件URL', max_length=DB_URL_LEN_LIMIT)
    file_type = models.CharField(u'文件类型', max_length=100, default='')
    account = models.ForeignKey(Account, verbose_name=u'上传用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'上传用户的类型', default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'上传用户的学校')
    is_protected = models.PositiveSmallIntegerField(u'是否受保护', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_common_file'
        verbose_name_plural = u'文件表'
        verbose_name = u'文件表'

    def __unicode__(self):
        return '%d: %s' % (self.id, self.file_name)


class GlobalPara(models.Model):
    key = models.CharField(u'键', max_length=100, blank=True, null=True)
    value = models.CharField(u'值', max_length=5000, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_global'
        verbose_name_plural = u'全局参数定义表'
        verbose_name = u'全局参数定义表'

    def __unicode__(self):
        return '%s:%s' % (self.key, self.value)



