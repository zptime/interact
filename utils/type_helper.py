# -*- coding=utf-8 -*-

import time
import types
import datetime


DEFAULT_FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S"


def is_string(data):
    return isinstance(data, basestring)


def not_null_string(data, default=''):
    """
        将None和数值型转化为String
    """
    if isinstance(data, types.NoneType):
        return default
    elif isinstance(data, types.IntType) or isinstance(data, types.FloatType):
        return str(data)
    else:
        return data


def datetime2str(datetime_para, format=DEFAULT_FORMAT_DATETIME):
    """
        时间转字符串
    """
    if not datetime_para:
        return ''
    return datetime_para.strftime(format)


def bool2str(bool_para):
    """
        布尔值转字符串
    """
    return '1' if bool_para else '0'


def str2bool(str_para):
    """
        字符串转布尔值
    """
    return False if str_para == '0' else True


def str2datetime(datetime_str):
    """
        功能说明：str日期转换为时间,YYYY-mm-dd hh:mm:ss
    """
    try:
        day = datetime.datetime.strptime(datetime_str, DEFAULT_FORMAT_DATETIME)
    except:
        day = datetime.datetime.now()
    return day


def datetime2timestamp(dt, without_point=False):
    timeStamp = int(time.mktime(dt.timetuple()))
    timeStamp = '%.3f'% (float(str(timeStamp) + str("%06d" % dt.microsecond)) / 1000000)
    if without_point:
        timeStamp = timeStamp.replace('.', '')
    return timeStamp


def timestamp2datetime(ts):
    return datetime.datetime.fromtimestamp(ts)