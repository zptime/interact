# -*- coding=utf-8 -*-

import imp
import logging
import os
import random
import re
import shutil
import datetime

import requests
from PIL import Image
from urlparse import urljoin
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import F
from django.http import StreamingHttpResponse, Http404

from applications.user_center.agents import call_api_with_para
from applications.user_center.utils_realtime import get_password
from utils import file_storage
from utils import net_helper
from utils import s3_storage
from utils import tools
from utils import type_helper
from utils.constant import *
from applications.common.models import *
from utils.errcode import *
from utils.file_storage import safe_filename_4_shell, safe_folder, safe_delete
from utils.remote_call import remote_request, get_usercenter_address
from utils.s3_storage import ObjectStorage
from utils.tools import BusinessException, record_time, get_type_current_user
from utils.wx import fetch

logger = logging.getLogger(__name__)


def check_get_file(file_id):
    if not file_id:
        raise BusinessException(FILE_NOT_EXIST)
    file_obj = SysFile.objects.filter(id=int(file_id)).first()
    if not file_obj:
        raise BusinessException(FILE_NOT_EXIST)
    return file_obj


def check_get_voice(voice_id):
    if not voice_id:
        raise BusinessException(VOICE_NOT_EXIST)
    voice_obj = SysVoice.objects.filter(id=int(voice_id)).first()
    if not voice_obj:
        raise BusinessException(VOICE_NOT_EXIST)
    return voice_obj


def is_parent(role_obj):
    return isinstance(role_obj, Parent)


def is_student(role_obj):
    return isinstance(role_obj, Student)


def is_teacher(role_obj):
    return isinstance(role_obj, Teacher)


def get_user_info(account_id, usertype_id, school_id):
    account = Account.objects.filter(pk=account_id).select_related().first()
    if not account:
        raise tools.BusinessException(USER_NOT_EXIST)
    role = tools.get_type_user(int(account_id), int(usertype_id), int(school_id))
    if not role:
        raise tools.BusinessException(USERTYPE_NOT_EXIST)
    classes = get_classes_by_role(role, verbose=False)

    user_info = {
        'name': role.full_name,
        'account_id': str(account_id),
        'user_type_id': str(usertype_id),
        'phone': account.mobile,
        'avatar': get_uc_static_file_path(role.image_url),
        'sex': role.sex,
        'role_id': str(role.id),
        'school': {
            'school_id': str(account.school.id),
            'school_name': account.school.name_full,
        },
        'is_privileged': TRUE_STR,
        'is_privileged_desc': '',
        'clazz': [],
        'family': [],
    }
    for each_class in classes:
        user_info['clazz'].append({
            'class_id': each_class['class_id'],
            'class_name': each_class['class_name'],
        })

    if is_teacher(role):
        if not role.is_in:
            user_info['is_privileged'] = FALSE_STR
            user_info['is_privileged_desc'] = u'您（教师）已经不在校，您无法继续使用本系统'

    if is_parent(role):
        all_children_not_in = True
        children = get_children(role)
        for child in children:
            user_info['family'].append({
                'account_id': str(child.account.id),
                'user_type_id': str(USER_TYPE_STUDENT),
                'school_id': str(child.school.id),
                'username': child.full_name,
                'class_name': child.cls.class_name if child.cls else '',
                'avatar': get_uc_static_file_path(child.image_url),
            })
            if child.is_in == TRUE_INT and child.cls.graduate_status == FALSE_INT:
                all_children_not_in = False
        if all_children_not_in:
            user_info['is_privileged'] = FALSE_STR
            user_info['is_privileged_desc'] = u'您（家长）的孩子均已毕业或不在校，您无法继续使用本系统'

    if is_student(role):
        if role.is_in == FALSE_INT:
            user_info['is_privileged'] = FALSE_STR
            user_info['is_privileged_desc'] = u'您（学生）已经不在校，您无法继续使用本系统'
        if role.cls.graduate_status == TRUE_INT:
            user_info['is_privileged'] = FALSE_STR
            user_info['is_privileged_desc'] = u'您（学生）已经毕业，您无法继续使用本系统'

        parents = get_parents(role)
        for parent in parents:
            user_info['family'].append({
                'account_id': str(parent.account.id),
                'user_type_id': str(USER_TYPE_PARENT),
                'school_id': str(parent.school.id),
                'username': parent.full_name,
                'class_name': '',
                'avatar': get_uc_static_file_path(parent.image_url),
            })
    return user_info


def get_my_info(user):
    return get_user_info(user.id, user.type, user.school.id)


def get_student_simple_info(request, account_id_para, user_type_id_para, school_id_para):
    account_id = int(account_id_para) if account_id_para else int(request.user.id)
    user_type_id = int(user_type_id_para) if account_id_para else int(request.user.type)
    school_id = int(school_id_para) if account_id_para else int(request.user.school.id)

    account = Account.objects.filter(pk=account_id).select_related().first()
    if not account:
        raise tools.BusinessException(USER_NOT_EXIST)
    role = tools.get_type_user(int(account_id), int(user_type_id), int(school_id))
    if not role:
        raise tools.BusinessException(USERTYPE_NOT_EXIST)
    if int(user_type_id) != USER_TYPE_STUDENT:
        raise tools.BusinessException(NOT_STUDENT)
    return {
        'stu_name': role.full_name,
        'stu_id': str(role.id),
        'clazz_id': role.cls.id if role.cls else '',
        'clazz_name': role.cls.class_name if role.cls else ''
    }


