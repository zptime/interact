# -*- coding=utf-8 -*-

import logging
import json

from applications.message import helper
from applications.message.const import ERR_MSG_CONNECT_MSG_CENTER_FAIL, ERR_CODE_CONNECT_MSG_CENTER_FAIL, ERR_MSG_WRONG_MSG_FORMAT, ERR_CODE_WRONG_MSG_FORMAT
from applications.message.helper import _remote_call


logger = logging.getLogger(__name__)


def send_msg(recipients, category, content, api_version='1'):
    """
        向消息中心发送消息
        suggest: use celery task to send msg
    """
    if not category or not content:
        logger.error('try to send message but without category or content')
        return helper.response200({'c': ERR_CODE_WRONG_MSG_FORMAT, 'm': ERR_MSG_WRONG_MSG_FORMAT})
    payload = {
        'function_name': 'create_msg',
        'parameter': json.dumps({
            'api_version': api_version,
            'recipients': recipients,   # format: account_id,user_type,school_id, e.g. 2,2,1;2,2,1;2,2,1
            'category_code': category,
            'content': json.dumps(content, ensure_ascii=False),
        }, ensure_ascii=False)
    }
    try:
        logger.info('send message to message_center:')
        logger.info(payload)
        remote_response = _remote_call(payload)
    except Exception as e:
        logger.exception(e)
        return helper.response200({'c': ERR_CODE_CONNECT_MSG_CENTER_FAIL, 'm': ERR_MSG_CONNECT_MSG_CENTER_FAIL})
    logger.info('message_center return response:')
    logger.info(remote_response)
    # remote_response  e.g:
    # {'tracking_num': str(tracking.id)}
    return remote_response