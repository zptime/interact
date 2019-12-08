# -*- coding=utf-8 -*-

import logging

from utils import auth_check
from utils.auth_check import *

from applications.message.helper import *
from applications.contacts.models import GroupMember, Group
from applications.common.services import *
from utils.tools import get_type_user, remove_dup_in_dictlist
from utils.utils_user import student_qs

logger = logging.getLogger(__name__)


def invite_user(request_user, grp, invite_users):
    # 只能邀请自己创建的群组
    if grp.account != request_user or grp.user_type != request_user.type or grp.school != request_user.school:
        raise BusinessException(CANNOT_CONTROL_NON_SELFCREATE_GRP)

    # 受邀用户必须在自己的通讯录中
    contacters = get_contact_book(request_user, flat=True)
    contacters_tuple_list = [(each_contact['account_id'], each_contact['user_type_id'], each_contact['school_id'])
                             for each_contact in contacters]

    for each in invite_users:
        account_id = each.split(',')[0]
        user_type_id = each.split(',')[1]
        school_id = each.split(',')[2]

        # 新版本仅支持让学生加入群组
        if int(user_type_id) != USER_TYPE_STUDENT:
            raise BusinessException(ONLY_STUDENT_CAN_ADDIN_GRP)

        if (account_id, user_type_id, school_id) not in contacters_tuple_list:
            logger.warn('user is not exist in user contact book: %s,%s,%s' % (account_id, user_type_id, school_id))
            continue
        try:
            user = auth_check.check_get_account(int(account_id))
            school = auth_check.check_get_school(int(school_id))
        except Exception as e:
            logger.exception(e)
            logger.warn('invite user into group, but user is not exist: %s,%s,%s' % (account_id, user_type_id, school_id))
            continue

        # 检测此时用户是否在群组中,不重复添加用户
        if GroupMember.objects.filter(is_del=FALSE_INT,
                group=grp, account=user, user_type=int(user_type_id), school=school).exists():
            logger.warn('user is already in group, no need to re-add: %s,%s,%s' % (account_id, user_type_id, school_id))
            continue

        # 邀请的用户直接加入群组
        new_member = GroupMember()
        new_member.group = grp
        new_member.account = user
        new_member.user_type = int(user_type_id)
        new_member.school = school
        new_member.save()


def delete_user(req_user, grp, delete_user_list):

    # 只能管理自己创建的群组
    if grp.account != req_user or grp.user_type != req_user.type or grp.school != req_user.school:
        raise BusinessException(CANNOT_CONTROL_NON_SELFCREATE_GRP)

    for each in delete_user_list:
        account_id = each.split(',')[0]
        user_type_id = each.split(',')[1]
        school_id = each.split(',')[2]

        try:
            user = auth_check.check_get_account(int(account_id))
            school = auth_check.check_get_school(int(school_id))
        except Exception as e:
            logger.exception(e)
            logger.warn('try to delete user from group, but user is not exist: %s,%s,%s' % (account_id, user_type_id, school_id))
            continue

        # # 不可删除群组的创建者
        # if account_id == str(grp.account.id) and user_type_id == str(grp.user_type) and school_id == str(grp.school.id):
        #     logger.warn('can not remove group creator from group, skip it')
        #     continue

        # 如果此人本来就不在该群组，跳过处理
        qs = GroupMember.objects.filter(
            is_del=FALSE_INT, user_type=user_type_id, account=user, school=school, group=grp)
        if not qs.exists():
            logger.warn('user %s,%s,%s not in group, skip it' % (account_id, user_type_id, school_id))
            continue

        # 将用户从群组中移除
        qs.update(is_del=TRUE_INT)


