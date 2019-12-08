# -*- coding=utf-8 -*-

from django.db import models

from utils.constant import *
from utils.utils_db import ManagerFilterDelete
from applications.common.models import SysFile, SysVoice
from applications.user_center.models import Student, Account, School


class NotifyBase(models.Model):
    account = models.ForeignKey(Account, verbose_name=u'发通知的用户', related_name='notify', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'发通知用户类型', default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'发通知用户的学校', related_name='notify', on_delete=models.PROTECT)
    title = models.CharField(u'通知标题', max_length=200, default='')
    intro = models.CharField(u'通知摘要', max_length=300, default='')
    content = models.TextField(u'通知正文', blank=True, null=True, default='')
    type = models.PositiveSmallIntegerField(u'通知类型', default=NOTIFICATION_CLASS,
                    choices=((NOTIFICATION_CLASS, u'班级通知'),
                             (NOTIFICATION_HOMEWORK, u'作业通知'),))
    scope = models.PositiveSmallIntegerField(u'通知范围', default=NOTIFICATION_SCOPE_1,
                    choices=((NOTIFICATION_SCOPE_1, u'通知学生，仅家长可读'),
                             (NOTIFICATION_SCOPE_2, u'通知学生，学生和家长可读'),))
    remind_count = models.PositiveSmallIntegerField(u'提醒次数', default=1)
    has_voice = models.PositiveSmallIntegerField(u'是否包含语音', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    has_image = models.PositiveSmallIntegerField(u'是否包含照片', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    has_video = models.PositiveSmallIntegerField(u'是否包含视频', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    has_file = models.PositiveSmallIntegerField(u'是否包含附件', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'通知发送时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_notify'
        verbose_name_plural = u'通知基本信息表'
        verbose_name = u'通知基本信息表'

    def __unicode__(self):
        return u'通知(%s)' % self.id


class NotifyAttachFile(models.Model):
    notify = models.ForeignKey(NotifyBase, verbose_name=u'通知基本对象', related_name='files', on_delete=models.PROTECT)
    file = models.ForeignKey(SysFile, verbose_name=u'通知包含的文件', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_notify_file'
        verbose_name_plural = u'通知附件表'
        verbose_name = u'通知附件表'

    def __unicode__(self):
        return u'通知附件(%s)' % self.file.id


class NotifyAttachVoice(models.Model):
    notify = models.ForeignKey(NotifyBase, verbose_name=u'通知基本对象', related_name='voices', on_delete=models.PROTECT)
    voice = models.ForeignKey(SysVoice, verbose_name=u'通知包含的语音', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_notify_voice'
        verbose_name_plural = u'通知语音表'
        verbose_name = u'通知语音表'

    def __unicode__(self):
        return u'通知语音(%s)' % self.voice.id


class NotifyUserStudent(models.Model):
    notify = models.ForeignKey(NotifyBase, verbose_name=u'通知基本对象', on_delete=models.PROTECT)
    student = models.ForeignKey(Student, verbose_name=u'学生', on_delete=models.PROTECT)
    is_read = models.PositiveSmallIntegerField(u'是否已读', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_notify_user_student'
        verbose_name_plural = u'通知学生表'
        verbose_name = u'通知学生表'

    def __unicode__(self):
        return u'通知学生(%s, %s)' % (self.notify.id, self.student.full_name)


