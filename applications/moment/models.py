# -*- coding=utf-8 -*-

from applications.common.models import SysVoice, SysImage, SysVideo, SysFile
from applications.user_center.models import *
from utils.constant import *
from utils.utils_db import ManagerFilterDelete


class MomentBase(models.Model):
    account = models.ForeignKey(Account, verbose_name=u'发互动用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'发互动用户的类型',default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'发互动用户的学校')
    user_name = models.CharField(u'姓名', max_length=30, blank=True, null=True, default='')
    content = models.TextField(u'互动文字', blank=True, null=True, default='')
    moment_type = models.PositiveSmallIntegerField(u'互动类型', default=MOMENT_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未定义'),
                             (MOMENT_TYPE_IMAGE, u'照片互动'),
                             (MOMENT_TYPE_VIDEO, u'视频互动'),
                             (MOMENT_TYPE_FILE, u'附件互动'),
                             (MOMENT_TYPE_VOTE, u'投票互动'),
                             (MOMENT_TYPE_MEDAL, u'奖章互动'),
                             (MOMENT_TYPE_DAYOFF, u'请假互动'),
                             (MOMENT_TYPE_EVALUATE, u'评价互动')))
    has_voice = models.PositiveSmallIntegerField(u'是否包含语音', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    has_image = models.PositiveSmallIntegerField(u'是否包含照片', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    has_video = models.PositiveSmallIntegerField(u'是否包含视频', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    has_file = models.PositiveSmallIntegerField(u'是否包含附件', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    append_attr = models.TextField(u'附加属性', blank=True, null=True, default='')  # 暂未使用
    read_count = models.PositiveIntegerField(u'被浏览次数', default=0)
    like_count = models.PositiveIntegerField(u'被点赞次数', default=0)
    reply_count = models.PositiveIntegerField(u'含评论个数', default=0)
    is_public = models.PositiveSmallIntegerField(u'是否公开', default=TRUE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment'
        verbose_name_plural = u'互动基础信息表'
        verbose_name = u'互动基础信息表'

    def __unicode__(self):
        return self.content[:20]


class MomentAttachVoice(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='voices', on_delete=models.PROTECT)
    voice = models.ForeignKey(SysVoice, verbose_name=u'语音', related_name='moments_attached', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_voice'
        verbose_name_plural = u'互动包含的语音表'
        verbose_name = u'互动包含的语音表'

    def __unicode__(self):
        return 'voice of moment [%s], id=%d' % (self.moment, self.id)


class MomentAttachImage(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='images', on_delete=models.PROTECT)
    image = models.ForeignKey(SysImage, verbose_name=u'图片', related_name='moments_attached', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_image'
        verbose_name_plural = u'互动包含的照片表'
        verbose_name = u'互动包含的照片表'

    def __unicode__(self):
        return 'image of moment [%s], id=%d' % (self.moment, self.id)


class MomentAttachVideo(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='videos', on_delete=models.PROTECT)
    video = models.ForeignKey(SysVideo, verbose_name=u'视频', related_name='moments_attached', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_video'
        verbose_name_plural = u'互动包含的视频表'
        verbose_name = u'互动包含的视频表'

    def __unicode__(self):
        return 'video of moment [%s], id=%d' % (self.moment, self.id)


class MomentAttachFile(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='files', on_delete=models.PROTECT)
    file = models.ForeignKey(SysFile, verbose_name=u'文件', related_name='moments_attached', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_file'
        verbose_name_plural = u'互动包含的附件表'
        verbose_name = u'互动包含的附件表'

    def __unicode__(self):
        return 'file of moment [%s], id=%d' % (self.moment, self.id)


class MomentVote(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='votes', on_delete=models.PROTECT)
    vote_title = models.CharField(u'投票主题', max_length=2000, default='')
    vote_num = models.PositiveSmallIntegerField(u'多选个数', default=1)  # 默认单选
    vote_deadline = models.DateTimeField(u'投票截止时间', blank=True, null=True)  # 为空表示无限期
    vote_statistics = models.IntegerField(u'投票次数统计', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_vote'
        verbose_name_plural = u'互动投票表'
        verbose_name = u'互动投票表'

    def __unicode__(self):
        return 'vote of moment [%s], title=%s, id=%d' % (self.moment, self.vote_title, self.id)


class MomentVoteItem(models.Model):
    vote = models.ForeignKey(MomentVote, verbose_name=u'投票对象', related_name='items', on_delete=models.PROTECT)
    branch = models.CharField(u'选择支', max_length=120, default='')
    sort = models.PositiveSmallIntegerField(u'选择支排序', default=100)
    count = models.PositiveIntegerField(u'被选择次数', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_vote_item'
        verbose_name_plural = u'投票选择支表'
        verbose_name = u'投票选择支表'

    def __unicode__(self):
        return self.branch


class MomentVoteUser(models.Model):
    account = models.ForeignKey(Account, verbose_name=u'投票用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'投票的用户当时的类型',default=USER_TYPE_NONE,
                    choices=((USER_TYPE_NONE, u'未设置'),
                             (USER_TYPE_STUDENT, u'学生'),
                             (USER_TYPE_TEACHER, u'教师'),
                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'投票用户的学校')
    vote_item = models.ForeignKey(MomentVoteItem, verbose_name=u'投票选择支', related_name='voter', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_vote_user'
        verbose_name_plural = u'用户投票表'
        verbose_name = u'用户投票表'

    def __unicode__(self):
        return 'account: %s, school: %s, type: %d select item [%s]' \
               % (self.account, self.user_school, self.user_type, self.vote_item)


class MomentEvaluate(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', on_delete=models.PROTECT)
    type = models.PositiveSmallIntegerField(u'评价类型', default=MOMENT_EVALUATE_ZAN,
                            choices=((MOMENT_EVALUATE_ZAN, u'表扬'), (MOMENT_EVALUATE_CAI, u'批评')))
    is_visible_for_parent_related = models.PositiveSmallIntegerField(u'仅相关家长可见', default=TRUE_INT,
                            choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_evaluate'
        verbose_name_plural = u'互动评价表'
        verbose_name = u'互动评价表'

    def __unicode__(self):
        return u'互动评价(%s)' % self.content


class MomentEvaluateStudent(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', on_delete=models.PROTECT)
    moment_evaluate = models.ForeignKey(MomentEvaluate, verbose_name=u'互动评价', on_delete=models.PROTECT)
    student = models.ForeignKey(Student, verbose_name=u'学生', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_evaluate_student'
        verbose_name_plural = u'互动评价学生表'
        verbose_name = u'互动评价学生表'

    def __unicode__(self):
        return u'互动评价学生(%s)' % self.student.full_name


class MomentDayoff(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', on_delete=models.PROTECT)
    is_visible_for_teacher = models.PositiveSmallIntegerField(u'仅教师可见', default=TRUE_INT,
                            choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_dayoff'
        verbose_name_plural = u'互动请假表'
        verbose_name = u'互动请假表'

    def __unicode__(self):
        return u'互动请假(%s)' % self.content


class MomentLike(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='lovers', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'点赞用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'点赞用户的类型', default=USER_TYPE_NONE,
                                    choices=((USER_TYPE_NONE, u'未设置'),
                                             (USER_TYPE_STUDENT, u'学生'),
                                             (USER_TYPE_TEACHER, u'教师'),
                                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'点赞用户的学校')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_like'
        verbose_name_plural = u'点赞表'
        verbose_name = u'点赞表'

    def __unicode__(self):
        return 'account: %s, school: %s, type: %d love moment [%s]' \
               % (self.account, self.user_school, self.user_type, self.moment)


class MomentRead(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='readers', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'浏览用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'浏览用户的类型', default=USER_TYPE_NONE,
                                    choices=((USER_TYPE_NONE, u'未设置'),
                                             (USER_TYPE_STUDENT, u'学生'),
                                             (USER_TYPE_TEACHER, u'教师'),
                                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'浏览用户的学校')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_read'
        verbose_name_plural = u'浏览表'
        verbose_name = u'浏览表'

    def __unicode__(self):
        return 'account: %s, school: %s, type: %d read moment [%s]' \
               % (self.account, self.user_school, self.user_type, self.moment)


class MomentReply(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'被评论的互动', related_name='replyers', on_delete=models.PROTECT)
    account = models.ForeignKey(Account, verbose_name=u'评论用户', on_delete=models.PROTECT)
    user_type = models.PositiveSmallIntegerField(u'评论用户的类型', default=USER_TYPE_NONE,
                                    choices=((USER_TYPE_NONE, u'未设置'),
                                             (USER_TYPE_STUDENT, u'学生'),
                                             (USER_TYPE_TEACHER, u'教师'),
                                             (USER_TYPE_PARENT, u'家长')))
    user_school = models.ForeignKey(School, verbose_name=u'评论用户的学校')
    ref = models.ForeignKey('self', verbose_name=u'被回复的评论', blank=True, null=True)   # 递归外键引用
    content = models.CharField(u'评论内容', max_length=2000, default='')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_reply'
        verbose_name_plural = u'评论表'
        verbose_name = u'评论表'

    def __unicode__(self):
        return 'account: %s, school: %s, type: %d reply moment [%s]' \
               % (self.account, self.user_school, self.user_type, self.moment)


class MomentCircleSchool(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='schoolcircle', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_circle_school'
        verbose_name_plural = u'分享到学校圈表'
        verbose_name = u'分享到学校圈表'

    def __unicode__(self):
        return self.moment


class MomentCircleClass(models.Model):
    moment = models.ForeignKey(MomentBase, verbose_name=u'互动基础对象', related_name='classcircle', on_delete=models.PROTECT)
    clazz = models.ForeignKey(Class, verbose_name=u'分享到的班级', related_name='classcircle', on_delete=models.PROTECT)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间', auto_now=True)
    is_del = models.PositiveSmallIntegerField(u'删除否', default=FALSE_INT, choices=((TRUE_INT, u'是'), (FALSE_INT, u'否')))

    objects = ManagerFilterDelete()
    builtin = models.Manager()

    class Meta:
        db_table = 'interact_moment_circle_class'
        verbose_name_plural = u'分享到班级圈表'
        verbose_name = u'分享到班级圈表'

    def __unicode__(self):
        return self.moment