def get_grp_user_list(group, verbose=True):
    user_list = list()
    members = list(group.members.filter(is_del=FALSE_INT, account__del_flag=FALSE_INT, school__del_flag=FALSE_INT).select_related())
    for member in members:
        member_info = {
            'account_id': str(member.account.id),
            'user_type_id': str(member.user_type),
            'school_id': str(member.school.id),
        }
        # 有可能用户已经被用户中心删除
        role_obj = tools.get_type_user(member.account.id, member.user_type, member.school.id)
        if not role_obj:
            # 如果用户已被用户中心删除，则从群组中移除
            member.is_del = TRUE_INT
            member.save()
            continue

        if verbose:
            is_creator = FALSE_STR
            if group.account == member.account \
                    and group.user_type == member.user_type \
                    and group.school == member.school:
                is_creator = TRUE_STR

            member_info['username'] = role_obj.full_name
            member_info['avatar'] = get_uc_static_file_path(role_obj.image_url)
            member_info['desc'] = get_user_desc(role_obj)
            member_info['is_creator'] = is_creator

        user_list.append(member_info)
    return tools.remove_dup_in_dictlist(user_list, ['account_id', 'user_type_id', 'school_id'])


def get_group_book(user):
    cluster = {
        CHAT_BOOK_CLUSTER_CLASS_GRP: list(),
        CHAT_BOOK_CLUSTER_CREATED_GRP: list(),
        CHAT_BOOK_CLUSTER_JOINED_GRP: list()
    }
    classes = get_classes_by_account(user)
    for each_class_info in classes:
        cluster[CHAT_BOOK_CLUSTER_CLASS_GRP].append({
            'class_id': each_class_info['class_id'],
            'class_name': each_class_info['class_name'],
            'grp_type': CHAT_GRP_TYPE_CLASS,
        })
    for each_grp_created in get_my_grp_created(user):
        cluster[CHAT_BOOK_CLUSTER_CREATED_GRP].append({
            'grp_id': str(each_grp_created.id),
            'grp_name': str(each_grp_created.name),
            'grp_type': CHAT_GRP_TYPE_CREATE,
        })
    tools.sort_list_by_dict_key(cluster[CHAT_BOOK_CLUSTER_CREATED_GRP], 'grp_name', in_place=True)
    for each_grp_joined in get_my_grp_joined(user):
        cluster[CHAT_BOOK_CLUSTER_JOINED_GRP].append({
            'grp_id': str(each_grp_joined.id),
            'grp_name': str(each_grp_joined.name),
            'grp_type': CHAT_GRP_TYPE_JOINED,
        })
    tools.sort_list_by_dict_key(cluster[CHAT_BOOK_CLUSTER_JOINED_GRP], 'grp_name', in_place=True)
    return cluster


def get_my_grp_created(account):
    grps_qs = Group.objects.filter(is_del=FALSE_INT, account=account, user_type=account.type, school=account.school)
    return list(grps_qs)


def get_my_grp_joined(account):
    members = GroupMember.objects.filter(is_del=FALSE_INT, account=account, user_type=int(account.type), school=account.school)
    grp_list = [each.group for each in members]

    # 自己创建的群组不在加入的群组中显示
    return list(set(grp_list) - set(get_my_grp_created(account)))


