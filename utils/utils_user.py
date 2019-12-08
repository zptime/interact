# coding=utf8
from applications.user_center.models import Student, ParentStudent, Parent
from utils.constant import FALSE_INT, TRUE_INT


def student_qs(school=None, only_in=True, only_normal=False, only_not_graduate=True):
    qs = Student.objects.filter(del_flag=FALSE_INT)
    if only_in:
        qs = qs.filter(is_in=TRUE_INT)
    if school:
        qs = qs.filter(school=school)
    if only_normal:
        qs = qs.filter(kind=u'正常')
    if only_not_graduate:
        qs = qs.filter(cls__graduate_status=FALSE_INT)
    return qs


def parent_qs(school=None, only_active=True, only_with_child=True):
    relation = ParentStudent.objects.filter(del_flag=FALSE_INT)
    qs = Parent.objects.filter(del_flag=FALSE_INT)
    if school:
        qs = qs.filter(school=school)
    if only_active:
        qs = qs.filter(is_active=TRUE_INT)
    if only_with_child:
        qs = qs.filter(parentstudent__in=relation, parentstudent__status=APPLICATION_STATUS_APPROVED[0],
                       parentstudent__student__in=student_qs(school=school).all()).distinct()
    return qs