def get_class_member(
        clazz, flat=False, exclude_teacher=False, exclude_parent=False, exclude_student=False):
    """
        获取班级中所有成员：老师/家长/学生
    """
    hierarchical_list = list()
    flat_list = list()
    # 获取老师
    if not exclude_teacher:
        teach_rela = clazz.teacherclass_set.filter(del_flag=FALSE_INT, teacher__del_flag=FALSE_INT)
        for each_teach_rela in teach_rela:
            teacher = each_teach_rela.teacher
            teacher_info = {
                'account_id': str(teacher.account.id),
                'user_type_id': str(USER_TYPE_TEACHER),
                'school_id': str(teacher.school.id),
                'username': teacher.full_name,
                'avatar': get_uc_static_file_path(teacher.image_url),
                'chat_id': '',
                'desc': get_user_desc(teacher),
            }
            hierarchical_list.append(teacher_info)
            flat_list.append(teacher_info)

    # 获取学生
    students = clazz.student_set.filter(del_flag=FALSE_INT)
    for stu in students:
        stu_info = {
            'account_id': str(stu.account.id),
            'user_type_id': str(USER_TYPE_STUDENT),
            'school_id': str(stu.school.id),
            'username': stu.full_name,
            'avatar': get_uc_static_file_path(stu.image_url),
            'chat_id': '',
            'desc': get_user_desc(stu),
        }
        if not exclude_student:
            flat_list.append(stu_info)

        # 获取学生的所有家长
        if not flat:
            stu_info['stu_relate_parent'] = []
        p_s_rela = stu.parent_stu_relation.filter(del_flag=FALSE_INT, parent__del_flag=FALSE_INT)
        for each_p_s in p_s_rela:
            parent = each_p_s.parent
            parent_info = {
                'account_id': str(parent.account.id),
                'user_type_id': str(USER_TYPE_PARENT),
                'school_id': str(parent.school.id),
                'username': parent.full_name,
                'avatar': get_uc_static_file_path(parent.image_url),
                'chat_id': '',
                'desc': get_user_desc(parent),
            }
            if not exclude_parent:
                flat_list.append(parent_info)
                if not flat:
                    stu_info['stu_relate_parent'].append(parent_info)
        if not exclude_student:
            hierarchical_list.append(stu_info)
    if flat:
        # 平行结构时，合并不同学生相同家长的数据
        flat_list = tools.remove_dup_in_dictlist(flat_list, ['account_id', 'user_type_id', 'school_id'])
    return flat_list if flat else hierarchical_list


def get_parent_desc(stu_list):
    safe_stu_list = [each for each in stu_list if each.cls]
    if len(safe_stu_list) <= 0:
        return u'家长'
    desc = reduce(lambda x, y: x+','+y, [stu.cls.class_name+stu.full_name for stu in safe_stu_list if stu.cls])
    return u'%s的家长' % desc


def get_student_desc(stu):
    if stu.cls:
        return stu.cls.class_name
    else:
        return ''


def get_teacher_desc():
    return USER_TYPE_MAP[USER_TYPE_TEACHER]


def get_user_desc(role_obj):
    """
        获取一个用户的描述信息
    """
    if is_teacher(role_obj):
        return get_teacher_desc()
    if is_student(role_obj):
        return get_student_desc(role_obj)
    if is_parent(role_obj):
        p_s_rela_qs = role_obj.parentstudent_set.filter(del_flag=FALSE_INT, student__del_flag=FALSE_INT)
        stu_list = [p_s_rela.student for p_s_rela in p_s_rela_qs]
        return get_parent_desc(stu_list)


def get_parents(student):
    """
        通过孩子找家长
    """
    result_parents = list()
    parent_relation = student.parent_stu_relation.filter(
        del_flag=FALSE_INT, parent__del_flag=FALSE_INT).only('parent')
    for each_rela in parent_relation:
        result_parents.append(each_rela.parent)
    return result_parents


def get_children(parent):
    """
        通过家长找孩子（仅查询本校的孩子）
    """
    result_children = list()
    my_children_rela = parent.parentstudent_set.filter(
        student__school=parent.school, del_flag=FALSE_INT, student__del_flag=FALSE_INT).only('student')
    for each_rela in my_children_rela:
        result_children.append(each_rela.student)
    return result_children


def get_class_simple_info(clazz, me_teacher=None):
    """
        获取一个班的基本信息
        'is_mentors' 仅针对老师有效
    """
    mentors = clazz.teacher_set.filter(del_flag=FALSE_INT)
    is_mentor = False
    if me_teacher:
        is_mentor = me_teacher in mentors
    return {
        'class_id': str(clazz.id),
        'class_name': clazz.class_name,
        'is_mentor': type_helper.bool2str(is_mentor),
    }