def get_contact_book_for_parent(parent, flat=False, except_me=True):
    """
        获取家长的通讯录人员
        flat： True扁平输出，False层叠输出
    """
    flat_userlist = list()  # 扁平输出
    cascade_userdict = {    # 层叠输出
        CHAT_BOOK_TEACHER_GRP: list(),
        CHAT_BOOK_STUDENT_GRP: list(),
        CHAT_BOOK_FAMILY_GRP: list()
    }

    # 获取孩子信息仅查询本校的
    my_children_rela = parent.parentstudent_set.filter(student__school=parent.school, del_flag=FALSE_INT, student__del_flag=FALSE_INT)
    children_classes = list()

    # 获取家长的各个子女信息
    for each_rela in my_children_rela:
        child = each_rela.student
        if child.cls:
            children_classes.append(child.cls)
        child_info = {
            'student_id': str(child.id),
            'account_id': str(child.account.id),
            'user_type_id': str(USER_TYPE_STUDENT),
            'school_id': str(child.account.school.id),
            'username': child.full_name,
            'avatar': get_uc_static_file_path(child.image_url),
            'phone': child.account.mobile,
            'desc': get_user_desc(child)
        }
        flat_userlist.append(child_info)
        cascade_userdict[CHAT_BOOK_FAMILY_GRP].append(child_info)

    # 获取家长各个子女所在班级的老师信息
    children_classes = set(children_classes)
    for clazz in children_classes:
        if clazz.del_flag == TRUE_INT:
            continue
        # teachers_id_in_class = [int(t['teacher_id']) for t in get_teacher_by_class(each_class)]
        # teachers = Teacher.objects.filter(id__in=teachers_id_in_class, del_flag=FALSE_INT).select_related()
        for each_teacher in get_teacher_by_class(clazz):
            teacher_info = {
                'teacher_id': str(each_teacher.id),
                'account_id': str(each_teacher.account.id),
                'user_type_id': str(USER_TYPE_TEACHER),
                'school_id': str(each_teacher.account.school.id),
                'username': each_teacher.full_name,
                'avatar': get_uc_static_file_path(each_teacher.image_url),
                'phone': each_teacher.account.mobile,
                'desc': get_user_desc(each_teacher),
            }
            flat_userlist.append(teacher_info)
            cascade_userdict[CHAT_BOOK_TEACHER_GRP].append(teacher_info)

    # 当多个子女拥有相同老师时，去掉重复的老师
    cascade_userdict[CHAT_BOOK_TEACHER_GRP] = tools.remove_dup_in_dictlist(cascade_userdict[CHAT_BOOK_TEACHER_GRP], ['account_id', 'user_type_id', 'school_id'])
    if flat:
        if not except_me:
            # self
            flat_userlist.append({
                'parent_id': str(parent.id),
                'account_id': str(parent.account.id),
                'user_type_id': str(USER_TYPE_PARENT),
                'school_id': str(parent.school.id),
                'username': parent.full_name,
                'avatar': get_uc_static_file_path(parent.image_url),
                'phone': parent.account.mobile,
                'desc': get_user_desc(parent),
            })
        flat_userlist = tools.remove_dup_in_dictlist(flat_userlist, ['account_id', 'user_type_id', 'school_id'])
        return flat_userlist
    else:
        return cascade_userdict


