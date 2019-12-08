# -*- coding=utf-8 -*-

from applications.user_center.models import *
from utils.constant import *
from utils.utils_db import ManagerFilterDelete


class Group(models.Model):
    name = models.CharField(u'名称', max_length=20)  # 可以重复，不能为空
    school = models.ForeignKey(School, verbose_name=u'所在学校', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'创建者', related_name='groups_created', on_delete=models.PROTECT)  # 只有自定义群组有创建者
    user_type = models.PositiveSmallIntegerField(u'创建者类型', default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_contacts_group'
        verbose_name_plural = u'群组表'
        verbose_name = u'群组表'

    def __unicode__(self):
        return u'群组(%s)' % self.name


class GroupMember(models.Model):
    group = models.ForeignKey(Group, verbose_name=u'群组', related_name='members', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'群组成员账号', related_name='members', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'群组成员类型',default=USER_TYPE_STUDENT,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    school = models.ForeignKey(School, verbose_name=u'群组成员所在学校', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_contacts_group_member'
        verbose_name_plural = u'群组成员表'
        verbose_name = u'群组成员表'

    def __unicode__(self):
        return u'群组成员(%s)' % self.account