def get_class_info(clazz, me_teacher=None):
    """
        获取一个班的详情
    """
    # 获取老师总人数
    teacher_count = len(get_teacher_by_class(clazz))
    # 获取学生总人数
    students_qs = clazz.student_set.filter(del_flag=FALSE_INT)
    student_count = students_qs.count()
    # 获取家长总人数
    parent_count = 0
    for each_stu in students_qs:
        parent_count += each_stu.parent_stu_relation.filter(del_flag=FALSE_INT, parent__del_flag=FALSE_INT).count()

    # 获取班主任列表
    mento_list = list()
    mentors = clazz.teacher_set.filter(del_flag=FALSE_INT)
    for each_mentor in mentors:
        mento_list.append({
            'account_id': str(each_mentor.account.id),
            'user_type_id': str(USER_TYPE_TEACHER),
            'school_id': str(each_mentor.school.id),
            'username': each_mentor.full_name,
        })
    return {
        'class_id': str(clazz.id),
        'class_name': clazz.class_name,
        'student_count': str(student_count),
        'teacher_count': str(teacher_count),
        'parent_count': str(parent_count),
        'mentors': mento_list,
        'is_mentor': type_helper.bool2str(me_teacher in mentors if me_teacher else False),
    }


def get_classes_by_role(role, verbose=True):
    result_list = list()
    if is_teacher(role):
        all_teach_class_obj = get_class_by_teacher(role.id)
        for each_teach_class in all_teach_class_obj:
            if not verbose:
                result_list.append(get_class_simple_info(each_teach_class.cls, role))
            else:
                result_list.append(get_class_info(each_teach_class.cls, role))

    if is_parent(role):
        my_children_rela = role.parentstudent_set.filter(  # 获取孩子信息仅查询本校的
            student__school=role.school, del_flag=FALSE_INT, student__del_flag=FALSE_INT)
        children_classes = list()
        # 获取家长的各个子女信息
        for each_rela in my_children_rela:
            if each_rela.student.cls:
                children_classes.append(each_rela.student.cls)
        children_classes = set(children_classes)
        for each_class in children_classes:
            if not verbose:
                result_list.append(get_class_simple_info(each_class))
            else:
                result_list.append(get_class_info(each_class))
    if is_student(role):
        if role.cls:
            if not verbose:
                result_list.append(get_class_simple_info(role.cls))
            else:
                result_list.append(get_class_info(role.cls))

    # 按照班级名称排序
    result_list = tools.sort_list_by_dict_key(result_list, 'class_name')
    return result_list


def get_classes_by_account(user, verbose=True):
    """
        获取我所在的所有班级:
        老师：获取所有任课班级
        学生：获取就读的班级（唯一一个）
        家长：获取各个孩子所在的班级（可能多个）
    """
    role = tools.get_type_current_user(user)
    if not role:
        raise BusinessException(USER_NOT_EXIST)
    return get_classes_by_role(role, verbose=verbose)


def get_classes_by_turple(account_id, user_type, school_id, verbose=False):
    role = tools.get_type_user(int(account_id), int(user_type), int(school_id))
    if not role:
        raise BusinessException(USER_NOT_EXIST)
    return get_classes_by_role(role, verbose=verbose)


def get_classes_in_school(school):
    """
        获取学校中的所有班级
    """
    classes = school.class_set.filter(del_flag=FALSE_INT, graduate_status=FALSE_INT)
    result = list()
    grade_dict = {}
    for clazz in classes:
        if clazz.grade_name not in grade_dict:
            grade_dict[clazz.grade_name] = []
        grade_dict[clazz.grade_name].append({
            'class_id': clazz.id,
            'class_name': clazz.class_name
        })
    for grade_name, grade_class in grade_dict.items():
        result.append({
            'grade_name': grade_name,
            'classes': grade_class
        })
    return tools.sort_list_by_dict_key(result, 'grade_name', mode=3)


# def get_class_by_teacher_usercenter(teacher_id):
#     """
#         获取一个老师所带的所有班级 （从用户中心实时获取）
#     """
#     from applications.user_center.utils_realtime import get_clazz_id_by_teacher
#     result = list()
#     if not Teacher.objects.filter(id=int(teacher_id), del_flag=FALSE_INT).exists():
#         raise Exception()
#     clazzes = get_clazz_id_by_teacher(teacher_id)
#     for each_clazz in clazzes:
#         clazz = Class.objects.filter(del_flag=FALSE_INT, id=int(each_clazz['clazz_id']), graduate_status=FALSE_INT).first()
#         if clazz:
#             result.append({
#                 'class_id': str(clazz.id),
#                 'class_name': clazz.class_name,
#                 'is_mentor': str(each_clazz['is_mentor'])
#             })
#     return result


# def get_class_by_teacher(teacher_id, from_uc=False):
#     if from_uc:
#         return get_class_by_teacher_usercenter(teacher_id)
#     else:
#         qs = TeacherClass.objects.filter(teacher__id=int(teacher_id), del_flag=FALSE_INT)
#         result = list()
#         for each in qs:
#             result.append({
#                 'class_id': str(each.cls.id),
#                 'class_name': each.cls.class_name,
#                 'is_mentor': str(each.is_master),
#             })
#         return result


def get_class_by_teacher(teacher_id):
    qs = TeacherClass.objects.select_related().filter(teacher__id=int(teacher_id), del_flag=FALSE_INT)
    return list(qs)