def get_contact_book_for_student(student, flat=False, except_me=True):
    """
        获取学生的通讯录人员
        flat： True扁平输出，False层叠输出
    """
    clazz = student.cls
    flat_userlist = list()  # 扁平输出
    cascade_userdict = {    # 层叠输出
        CHAT_BOOK_TEACHER_GRP: list(),
        CHAT_BOOK_STUDENT_GRP: list(),
        CHAT_BOOK_FAMILY_GRP: list()}

    # 获取学生所在班级的老师信息
    if clazz:
        # teacher_id_list = [int(t['teacher_id']) for t in get_teacher_by_class(clazz)]
        # all_teachers = Teacher.objects.filter(del_flag=FALSE_INT, id__in=teacher_id_list).select_related()
        for each_teacher in get_teacher_by_class(clazz):
            teacher_info = {
                'teacher_id': str(each_teacher.id),
                'account_id': str(each_teacher.account.id),
                'user_type_id': str(USER_TYPE_TEACHER),
                'school_id': str(each_teacher.account.school.id),
                'avatar': get_uc_static_file_path(each_teacher.image_url),
                'username': each_teacher.full_name,
                'phone': each_teacher.account.mobile,
                'desc': get_user_desc(each_teacher)
            }
            flat_userlist.append(teacher_info)
            cascade_userdict[CHAT_BOOK_TEACHER_GRP].append(teacher_info)
        tools.sort_list_by_dict_key(cascade_userdict[CHAT_BOOK_TEACHER_GRP], 'username', in_place=True)

    # 获取学生的家长
    parent_relation = student.parent_stu_relation.filter(del_flag=FALSE_INT, parent__del_flag=FALSE_INT).select_related()
    for each_rela in parent_relation:
        my_parent_info = {
            'parent_id': str(each_rela.parent.id),
            'account_id': str(each_rela.parent.account.id),
            'user_type_id': str(USER_TYPE_PARENT),
            'school_id': str(each_rela.parent.school.id),
            'avatar': get_uc_static_file_path(each_rela.parent.image_url),
            'username': each_rela.parent.full_name,
            'phone': each_rela.parent.account.mobile,
            'desc': get_user_desc(each_rela.parent)
        }
        flat_userlist.append(my_parent_info)
        cascade_userdict[CHAT_BOOK_FAMILY_GRP].append(my_parent_info)
    tools.sort_list_by_dict_key(cascade_userdict[CHAT_BOOK_FAMILY_GRP], 'username', in_place=True)

    # 获取学生所在班级的同学信息
    if clazz:
        class_info = {
            'class_id': str(clazz.id),
            'class_name': clazz.class_name,
            'is_mentor': '',  # 该字段对学生无效
            'students': list()
        }
        classmates = clazz.student_set.filter(del_flag=FALSE_INT).select_related()
        if except_me:
            classmates = classmates.exclude(id=student.id)
        for classmate in classmates:
            student_info = {
                'student_id': str(classmate.id),
                'account_id': str(classmate.account.id),
                'user_type_id': str(USER_TYPE_STUDENT),
                'school_id': str(classmate.school.id),
                'username': classmate.full_name,
                'avatar': get_uc_static_file_path(classmate.image_url),
                'phone': classmate.account.mobile,
                'desc': get_user_desc(classmate)
            }
            flat_userlist.append(student_info)
            # 获取学生下属的家长信息  -- 20170420, 学生不可看见同学的家长
            stu_relate_parent = list()
            if not flat:
                student_info['stu_relate_parent'] = stu_relate_parent
            class_info['students'].append(student_info)
        tools.sort_list_by_dict_key(class_info['students'], 'username', in_place=True)
        cascade_userdict[CHAT_BOOK_STUDENT_GRP].append(class_info)
    if flat:
        flat_userlist = tools.remove_dup_in_dictlist(flat_userlist, ['account_id', 'user_type_id', 'school_id'])
        return flat_userlist
    else:
        return cascade_userdict


