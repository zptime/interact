# coding=utf-8


# 解散群组发消息给群组用户
# if settings.USE_MSG:       # you can use a switcher to control whether sending message
#     msg_content = {        # all parameters are string
#         # following content are different depend on message type
#         'account_id': str(grp.account.id),
#         'user_type_id': str(grp.user_type),
#         'school_id': str(grp.school.id),
#         'username': request_user_role.full_name,
#         'avatar': get_uc_static_file_path(request_user_role.image_url),
#         'group_id': str(grp.id),
#         'group_name': grp.name,
#         'description': u'%s解散了聊天群组: %s' % (request_user_role.full_name, grp.name)
#     }
#     send_user_str = ';'.join(members_list)   # members_list: ['2,2,1','3,2,1','4,2,1' ......]
#     send_msg(send_user_str, MSG_CATEGORY_SYS_GRP_DISSOLVE, msg_content)