# def get_teacher_by_class(clazz):
#     """
#         获取一个班级的所有老师 （从本地数据库读取）
#     """
#     teachers = list()
#     teach_relation = clazz.teacherclass_set.filter(del_flag=FALSE_INT, teacher__del_flag=FALSE_INT)
#     for each_teach_relation in teach_relation:
#         teachers.append({
#             'school_id': str(each_teach_relation.teacher.school.id),
#             'teacher_id': str(each_teach_relation.teacher.id),
#             'account_id': str(each_teach_relation.teacher.account.id),
#             'teacher_name': each_teach_relation.teacher.full_name,
#             'is_mentor': str(each_teach_relation.is_master)
#         })
#     return teachers


def get_teacher_by_class(clazz):
    """
        获取一个班级的所有老师 （从本地数据库读取）
    """
    teachers = list()
    qs = clazz.teacherclass_set.filter(del_flag=FALSE_INT, teacher__del_flag=FALSE_INT)
    for each_teach_relation in qs:
        teachers.append(each_teach_relation.teacher)
    return teachers


def add_teach_relation(teacher, classes):
    class_id_list = [each.id for each in classes]
    param_dict = {
        'class_id_list': json.dumps(class_id_list, ensure_ascii=False),
    }
    logger.info('add teacher_class relation to user_center ...')
    logger.info(param_dict)
    remote_rslt = call_api_with_para(teacher.account.id, 'api_add_teacher_class', param_dict)
    logger.info(remote_rslt)
    result_code = json.loads(remote_rslt)['c']
    if result_code != 0:
        raise BusinessException(ADD_TEACHCLASS_UC_FAIL)


def delete_teach_relation(teacher, classes):
    class_id_list = [each.id for each in classes if teacher.cls != each]
    param_dict = {
        'class_id_list': json.dumps(class_id_list, ensure_ascii=False),
    }
    logger.info('delete teacher_class relation to user_center ...')
    logger.info(param_dict)
    remote_rslt = call_api_with_para(teacher.account.id, 'api_delete_teacher_class', param_dict)
    logger.info(remote_rslt)
    result_code = json.loads(remote_rslt)['c']
    if result_code != 0:
        raise BusinessException(DEL_TEACHCLASS_UC_FAIL)


def upload_file(file, user, is_secure, file_name=''):
    """
        上传一个附件，保存在本地或者S3存储
    """
    fname = file_name or file.name

    # 存储安全路径还是公开路径
    media_path = settings.MEDIA_PATH_PROTECT if is_secure == TRUE_STR else settings.MEDIA_PATH_PUBLIC

    # 生成全局唯一文件名
    unique_file_name = file_storage.filename_unique(fname)

    # 文件保存相对路径： media/{public|proteced}/file/{school_code}/{filename}_{uuid1}.{ext}
    relative_path = file_storage.gen_path(
        os.path.join(media_path, user.school.code, 'file'), unique_file_name)

    if settings.USE_S3:
        raw_md5 = s3_storage.get_operator().upload_file_obj(file, relative_path)
    else:
        file_storage.save_file(file, os.path.join(settings.BASE_DIR, relative_path))

    sys_file = SysFile()
    sys_file.file_name = fname
    sys_file.file_size = str(file.size)
    sys_file.file_url = relative_path
    sys_file.file_type = (fname[fname.rfind('.')+1:]).lower()
    sys_file.account = user
    sys_file.user_type = user.type
    sys_file.user_school = user.school
    sys_file.is_protected = int(is_secure)
    sys_file.save()

    return_json = {
        'file_id': str(sys_file.id),
        'file_url': tools.gen_url_with_fname(
            os.path.join(get_current_sys_domain(), sys_file.file_url),
            fname
        ),
        'file_size': str(file.size),
        'file_name': sys_file.file_name,
    }
    return return_json