def get_contact_book_for_teacher(teacher, flat=False, exclude=()):
    """
        获取老师的通讯录人员
        flat： True扁平输出，False层叠输出
    """
    flat_userlist = list()  # 扁平输出
    cascade_userdict = {    # 层叠输出
        CHAT_BOOK_TEACHER_GRP: list(),
        CHAT_BOOK_STUDENT_GRP: list(),
        CHAT_BOOK_FAMILY_GRP: list()}

    # 获取老师信息
    all_teachers = teacher.school.teacher_set.filter(del_flag=FALSE_INT).select_related()

    for each_teacher in all_teachers:
        triple = '%s_%s_%s' % (each_teacher.account.id, USER_TYPE_TEACHER, each_teacher.school.id)
        if triple in exclude:
            continue
        each_teacher_account = each_teacher.account
        each_teacher_info = {
            'teacher_id': str(each_teacher.id),
            'account_id': str(each_teacher_account.id),
            'user_type_id': str(USER_TYPE_TEACHER),
            'avatar': get_uc_static_file_path(each_teacher.image_url),
            'school_id': str(each_teacher.school.id),
            'username': each_teacher.full_name,
            'phone': each_teacher_account.mobile,
            'desc': USER_TYPE_MAP[USER_TYPE_TEACHER]
        }
        flat_userlist.append(each_teacher_info)
        cascade_userdict[CHAT_BOOK_TEACHER_GRP].append(each_teacher_info)
    tools.sort_list_by_dict_key(cascade_userdict[CHAT_BOOK_TEACHER_GRP], 'username', in_place=True)

    # 获取学生信息
    all_teach_class = get_class_by_teacher(teacher.id)
    for each_teach_class_obj in all_teach_class:
        clazz = each_teach_class_obj.cls
        class_user = {
            'class_id': str(clazz.id),
            'class_name': clazz.class_name,
            'is_mentor': str(each_teach_class_obj.is_master),
            'students': list()
        }

        # 班级里的所有学生
        students_in_class = clazz.student_set.filter(del_flag=FALSE_INT).select_related()

        # 班级里的所有家长学生联系
        p_s_in_class = list(ParentStudent.objects.filter(
            del_flag=FALSE_INT, parent__del_flag=FALSE_INT, student__in=students_in_class).select_related())

        for each_student in students_in_class:
            triple = '%s_%s_%s' % (each_student.account.id, USER_TYPE_STUDENT, each_student.school.id)
            if triple in exclude:
                continue
            student_info = {
                'student_id': str(each_student.id),
                'account_id': str(each_student.account.id),
                'user_type_id': str(USER_TYPE_STUDENT),
                'avatar': get_uc_static_file_path(each_student.image_url),
                'school_id': str(each_student.school.id),
                'username': each_student.full_name,
                'phone': each_student.account.mobile,
                'desc': clazz.class_name,
            }
            flat_userlist.append(student_info)

            # 获取学生下属的家长信息
            stu_relate_parent = list()
            for each_relation in p_s_in_class:
                if each_relation.student == each_student:
                    parent = each_relation.parent
                    triple = '%s_%s_%s' % (parent.account.id, USER_TYPE_PARENT, parent.school.id)
                    if triple in exclude:
                        continue
                    parent_info = {
                        'parent_id': str(parent.id),
                        'account_id': str(parent.account.id),
                        'user_type_id': str(USER_TYPE_PARENT),
                        'avatar': get_uc_static_file_path(parent.image_url),
                        'school_id': str(parent.school.id),
                        'username': parent.full_name,
                        'phone': parent.account.mobile,
                        'desc': get_parent_desc([each_student, ]),
                        'child_account_id': str(each_student.account.id),
                        'child_user_type_id': str(each_student.account.type),
                        'child_school_id': str(each_student.school.id),
                    }
                    flat_userlist.append(parent_info)
                    stu_relate_parent.append(parent_info)

            if not flat:
                student_info['stu_relate_parent'] = stu_relate_parent
            class_user['students'].append(student_info)
        tools.sort_list_by_dict_key(class_user['students'], 'username', in_place=True)
        cascade_userdict[CHAT_BOOK_STUDENT_GRP].append(class_user)
    tools.sort_list_by_dict_key(cascade_userdict[CHAT_BOOK_STUDENT_GRP], 'class_name', in_place=True)

    if flat:
        # 需要家长去重
        flat_userlist = tools.remove_dup_in_dictlist(flat_userlist, ['account_id', 'user_type_id', 'school_id'])
        return flat_userlist
    else:
        return cascade_userdict


def get_contact_book(user, flat=False, except_me=True):
    role = tools.get_type_current_user(user)
    if not role:
        raise BusinessException(USERTYPE_NOT_EXIST)
    if is_teacher(role):
        result = get_contact_book_for_teacher(role, flat=flat,
                    exclude=('%s_%s_%s' % (role.account.id, USER_TYPE_TEACHER, role.school.id),))
    elif is_student(role):
        result = get_contact_book_for_student(role, flat=flat, except_me=except_me)
    elif is_parent(role):
        result = get_contact_book_for_parent(role, flat=flat, except_me=except_me)
    else:
        raise BusinessException(USERTYPE_NOT_EXIST)
    return result


