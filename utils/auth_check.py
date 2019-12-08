# -*- coding: utf-8 -*-

import logging
import types
from functools import wraps

from django.conf import settings
from applications import common
from applications.contacts.models import Group
from utils import net_helper
from utils.constant import *
from utils.errcode import *
from utils.net_helper import response405, response403, response200

from utils.tools import BusinessException, get_type_current_user
from applications.user_center.models import *


logger = logging.getLogger(__name__)


def validate(method, internal=False, authenticate=True,
        usertype=(USER_TYPE_STUDENT, USER_TYPE_TEACHER, USER_TYPE_PARENT), condition=None):
    """
        用户请求基本权限验证
    """
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            if request.method != method:
                return response405({'c': REQUEST_WRONG_METHOD[0], 'm': REQUEST_WRONG_METHOD[1]})

            if internal:
                if not net_helper.is_internal_request(request):
                    return response403({'c': REQUEST_INTERNAL[0], 'm': REQUEST_INTERNAL[1]})
            elif authenticate:
                if request.user.username == settings.DB_ADMIN:
                    return response403({'c': ROOT_FORBID[0], 'm': ROOT_FORBID[1]})
                if not request.user.is_authenticated():
                    return response200({'c': AUTH_NEED_LOGIN[0], 'm': AUTH_NEED_LOGIN[1]})
                
                # 检查用户是否存在
                if request.user.del_flag == TRUE_INT:
                    return response403({'c': USER_NOT_EXIST[0], 'm': USER_NOT_EXIST[1]})
                if request.user.school.del_flag == TRUE_INT:
                    return response403({'c': SCHOOl_NOT_EXIST[0], 'm': SCHOOl_NOT_EXIST[1]})
                if not get_type_current_user(request.user):
                    return response403({'c': USER_NOT_EXIST[0], 'm': USER_NOT_EXIST[1]})

                # 检查用户所在学校是否启用了该服务
                services_avai_count = request.user.school.schoolservice_set\
                    .filter(service__code__in=(settings.SYSTEM_NAME,),
                            del_flag=FALSE_INT,
                            service__del_flag=FALSE_INT,
                            school__del_flag=FALSE_INT)\
                    .count()
                if services_avai_count <= 0:
                    return response403({'c': AUTH_WRONG_SCHOOL[0], 'm': AUTH_WRONG_SCHOOL[1]})

                # 检查HTTP请求头，是否用户类型已经被PC端切换
                mobile_user_head = request.META.get('HTTP_'+settings.HTTP_HEADER_CURRENT_USER_TYPE, '')
                if mobile_user_head != '':  # 该请求头可选
                    mobile_user_type = mobile_user_head.split(',')[0]
                    mobile_school_id = mobile_user_head.split(',')[1]
                    user_info = common.services.get_my_info(request.user)
                    if user_info['user_type'] != mobile_user_type \
                        or user_info['school_id'] != mobile_school_id:
                        return response403({'c': AUTH_USER_TYPE_CRUSH[0], 'm': AUTH_USER_TYPE_CRUSH[1]})

                # 检查用户类型是否被允许
                request_user_type = request.user.type
                if request_user_type not in usertype:
                    return response403({'c': AUTH_WRONG_TYPE[0], 'm': AUTH_WRONG_TYPE[1]})
                elif isinstance(condition, types.FunctionType):
                    if not condition(request):
                        return response403({'c': AUTH_CONDITION_FAIL[0], 'm': AUTH_CONDITION_FAIL[1]})
            return func(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def is_in_same_school(user, school_id):
    """
        判断用户是否在该所学校
    """
    return user.school.id == int(school_id)


def check_get_account(account_id):
    if not account_id:
        raise BusinessException(USER_NOT_EXIST)
    account = Account.objects.filter(id=int(account_id), del_flag=FALSE_INT).first()
    if not account:
        raise BusinessException(USER_NOT_EXIST)
    return account


def check_get_school(school_id):
    if not school_id:
        raise BusinessException(SCHOOl_NOT_EXIST)
    school = School.objects.filter(id=int(school_id), del_flag=FALSE_INT).first()
    if not school:
        raise BusinessException(SCHOOl_NOT_EXIST)
    return school


def check_get_class(class_id):
    if not class_id:
        raise BusinessException(CLASS_NOT_EXIST)
    clazz = Class.objects.filter(id=int(class_id), del_flag=FALSE_INT).first()
    if not clazz:
        raise BusinessException(CLASS_NOT_EXIST)
    return clazz


def check_get_teacher(teacher_id):
    if not teacher_id:
        raise BusinessException(TEACHER_NOT_EXIST)
    teacher = Teacher.objects.filter(id=int(teacher_id), del_flag=FALSE_INT).first()
    if not teacher:
        raise BusinessException(TEACHER_NOT_EXIST)
    return teacher


def check_get_parent(parent_id):
    if not parent_id:
        raise BusinessException(PARENT_NOT_EXIST)
    parent = Parent.objects.filter(id=int(parent_id), del_flag=FALSE_INT).first()
    if not parent:
        raise BusinessException(PARENT_NOT_EXIST)
    return parent


def check_get_student(student_id):
    if not student_id:
        raise BusinessException(STUDENT_NOT_EXIST)
    student = Student.objects.filter(id=int(student_id), del_flag=FALSE_INT).first()
    if not student:
        raise BusinessException(STUDENT_NOT_EXIST)
    return student


def check_get_group(group_id):
    if not group_id:
        raise BusinessException(GROUP_NOT_EXIST)
    group = Group.objects.filter(id=int(group_id), is_del=FALSE_INT).first()
    if not group:
        raise BusinessException(GROUP_NOT_EXIST)
    return group


def assert_in_school(request_user, school):
    if request_user.school != school:
        raise BusinessException(AUTH_SAME_SCHOOL)