def upload_video(video_file, video_duration, video_width, video_height, video_cover_image, user, is_secure):
    """
        上传一个视频，保存在本地或者S3存储，并生成形如如下地址：
    """
    # 存储安全路径还是公开路径
    media_path = settings.MEDIA_PATH_PROTECT if is_secure == TRUE_STR else settings.MEDIA_PATH_PUBLIC

    name = safe_filename_4_shell(video_file.name)

    # 生成全局唯一文件名
    unique_file_name = file_storage.filename_unique(name)

    # 文件保存相对路径： media/{public|proteced}/video/{school_code}/{filename}_{uuid1}.{ext}
    relative_path = file_storage.gen_path(
        os.path.join(media_path, user.school.code, 'video'), unique_file_name)

    if settings.USE_S3:
        logger.info('uploading video %s to s3 ...' % name)
        raw_md5 = s3_storage.get_operator().upload_file_obj(video_file, relative_path)
        logger.info('upload video %s to s3 successfully' % name)
    else:
        logger.info('saving video %s to local ...' % name)
        file_storage.save_file(video_file, os.path.join(settings.BASE_DIR, relative_path))
        logger.info('save video %s to local successfully' % name)

    # 视频后缀
    ext = (name[name.rfind('.')+1:]).lower()

    video_obj = SysVideo()

    # 如果包含视频封面，则保存
    relative_cover_path = ''
    if video_cover_image:
        # 生成全局唯一文件名
        unique_cover_name = file_storage.filename_unique(video_cover_image.name)

        # 文件保存相对路径： media/{public|proteced}/video_snap/{school_code}/{filename}_{uuid1}.{ext}
        relative_cover_path = file_storage.gen_path(
            os.path.join(media_path, user.school.code, 'video_snapshot'), unique_cover_name)
        if settings.USE_S3:
            raw_md5 = s3_storage.get_operator().upload_file_obj(video_cover_image, relative_cover_path)
        else:
            file_storage.save_file(video_cover_image, os.path.join(settings.BASE_DIR, relative_cover_path))
        video_obj.video_snapshot_status = VIDEO_SNAPSHOT_STATUS_NONE
        video_obj.video_snapshot_url = relative_cover_path
    else:
        video_obj.video_snapshot_status = VIDEO_SNAPSHOT_STATUS_NONE
        video_obj.video_snapshot_url = None

    video_obj.video_name = name
    video_obj.video_size = str(video_file.size)
    video_obj.video_duration = video_duration
    video_obj.video_url = relative_path
    video_obj.video_converted_url = relative_path
    video_obj.video_converted_status = VIDEO_CONVERT_STATUS_NONE
    video_obj.video_type = ext
    video_obj.video_square = '%s,%s' % (str(video_width), str(video_height))
    video_obj.account = user
    video_obj.user_type = user.type
    video_obj.user_school = user.school
    video_obj.is_protected = int(is_secure)
    video_obj.save()

    # mov格式需要异步转码
    # if ext == 'mov' and settings.IS_AUTO_CONVERT_MOV_TO_MP4:
    #     from applications.common.tasks import convert_mov
    #     try:
    #         if settings.USE_ASYNC:
    #             convert_mov.delay(video_obj.id)
    #         else:
    #             convert_mov(video_obj.id)
    #     except Exception as e:
    #         logger.exception('convert video occur exception')

    # 是否自动压缩&转码文件
    if settings.IS_AUTO_CONVERT_AND_COMPRESS_MP4:
        from applications.common.tasks import convert
        try:
            if settings.USE_ASYNC:
                convert.delay(video_obj.id)
            else:
                convert(video_obj.id)
        except Exception as e:
            logger.exception('convert and compress occur exception')

    # 没有截图的视频需要异步截图
    # if not video_cover_image and settings.IS_AUTO_SNAPSHOT:
    #     from applications.common.tasks import snapshot
    #     try:
    #         if settings.USE_ASYNC:
    #             snapshot.delay(video_obj.id)
    #         else:
    #             snapshot(video_obj.id)
    #     except Exception as e:
    #         logger.exception('snapshot video occur exception')

    return_json = {
        'video_id': str(video_obj.id),
        'video_name': name,
        'video_size': str(video_file.size),
        'video_duration': type_helper.not_null_string(video_duration),
        'video_width': str(video_width),
        'video_height': str(video_height),
        'video_url': os.path.join(get_current_sys_domain(), video_obj.video_url),
        'video_cover_url': os.path.join(get_current_sys_domain(), relative_cover_path)
    }
    return return_json


def upload_voice(voice_file, duration, user, is_secure):
    """
        上传一个语音，保存在本地或者S3存储，并生成形如如下地址
    """
    # 存储安全路径还是公开路径
    media_path = settings.MEDIA_PATH_PROTECT if is_secure == TRUE_STR else settings.MEDIA_PATH_PUBLIC

    name = safe_filename_4_shell(voice_file.name)

    # 生成全局唯一文件名
    unique_file_name = file_storage.filename_unique(name)

    # 文件保存相对路径： media/{public|proteced}/voice/{school_code}/{filename}_{uuid1}.{ext}
    relative_path = file_storage.gen_path(
        os.path.join(media_path, user.school.code, 'voice'), unique_file_name)

    if settings.USE_S3:
        logger.info('uploading voice %s to s3, using PATH %s' % (voice_file.name, relative_path))
        raw_md5 = s3_storage.get_operator().upload_file_obj(voice_file, relative_path)
    else:
        file_storage.save_file(voice_file, os.path.join(settings.BASE_DIR, relative_path))

    ext = (name[name.rfind('.') + 1:]).lower()

    voice = SysVoice()
    voice.voice_name = name
    voice.voice_size = str(voice_file.size)
    voice.voice_duration = duration
    voice.voice_url = relative_path
    voice.voice_converted_url = relative_path
    voice.voice_type = ext
    voice.account = user
    voice.user_type = user.type
    voice.user_school = user.school
    voice.is_protected = int(is_secure)
    voice.voice_converted_status = VOICE_CONVERT_STATUS_NONE
    voice.save()

    # 异步转码
    if (ext == 'wav' or ext == 'amr') and settings.IS_AUTO_CONVERT_MOV_TO_MP3:
        from applications.common.tasks import convert_voice
        try:
            if settings.USE_ASYNC:
                convert_voice.delay(voice.id)
            else:
                convert_voice(voice.id)
        except Exception as e:
            logger.exception('convert voice occur exception')

    return_json = {
        'voice_id': str(voice.id),
        'voice_name': name,
        'voice_size': str(voice_file.size),
        'voice_duration': type_helper.not_null_string(duration),
        'voice_url': os.path.join(get_current_sys_domain(), voice.voice_url)
    }
    return return_json