def dissolve_grp(user, grp):
    """
        解散一个群组
    """
    # request_user_role = tools.get_type_user(user.id, user.type, user.school.id)
    members_list = list()
    memeber_qs = grp.members.filter(is_del=FALSE_INT)
    with transaction.atomic():
        # for member in memeber_qs:
        #     members_list.append('%d,%d,%d' % (member.account.id, member.user_type, member.school.id))
        memeber_qs.update(is_del=TRUE_INT)
        grp.is_del = TRUE_INT
        grp.save()


def grp_detail(group_ids, user):
    result = list()
    for each_id in group_ids.split(','):
        if not each_id:
            continue
        grp = Group.objects.filter(is_del=FALSE_INT, id=int(each_id)).first()
        if (not grp) or (grp.school != user.school):
            result.append({
                'group_id': str(each_id),
                'group_status': FALSE_STR,
                'group_name': '',
                'member_count': '',
                'account_id': '',
                'user_type': '',
                'school_id': '',
                'school_name': '',
                'username': '',
                'avatar': '',
                'chat_id': '',
            })
        else:
            members = GroupMember.objects.filter(is_del=FALSE_INT, group=grp).count()
            usertype = tools.get_type_user(grp.account.id, grp.account.type, grp.school.id)
            result.append({
                'group_id': str(each_id),
                'group_status': TRUE_STR,
                'group_name': grp.name,
                'member_count': str(members),
                'account_id': str(grp.account.id),
                'user_type': str(grp.account.type),
                'school_id': str(grp.school.id),
                'school_name': str(grp.school.name_simple),
                'username': usertype.full_name,
                'avatar': get_uc_static_file_path(usertype.image_url),
                'chat_id': '',
            })
    return result


def create_grp(grp_name, user):
    if user.type != USER_TYPE_TEACHER:
        raise BusinessException(ONLY_TEACHER_CAN_HANDLE_GRP)

    # 群组名称不支持emoji表情
    if tools.containsEmoji(grp_name):
        raise BusinessException(GRP_NAME_NOT_SUPPORT_EMOJI)

    # 限制每个人创建群组的最大数目
    my_grp_count = Group.objects.filter(
        is_del=FALSE_INT, account=user, user_type=user.type, school=user.school).count()
    if my_grp_count >= GROUP_MAX:
        raise BusinessException(CREATE_GRP_MAX)

    with transaction.atomic():
        new_grp = Group()
        new_grp.name = grp_name
        new_grp.account = user
        new_grp.school = user.school
        new_grp.user_type = user.type
        # 同一所学校自定义群组名称不允许重复
        if Group.objects.filter(is_del=FALSE_INT, school=user.school, name=grp_name).exists():
            raise BusinessException(DUP_GROUP_NAME_IN_SCHOOL)
        new_grp.save()

        # 新版本群组是学生群组，老师无需加入
        # 将创建者加入群组
        # grp_m = GroupMember()
        # grp_m.group = new_grp
        # grp_m.account = user
        # grp_m.user_type = user.type
        # grp_m.school = user.school
        # grp_m.save()

    return new_grp


def edit_grp(group, group_name, user):
    # 只能修改自己创建的群组
    if group.account != user or group.user_type != user.type or group.school != user.school:
        raise BusinessException(CANNOT_CONTROL_NON_SELFCREATE_GRP)
    try:
        group.name = group_name
        group.save()
    except:
        raise BusinessException(EDIT_GRP_FAIL)


def v2_get_invite_available(grp, teacher):
    """
        针对新版和微信版的邀请成员列表接口
    """
    grp_user = GroupMember.objects.filter(group=grp)
    grp_user_triple = ['%s_%s_%s' % (each.account.id, each.user_type, each.school.id) for each in grp_user]
    logger.debug('these user already in group %s, skip them when try to invite user: %s' % (grp.name, grp_user_triple))
    return get_contact_book_for_teacher(teacher, flat=False, exclude=grp_user_triple)


