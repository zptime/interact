# coding=utf-8

# message definition
MSG_CATEGORY_SYS_GRP_INVITE = 'system_group_invite'
MSG_CATEGORY_SYS_GRP_ACCEPT = 'system_group_accept'
MSG_CATEGORY_SYS_GRP_DENY = 'system_group_deny'
MSG_CATEGORY_SYS_GRP_KICKOUT = 'system_group_kickout'
MSG_CATEGORY_SYS_GRP_DISSOLVE = 'system_group_dissolve'
MSG_CATEGORY_SYS_GRP_QUIT = 'system_group_quit'
MSG_CATEGORY_MOMENT_LIKE = 'moment_dynamic_like'
MSG_CATEGORY_MOMENT_REPLY_TOPIC = 'moment_dynamic_reply_topic'
MSG_CATEGORY_MOMENT_REPLY_COMMENT = 'moment_dynamic_reply_comment'
MSG_CATEGORY_NOTIFY_RECEIVE = 'notify_receive'
MSG_CATEGORY_NOTIFY_HOMEWORK = 'system_notify_homework'
MSG_CATEGORY_NOTIFY_CLASS = 'system_notify_class'

# ------------------------ don't modify below ---------------------------

FAIL = [-1, u'请求失败']
SUCCESS = [0, u'请求完成']

ERR_CODE_CONNECT_MSG_CENTER_FAIL = 11
ERR_MSG_CONNECT_MSG_CENTER_FAIL = u'与消息中心通讯失败'
ERR_CODE_WRONG_MSG_FORMAT = 12
ERR_MSG_WRONG_MSG_FORMAT = u'消息结构错误'

REQUEST_TIMEOUT = 20  # 与消息中心通信超时时间 second