def wx_voice_fetch(request, media_id, duration, access_token):
    voice_response = fetch(request.user, media_id, token=access_token)
    #HEAD:Content-disposition    attachment; filename="DTsH2SDUkNn12liTv53OuSXVhZ10yrWhwaPj4WlHJdqCBorq6U4-e4QefeA23Qr0.amr"
    pattern = r'attachment; filename="(.+)"'
    header_fname = voice_response.headers['Content-disposition']
    fname = re.findall(pattern, header_fname)[0]
    tmp_path = os.path.join(settings.TEMP_DIR, fname)
    with open(tmp_path, "wb") as tmp_f:
        for chunk in voice_response.iter_content(chunk_size=512):
            if chunk:
                tmp_f.write(chunk)
    response = trigger_upload_voice_request(request, fname, tmp_path, duration)
    status_code = response.status_code
    if status_code != 200:
        raise BusinessException(WX_UPLOAD_VOICE_FAIL)
    else:
        safe_delete(tmp_path)
    return response.text


def trigger_upload_voice_request(request, fname, file_path, duration):
    fname = 'wx_voice' + fname[fname.rfind('.'):]
    files = {
      "voice": (fname, open(file_path, "rb")),
    }
    upload_request_path = urljoin(domain_this_internal(), 'api/common/upload/voice')
    logger.info('visit local-server %s to upload wx-voice' % upload_request_path)
    response = requests.post(
        upload_request_path,
        cookies=request.COOKIES,
        data={'duration': str(duration)},
        files=files,
        timeout=30)
    return response


def _save_local_tmp_image(tmp_path, relative_path):
    if settings.USE_S3:
        if os.path.exists(tmp_path):
            raw_md5 = s3_storage.get_operator().upload_local_file(tmp_path, relative_path)
            os.remove(tmp_path)
    else:
        if os.path.exists(tmp_path):
            shutil.move(tmp_path, os.path.join(settings.BASE_DIR, relative_path))


def _gen_image_download_path(path, fname):
    if not path:
        return None
    return os.path.join(get_current_sys_domain(), path)


def _get_media_path(is_secure):
    return settings.MEDIA_PATH_PROTECT if is_secure == TRUE_STR else settings.MEDIA_PATH_PUBLIC


def image_handle_common(image_file, user, is_secure):
    # 存储安全路径还是公开路径
    media_path = _get_media_path(is_secure)

    # 生成全局唯一文件名
    unique_file_name = file_storage.filename_unique(image_file.name)
    unique_thumb_name = file_storage.gen_thumb_fname(unique_file_name)
    unique_crop_name = file_storage.gen_crop_fname(unique_file_name)

    # 文件保存相对路径： media/{public|proteced}/image/{school_code}/{filename}_{uuid1}.{ext}
    image_repo = os.path.join(media_path, user.school.code, 'image')
    relative_path = file_storage.gen_path(image_repo, unique_file_name)
    thumb_relative_path = file_storage.gen_path(image_repo, unique_thumb_name)
    crop_relative_path = file_storage.gen_path(image_repo, unique_crop_name)

    # 依照EXIF旋转图片
    try:
        im_after_orient = tools.pic_orientation(Image.open(image_file))
    except Exception as e:
        logger.exception(e)
        raise BusinessException(INVALID_IMAGE)
    path_after_orient = os.path.join(file_storage.safe_folder(settings.TEMP_DIR), unique_file_name)
    im_after_orient.save(path_after_orient)

    # 处理缩略图
    thumb_tmp_path = os.path.join(file_storage.safe_folder(settings.TEMP_DIR), unique_thumb_name)
    has_thumb = file_storage.create_thumb(path_after_orient, thumb_tmp_path)

    # 处理裁剪图
    crop_tmp_path = os.path.join(file_storage.safe_folder(settings.TEMP_DIR), unique_crop_name)
    if not os.path.exists(thumb_tmp_path):
        has_crop = file_storage.create_crop(path_after_orient, crop_tmp_path)
    else:
        has_crop = file_storage.create_crop(thumb_tmp_path, crop_tmp_path)

    if settings.USE_S3:
        md5 = s3_storage.get_operator().upload_local_file(path_after_orient, relative_path)
        os.remove(path_after_orient)
    else:
        shutil.move(path_after_orient, os.path.join(settings.BASE_DIR, relative_path))
        # file_storage.save_file(image_file, os.path.join(settings.BASE_DIR, relative_path))

    if has_thumb:
        _save_local_tmp_image(thumb_tmp_path, thumb_relative_path)
    if has_crop:
        _save_local_tmp_image(crop_tmp_path, crop_relative_path)

    image_to_save = SysImage()
    image_to_save.image_name = image_file.name
    image_to_save.image_size = str(image_file.size)
    image_to_save.image_square = ','.join([str(each) for each in Image.open(image_file).size])
    image_to_save.image_original_url = relative_path
    image_to_save.account = user
    image_to_save.user_type = user.type
    image_to_save.user_school = user.school
    image_to_save.is_protected = int(is_secure)
    if has_thumb:
        image_to_save.image_thumb_url = thumb_relative_path
    if has_crop:
        image_to_save.image_crop_url = crop_relative_path
    image_to_save.image_type = (image_file.name[image_file.name.rfind('.') + 1:]).lower()
    image_to_save.save()

    return_ori_path = _gen_image_download_path(image_to_save.image_original_url, image_file.name)
    return_thumb_path = _gen_image_download_path(image_to_save.image_thumb_url or image_to_save.image_original_url, image_file.name)
    return_crop_path = _gen_image_download_path(image_to_save.image_crop_url, image_file.name)

    return image_to_save, return_ori_path, return_thumb_path, return_crop_path