def get_invite_available(group, user):   # deprecated
    result_list = list()
    is_teacher = (user.type == USER_TYPE_TEACHER)
    my_contact_book = get_contact_book(user, flat=True, except_me=False)
    member_tuple_list = [(each['account_id'], each['user_type_id'], each['school_id'])
                         for each in get_grp_user_list(group, verbose=False)]
    if is_teacher:
        parent_list = list()
        for each_in_book in my_contact_book:
            if each_in_book['user_type_id'] == str(USER_TYPE_PARENT):
                parent_list.append(each_in_book)

    for each_in_book in my_contact_book:
        contact_handled = {
            'account_id': each_in_book['account_id'],
            'user_type_id': each_in_book['user_type_id'],
            'school_id': each_in_book['school_id'],
            'username': each_in_book['username'],
            'avatar': each_in_book['avatar'],
            'desc': each_in_book['desc'],
            'is_in': FALSE_STR,
        }
        if (contact_handled['account_id'], contact_handled['user_type_id'],
                contact_handled['school_id']) in member_tuple_list:
            contact_handled['is_in'] = TRUE_STR

        # 如果老师查询可邀请用户,学生要处理关联的家长
        if is_teacher:
            if each_in_book['user_type_id'] == str(USER_TYPE_PARENT):
                continue
            if each_in_book['user_type_id'] == str(USER_TYPE_STUDENT):
                contact_handled['stu_relate_parent'] = list()
                for parent_in_book in parent_list:
                    if (parent_in_book['child_account_id'] == each_in_book['account_id'])\
                        and (parent_in_book['child_user_type_id'] == each_in_book['user_type_id'])\
                        and (parent_in_book['child_school_id'] == each_in_book['school_id']):
                        parent_handled = {
                            'account_id': parent_in_book['account_id'],
                            'user_type_id': parent_in_book['user_type_id'],
                            'school_id': parent_in_book['school_id'],
                            'username': parent_in_book['username'],
                            'avatar': parent_in_book['avatar'],
                            'desc': parent_in_book['desc'],
                            'is_in': FALSE_STR,
                        }
                        if (parent_handled['account_id'], parent_handled['user_type_id'],
                            parent_handled['school_id']) in member_tuple_list:
                            parent_handled['is_in'] = TRUE_STR
                        contact_handled['stu_relate_parent'].append(parent_handled)
            result_list.append(contact_handled)
        else:
            result_list.append(contact_handled)
    return result_list


def collect_stu(user_triples, grp_ids, clazz_ids):
    raw_list = list()

    if user_triples:
        user_triple_list = user_triples.strip(';').split(';')
        for each in user_triple_list:
            triple = each.split(',')
            raw_list.append({
                'account_id': int(triple[0]),
                'user_type': int(triple[1]),
                'school_id': int(triple[2]),
            })

    if grp_ids:
        for each_grp in grp_ids.strip(',').split(','):
            if not each_grp:
                continue
            group = Group.objects.filter(id=int(each_grp)).first()
            for each_stu_in_grp in GroupMember.objects.filter(group=group, user_type=USER_TYPE_STUDENT):
                raw_list.append({
                    'account_id': int(each_stu_in_grp.account.id),
                    'user_type': int(each_stu_in_grp.user_type),
                    'school_id': int(each_stu_in_grp.school.id),
                })

    if clazz_ids:
        clazzes = [Class.objects.filter(id=int(each_clazz)).first()
                    for each_clazz in clazz_ids.strip(',').split(',') if each_clazz]
        stus = student_qs().filter(cls__in=clazzes)
        for each_stu_in_clazz in stus:
            raw_list.append({
                'account_id': int(each_stu_in_clazz.account.id),
                'user_type': USER_TYPE_STUDENT,
                'school_id': int(each_stu_in_clazz.school.id),
            })

    trimed_list = remove_dup_in_dictlist(raw_list, ('account_id', 'user_type', 'school_id'))
    stu_id_list = list()
    for each in trimed_list:
        stu = get_type_user(each['account_id'], each['user_type'], each['school_id'])
        stu_id_list.append(stu)
    return stu_id_list