def image_handle_gif(image_file, user, is_secure):
    # 存储安全路径还是公开路径
    media_path = _get_media_path(is_secure)

    # 生成全局唯一文件名
    unique_file_name = file_storage.filename_unique(image_file.name)

    # 文件保存相对路径： media/{public|proteced}/image/{school_code}/{filename}_{uuid1}.{ext}
    image_repo = os.path.join(media_path, user.school.code, 'image')
    relative_path = file_storage.gen_path(image_repo, unique_file_name)

    if settings.USE_S3:
        md5 = s3_storage.get_operator().upload_file_obj(image_file, relative_path)
    else:
        file_storage.save_file(image_file, os.path.join(settings.BASE_DIR, relative_path))

    image_to_save = SysImage()
    image_to_save.image_name = image_file.name
    image_to_save.image_size = str(image_file.size)
    image_to_save.image_square = ','.join([str(each) for each in Image.open(image_file).size])
    image_to_save.image_original_url = relative_path
    image_to_save.account = user
    image_to_save.user_type = user.type
    image_to_save.user_school = user.school
    image_to_save.is_protected = int(is_secure)
    image_to_save.image_thumb_url = relative_path
    image_to_save.image_crop_url = relative_path
    image_to_save.image_type = (image_file.name[image_file.name.rfind('.') + 1:]).lower()
    image_to_save.save()

    return_ori_path = _gen_image_download_path(image_to_save.image_original_url, image_file.name)
    return_thumb_path = return_ori_path
    return_crop_path = return_ori_path

    return image_to_save, return_ori_path, return_thumb_path, return_crop_path


def upload_image(image_file, user, is_secure):
    """
        上传一个图片，保存在本地或者S3存储
    """
    ext = (image_file.name[image_file.name.rfind('.')+1:]).lower()
    if ext == 'gif':
        image_obj, ori_path, thumb_path, crop_path = image_handle_gif(image_file, user, is_secure)
    else:
        image_obj, ori_path, thumb_path, crop_path = image_handle_common(image_file, user, is_secure)

    return_json = {
        'image_id': str(image_obj.id),
        'image_name': image_file.name,
        'original_size': str(image_file.size),
        'original_image_url': ori_path,
        'image_url': thumb_path,
        'image_crop_url': crop_path,
        'original_width': image_obj.image_square.split(',')[0],
        'original_height': image_obj.image_square.split(',')[1],
    }
    return return_json


uc_url = None
def domain_uc():
    global uc_url
    if not uc_url:
        from applications.user_center import agents
        uc_url = agents.get_user_center_url()
    return uc_url


this_sys_url = None
def domain_this():
    global this_sys_url
    if not this_sys_url:
        this_service = Service.objects.filter(code__in=(settings.SYSTEM_NAME,)).first()
        if not this_service:
            return None
        this_sys_url = net_helper.url_with_scheme_and_location(this_service.internet_url)
    return this_sys_url


this_sys_url_internal = None
def domain_this_internal():
    global this_sys_url_internal
    if not this_sys_url_internal:
        this_service = Service.objects.filter(code__in=(settings.SYSTEM_NAME,)).first()
        if not this_service:
            return None
        this_sys_url_internal = net_helper.url_with_scheme_and_location(this_service.intranet_url)
    return this_sys_url_internal


def get_uc_static_file_path(fname):
    """
        获取用户中心文件的全路径
    """
    if not fname:
        return ''
    if getattr(settings, 'UC_INFORMAL_DOMAIN', None) and getattr(settings, 'UC_INFORMAL_STATIC_PATH', None):
        return os.path.join(settings.UC_INFORMAL_DOMAIN + settings.UC_INFORMAL_STATIC_PATH, fname)
    else:
        path = '/' + settings.SERVICE_USER_CENTER_BUCKET + '/' + fname
        return domain_uc() + path


def get_current_sys_domain():
    if getattr(settings, 'LOCAL_INFORMAL_DOMAIN', None):
        return settings.LOCAL_INFORMAL_DOMAIN
    return domain_this()


def is_same_user_by_tuple_dict(user_dict_1, user_dict_2):
    """
        判断包含了身份三元组的两个字典是否指向同一个人物角色
    """
    return user_dict_1['account_id'] == user_dict_2['account_id'] \
        and user_dict_1['user_type_id'] == user_dict_2['user_type_id'] \
        and user_dict_1['school_id'] == user_dict_2['school_id']


def image_delete(image):
    if settings.USE_S3:
        if image.image_original_url:
            s3_storage.get_operator().delete(image.image_original_url)
        if image.image_thumb_url:
            s3_storage.get_operator().delete(image.image_thumb_url)
        if image.image_crop_url:
            s3_storage.get_operator().delete(image.image_crop_url)
    else:
        if image.image_original_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, image.image_original_url))
        if image.image_thumb_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, image.image_thumb_url))
        if image.image_crop_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, image.image_crop_url))
    image.is_del = TRUE_INT
    image.save()


def video_delete(video):
    if settings.USE_S3:
        if video.video_url:
            s3_storage.get_operator().delete(video.video_url)
        if video.video_converted_url:
            s3_storage.get_operator().delete(video.video_converted_url)
        if video.video_snapshot_url:
            s3_storage.get_operator().delete(video.video_snapshot_url)
    else:
        if video.video_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, video.video_url))
        if video.video_converted_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, video.video_converted_url))
        if video.video_snapshot_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, video.video_snapshot_url))
    video.is_del = TRUE_INT
    video.save()


def voice_delete(voice):
    if settings.USE_S3:
        if voice.voice_url:
            s3_storage.get_operator().delete(voice.voice_url)
    else:
        if voice.voice_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, voice.voice_url))
    voice.is_del = TRUE_INT
    voice.save()


def file_delete(f):
    if settings.USE_S3:
        if f.file_url:
            s3_storage.get_operator().delete(f.file_url)
    else:
        if f.file_url:
            file_storage.safe_delete(os.path.join(settings.BASE_DIR, f.file_url))
    f.is_del = TRUE_INT
    f.save()


def get_media_image_redundant():
    from applications.moment.models import MomentAttachImage
    qs = MomentAttachImage.objects.filter(is_del=FALSE_INT, image__is_del=FALSE_INT)
    moment_used_images = [each.image for each in qs]
    total_imgs = list(SysImage.objects.filter(is_del=FALSE_INT))
    return set(total_imgs) - set(moment_used_images)


def clear_media_image():
    for each_need_delete in get_media_image_redundant():
        try:
            expires_time = each_need_delete.update_time + datetime.timedelta(seconds=settings.MEDIA_EXPIRE_TIME)
            if datetime.datetime.now() > expires_time:
                logger.info('delete redundant item: ' + str(each_need_delete))
                image_delete(each_need_delete)
            else:
                logger.info('redundant item is not expired, delete it later: ' + str(each_need_delete))
        except Exception as e:
            logger.exception(e)
            continue


def get_media_video_redundant():
    from applications.moment.models import MomentAttachVideo
    qs = MomentAttachVideo.objects.filter(is_del=FALSE_INT, video__is_del=FALSE_INT)
    moment_used_items = [each.video for each in qs]
    total_items = list(SysVideo.objects.filter(is_del=FALSE_INT))
    return set(total_items) - set(moment_used_items)


def clear_media_video():
    for each_need_delete in get_media_video_redundant():
        try:
            expires_time = each_need_delete.update_time + datetime.timedelta(seconds=settings.MEDIA_EXPIRE_TIME)
            if datetime.datetime.now() > expires_time:
                logger.info('delete redundant item: ' + str(each_need_delete))
                video_delete(each_need_delete)
            else:
                logger.info('redundant item is not expired, delete it later: ' + str(each_need_delete))
        except Exception as e:
            logger.exception(e)
            continue


def get_media_voice_redundant():
    from applications.moment.models import MomentAttachVoice
    qs = MomentAttachVoice.objects.filter(is_del=FALSE_INT, voice__is_del=FALSE_INT)
    moment_used_items = [each.voice for each in qs]
    total_items = list(SysVoice.objects.filter(is_del=FALSE_INT))
    return set(total_items) - set(moment_used_items)


def clear_media_voice():
    for each_need_delete in get_media_voice_redundant():
        try:
            expires_time = each_need_delete.update_time + datetime.timedelta(seconds=settings.MEDIA_EXPIRE_TIME)
            if datetime.datetime.now() > expires_time:
                logger.info('delete redundant item: ' + str(each_need_delete))
                voice_delete(each_need_delete)
            else:
                logger.info('redundant item is not expired, delete it later: ' + str(each_need_delete))
        except Exception as e:
            logger.exception(e)
            continue


def get_media_file_redundant():
    from applications.moment.models import MomentAttachFile
    from applications.notification.models import NotifyAttachFile
    qs1 = MomentAttachFile.objects.filter(is_del=FALSE_INT, file__is_del=FALSE_INT)
    moment_used_items = [each1.file for each1 in qs1]
    qs2 = NotifyAttachFile.objects.filter(is_del=FALSE_INT, file__is_del=FALSE_INT)
    notify_used_items = [each2.file for each2 in qs2]
    total_items = list(SysFile.objects.filter(is_del=FALSE_INT))
    return set(total_items) - set(moment_used_items) - set(notify_used_items)


def clear_media_file():
    for each_need_delete in get_media_file_redundant():
        try:
            expires_time = each_need_delete.update_time + datetime.timedelta(seconds=settings.MEDIA_EXPIRE_TIME)
            if datetime.datetime.now() > expires_time:
                logger.info('delete redundant item: ' + str(each_need_delete))
                file_delete(each_need_delete)
            else:
                logger.info('redundant item is not expired, delete it later: ' + str(each_need_delete))
        except Exception as e:
            logger.exception(e)
            continue





