# -*- coding=utf-8 -*-
import collections
import logging
import re, sys
import os, time, random
import datetime
import types
import math
import socket
import uuid
from functools import wraps

import io

import operator
from urlparse import urljoin

from PIL import Image
from django.http import HttpResponse
import json
from decimal import Decimal
import base64
import hmac
import hashlib

from applications.user_center.models import *
from django.conf import settings
from utils import net_helper
from utils.constant import *
from utils.errcode import RATE_LIMIT

logger = logging.getLogger(__name__)


start_time = None
end_time = None


def t_start():
    global start_time
    start_time = datetime.datetime.now()


def t_end():
    global start_time
    global end_time
    end_time = datetime.datetime.now()
    logger.debug(end_time - start_time)


def get_pinyin(chinese):
    import pypinyin
    unicode_char = safe_unicode(chinese)
    first_l_list = pypinyin.lazy_pinyin(unicode_char, style=pypinyin.FIRST_LETTER)
    return ''.join(first_l_list)


def sort_list_by_dict_key(ori_list, key_str, reverse=False, in_place=False, mode=2):
    """
        in_place: 是否原地排序
        
        mode 1: 按照unicode排序 
        mode 2: 按照汉字拼音排序
        mode 3: 按照序号排序（一、壹、1、１） 
    """
    def _transfer_chinese_2_pinyin(raw):
        raw = raw.lstrip()
        string = raw
        if is_chinese_string(raw, mode=3):
            string = '~' + raw
        return get_pinyin(string)
    mode3_map = {
        u'0': u'00',
        u'1': u'01', u'2': u'02', u'3': u'03', u'4': u'04', u'5': u'05', u'6': u'06', u'7': u'07', u'8': u'08', u'9': u'09',
        u'零': u'10',
        u'一': u'11', u'二': u'12', u'三': u'13', u'四': u'14', u'五': u'15', u'六': u'16', u'七': u'17', u'八': u'18', u'九': u'19',
        u'壹': u'21', u'贰': u'22', u'叁': u'23', u'肆': u'24', u'伍': u'25', u'陆': u'26', u'柒': u'27', u'捌': u'28', u'玖': u'29',
        u'０': u'30',
        u'１': u'31', u'２': u'32', u'３': u'33', u'４': u'34', u'５': u'35', u'６': u'36', u'７': u'37', u'８': u'38', u'９': u'39'
    }

    def _trasfer_chinese_number_2_no(raw):
        string = safe_unicode(raw.lstrip())
        if not len(string) > 0:
            return ''
        new_str = string
        if string[0] in mode3_map:
            if len(string) <= 1:
                new_str = mode3_map[string[0]]
            else:
                new_str = mode3_map[string[0]] + string[1:]
        return new_str

    if 1 == mode:
        if not in_place:
            return sorted(ori_list, key=operator.itemgetter(key_str), reverse=reverse)
        else:
            ori_list.sort(key=operator.itemgetter(key_str), reverse=reverse)
    elif 2 == mode:
        if not in_place:
            return sorted(ori_list, key=lambda x: _transfer_chinese_2_pinyin(x[key_str]), reverse=reverse)
        else:
            ori_list.sort(
                # key=lambda x: x[key_str].decode("UTF8").encode("GB18030")
                key=lambda x: _transfer_chinese_2_pinyin(x[key_str]), reverse=reverse)
    elif 3 == mode:
        if not in_place:
            return sorted(ori_list, key=lambda x: _trasfer_chinese_number_2_no(x[key_str]), reverse=reverse)
        else:
            ori_list.sort(
                key=lambda x: _trasfer_chinese_number_2_no(x[key_str]), reverse=reverse)
    else:
        return None


def guid_by_uuid():
    """
        通过uuid生成唯一标识符
    """
    return str(uuid.uuid1()).replace('-', '')


def guid_by_time():
    """
        通过当前时间生成唯一标识符(20位)
    """
    fn = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
    fn += '%d' % random.randint(10, 99)
    return fn


def dictlist_sort(dictlist, cond):
    """
        字典列表排序，可指定按照不同字段的排序、优先级、是否按照数值排序等，目前支持字典value是字符串或者整型
        condiction = [  # 优先级从高到低， 'as_int'表示该字段是否按照整型排序
            {'key': 'a', 'sort': 'ASC'},
            {'key': 'b', 'sort': 'ASC'},
            {'key': 'c', 'sort': 'DESC', 'as_int': True},
        ]
        test_case_dictlist = [
            {'a': 'a01', 'b': 'b01', 'c': '5'},
            {'a': 'a01', 'b': 'b01', 'c': '20'},
            {'a': 'a03', 'b': 'b03', 'c': '4'},
            {'a': 'a02', 'b': 'b03', 'c': '5'},
            {'a': 'a02', 'b': 'b07', 'c': '3'},
            {'a': 'a03', 'b': 'b04', 'c': '15'},
            {'a': 'a01', 'b': 'b01', 'c': '10'},
        ] 
        排序结果：
        [
            {'a': 'a01', 'c': '20', 'b': 'b01'}, 
            {'a': 'a01', 'c': '10', 'b': 'b01'}, 
            {'a': 'a01', 'c': '5', 'b': 'b01'}, 
            {'a': 'a02', 'c': '5', 'b': 'b03'}, 
            {'a': 'a02', 'c': '3', 'b': 'b07'}, 
            {'a': 'a03', 'c': '4', 'b': 'b03'}, 
            {'a': 'a03', 'c': '15', 'b': 'b04'}
        ]
        或使用多次排序亦可：
        test_case_dictlist.sort(key=lambda x: int(x['c']))
        test_case_dictlist.sort(key=itemgetter('a', 'b'))
    """
    def need_reservse(string):
        return True if string == 'DESC' else False

    def get_comp_item(item, cond):
        if cond.get('as_int', False):
            try:
                value = int((item.get(cond['key'], 0)))
            except ValueError as e:
                value = item.get(cond['key'], '')
        else:
            value = item.get(cond['key'], '')
        return value

    cond.reverse()
    for each_cond in cond:
        dictlist.sort(key=lambda item: get_comp_item(item, each_cond),
                       reverse=need_reservse(each_cond['sort']))


def gen_url_with_fname(url, original_fname):
    """
        生成带有?fname=xxx格式的URL，使得nginx可以增加指定文件名的响应头
    """
    if not url or not original_fname:
        return ''
    (shortname, extension) = os.path.splitext(original_fname)
    return '%s?fname=%s' % (url, shortname)


def log_request(request):
    if settings.DEBUG:
        if hasattr(request, 'user'):
            user_account = getattr(request.user, 'username', '-')
        else:
            user_account = 'anonymous'
        logger.debug('%s %s' % (user_account, request.get_full_path()))


def log_response(request, data):
    if settings.DEBUG:
        logger.debug('request: %s, response json: %s' % (request.get_full_path(), json.dumps(data, ensure_ascii=False)))


def cut_last_char(raw, char_def=';'):
    if raw.endswith(char_def):
        return raw[0:-1]
    else:
        return raw


def format_multiple_role_str(raw, split_user=';', split_field=','):
    result_list = list()
    for each in cut_last_char(raw).split(split_user):
        account_id, user_type_id, school_id = each.split(split_field)
        result_list.append({
            'account_id': account_id,
            'user_type_id': user_type_id,
            'school_id': school_id,
        })
    return result_list


def split_system(original):
    if settings.SERVICE_SYSTEM_SPLIT_CHAR in original:
        return original.split(settings.SERVICE_SYSTEM_SPLIT_CHAR)[1]
    else:
        return original


def random_code(length):
    """
        随机生成验证码
    """
    num = '0123456789'
    return ''.join(random.sample(num, length))


def is_duplicate_field(app_name, model_name, field_name, value, del_str='is_del'):
    models_file_name = app_name + '.models'
    __import__(models_file_name)
    model_clazz = getattr(sys.modules[models_file_name], model_name)
    query_para = {
        del_str: False,
        field_name: value
    }
    return model_clazz.objects.filter(**query_para).exists()


def remove_dup_in_dictlist(raw_list, key):
    """
        从字典型列表中去除指定关键字重复的记录
    """
    result = list()
    key_bucket = list()
    for each in raw_list:
        if each[key] in key_bucket:
            continue
        else:
            result.append(each)
            key_bucket.append(each[key])
    return result


def record_time(func):
    """
        装饰器： 记录函数运行时间
    """
    @wraps(func)
    def returned_wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        return_value = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        logger.info('runtime %s : %s' % (func.__name__, str(end_time - start_time)))
        return return_value
    return returned_wrapper


def check_identity_no(id):
    """
        身份证合法性验证
    """
    id = id.upper()
    c = 0
    for (d, p) in zip(map(int, id[:~0]), range(17, 0, -1)):
        c += d * (2 ** p) % 11
    return id[~0] == '10X98765432'[c % 11]


def safe_unicode(raw):
    if not isinstance(raw, unicode) and not isinstance(raw, str):
        return str(raw).decode('utf8')
    elif isinstance(raw, str):
        return raw.decode('utf8')
    elif isinstance(raw, unicode):
        return raw
    else:
        return None


def unicode_2_utf8(raw):
    if not isinstance(raw, unicode):
        return str(raw)
    else:
        return raw.encode('utf8')


def is_chinese_string(raw_string, mode=1):
    """
        判断是否为中文字符串
        mode:
        1: 是不是全部是中文 
        2: 是不是包含中文 
        3: 是不是以中文开头
    """
    string = safe_unicode(raw_string.lstrip())
    if mode == 1:
        for x in string:
            if not (x >= u'\u4e00' and x <= u'\u9fa5'):
                return False
        return True
    elif mode == 2:
        for x in string:
            if (x >= u'\u4e00' and x <= u'\u9fa5'):
                return True
        return False
    elif mode == 3:
        if len(string) > 0:
            x = string[0]
            return (x >= u'\u4e00' and x <= u'\u9fa5')
        else:
            return False
    else:
        return False


def random_int_len(start, end, length):
    nums = range(start, end)
    data = random.sample(nums, length)
    return data


def today(FORMAT_DATE='%Y-%m-%d', is_str=True):
    if is_str:
        return time.strftime(FORMAT_DATE, time.localtime(time.time()))
    else:
        return datetime.datetime.strptime(
            time.strftime(FORMAT_DATE, time.localtime(time.time())),
            FORMAT_DATE)


def yesterday(FORMAT_DATE='%Y-%m-%d', is_str=True):
    if is_str:
        return time.strftime(FORMAT_DATE, time.localtime(time.time() - 24 * 60 * 60))
    else:
        return datetime.datetime.strptime(
            time.strftime(FORMAT_DATE, time.localtime(time.time() - 24 * 60 * 60)),
            FORMAT_DATE)


def remove_dup_in_dictlist(dictlist, keys_list):
    """
        去掉字典列表中的指定组合关键字重复的记录
    """
    remove_dup_list = list()
    result_list = list()
    for element in dictlist:
        tp = sorted((element[each_key] for each_key in keys_list))
        if tp not in remove_dup_list:
            result_list.append(element)
            remove_dup_list.append(tp)
    return result_list


def get_host_ip():
    """
        获取当前IP地址
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def mask_words(words, content):
    """
        替换敏感词
        敏感词用逗号分割
    """
    if not words:
        return content
    try:
        lst = words.split(',')
        for w in lst:
            content = content.replace(w, '**')
    except:
        logger.exception('')
    return content


def remove_html_tag(html):
    """
        去除html标签
    """
    reg = re.compile('<[^>]*>')
    return reg.sub('', html)


def copy_attr_include(src, destiny, include=()):
    for each in include:
        setattr(destiny, each, getattr(src, each))


def copy_image_attr(src, destiny):
    """
        从临时表到正式表复制图片属性
    """
    copy_attr_include(src, destiny,
                      include=('image_name', 'image_size', 'image_square', 'image_original_url', 'image_thumb_url', 'image_type'))


def copy_voice_attr(src, destiny):
    """
        从临时表到正式表复制语音属性
    """
    copy_attr_include(src, destiny,
                      include=('voice_name', 'voice_size', 'voice_duration', 'voice_url', 'voice_type'))


def copy_file_attr(src, destiny):
    """
        从临时表到正式表复制附件属性
    """
    copy_attr_include(src, destiny,
                      include=('file_name', 'file_size', 'file_url', 'file_type'))


def copy_video_attr(src, destiny):
    """
        从临时表到正式表复制视频属性
    """
    copy_attr_include(src, destiny, include=('video_name', 'video_size', 'video_duration',
            'video_url', 'video_cover_url', 'video_square','video_type'))


def get_type_current_user(user):
    return get_type_user(user.id, user.type, user.school.id)


def get_type_user(account_id, user_type, school_id):
    """
    查询ID当前对应的用户类型资料（学生、老师、家长）
    :param:用户ID，当前用户类型，学校ID
    :return:类型对应的对象
    """
    if user_type == USER_TYPE_STUDENT:
        result = Student.objects.filter(account_id=account_id, school_id=school_id, del_flag=FALSE_INT).first()
    elif user_type == USER_TYPE_TEACHER:
        result = Teacher.objects.filter(account_id=account_id, school_id=school_id, del_flag=FALSE_INT).first()
    elif user_type == USER_TYPE_PARENT:
        result = Parent.objects.filter(account_id=account_id, school_id=school_id, del_flag=FALSE_INT).first()
    else:
        result = None
    return result


def get_mac():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


def get_mac_last4():
    return ''.join(get_mac().split(':'))[-4:]


class BusinessException(Exception):
    """
        业务Exception，通常在view层捕捉
        传入errcode文件中定义的错误信息
    """
    def __init__(self, value):
        self.code = value[0]
        self.msg = value[1]

    def __str__(self):
        return repr(self.msg)


def print_json(raw_obj):
    """
        将字典/列表等格式漂亮输出成json格式
    """
    print json.dumps(raw_obj, ensure_ascii=False, indent=4)


def filter_with_tuple(model_name_abs, fields_list, tuple_list, del_str='is_del', kickout_del=True):
    """
        组合条件查询
        model_name example: applications.user_center.models.Account
    """
    if not tuple_list:
        return None
    _index = model_name_abs.rfind('.')
    model_name = model_name_abs[_index+1:]
    pkg = model_name_abs[:_index]
    __import__(pkg)
    model_clazz = getattr(sys.modules[pkg], model_name)
    query_para = {
        del_str: False,
    }
    fields_str = ','.join(fields_list)
    _tmp_list = list()

    for each in tuple_list:
        _tmp_list.append('(%s)'% ','.join([str(x) for x in each]))
    values_str = ','.join(_tmp_list)
    _qs_1 = model_clazz.objects.extra(where=['(%s) in (%s)' % (fields_str, values_str)])
    if kickout_del:
        _qs_2 = _qs_1.filter(**query_para)
    return _qs_2


def convert_and_compress(src, dest, pix=480):
    # ffmpeg -i xxx.mov -vcodec h264 -vf scale=480:-2 -r 24 -b:a 32k xxx.mp4
    try:
        cmd = "%s -i '%s' -vcodec h264 -vf scale=%d:-2 -r 24 -b:a 32k '%s'" % (settings.FFMPEG, src, int(pix), dest)
        logger.info(cmd)
        handler = os.popen(cmd)
    except Exception as e:
        logger.error('convert and compress video %s to %s fail' % (src, dest))
        logger.exception(e)
        return False
    finally:
        handler.close()
    if os.path.exists(dest) and (os.path.getsize(dest) > 0):
        logger.info('convert and compress video %s to %s successfully' % (src, dest))
        return True
    else:
        logger.error('convert and compress video %s to %s fail' % (src, dest))
        return False


def video_snapshot(src, dest, second='3'):
    """
        取视频中的截图
    """
    try:
        cmd = "%s -i '%s' -y -f image2 -ss %s -vframes 1 '%s'" % (settings.FFMPEG, src, second, dest)
        logger.info(cmd)
        handler = os.popen(cmd)
    except Exception as e:
        logger.error('create snapshot for video %s fail' % src)
        logger.exception(e)
        return False
    finally:
        handler.close()
    if os.path.exists(dest) and (os.path.getsize(dest) > 0):
        logger.info('create snapshot for video %s successfully' % src)
        return True
    else:
        logger.error('create snapshot for video %s fail' % src)
        return False


def convert_voice_2_mp3(src, dest):
    """
        将amr格式和wav格式转换为mp3格式
    """
    try:
        cmd = "%s -i '%s' '%s'" % (settings.FFMPEG, src, dest)
        logger.info(cmd)
        handler = os.popen(cmd)
    except Exception as e:
        logger.error('convert voice %s to %s fail' % (src, dest))
        logger.exception(e)
        return False
    finally:
        handler.close()
    if os.path.exists(dest) and (os.path.getsize(dest) > 0):
        logger.info('convert voice %s to %s successfully' % (src, dest))
        return True
    else:
        logger.error('convert voice %s to %s fail' % (src, dest))
        return False


def pic_orientation(im):
    """
    Extract the oritentation EXIF tag from the image, which should be a PIL Image instance,
    and if there is an orientation tag that would rotate the image, apply that rotation to
    the Image instance given to do an in-place rotation.

    :param Image im: Image instance to inspect
    :return: A possibly transposed image instance
    """
    def flip_horizontal(im):
        logger.info('image transpose horizontal')
        return im.transpose(Image.FLIP_LEFT_RIGHT)

    def flip_vertical(im):
        logger.info('image transpose vertical')
        return im.transpose(Image.FLIP_TOP_BOTTOM)

    def rotate_180(im):
        logger.info('image transpose 180')
        return im.transpose(Image.ROTATE_180)

    def rotate_90(im):
        logger.info('image transpose 90')
        return im.transpose(Image.ROTATE_90)

    def rotate_270(im):
        logger.info('image transpose 270')
        return im.transpose(Image.ROTATE_270)

    def transpose(im):
        return rotate_90(flip_horizontal(im))

    def transverse(im):
        return rotate_90(flip_vertical(im))

    orientation_funcs = [None,
         lambda x: x,      # 1
         flip_horizontal,  # 2
         rotate_180,       # 3
         flip_vertical,    # 4
         transpose,        # 5
         rotate_270,       # 6
         transverse,       # 7
         rotate_90         # 8
    ]
    try:
        kOrientationEXIFTag = 0x0112
        if hasattr(im, '_getexif'): # only present in JPEGs
            e = im._getexif()       # returns None if no EXIF data
            if e is not None:
                logger.info('EXIF data found: %r', e)
                orientation = e[kOrientationEXIFTag]
                f = orientation_funcs[orientation]
                return f(im)
            else:
                logger.info('EXIF data not found')
        else:
            logger.info('image has not EXIF, skip transpose')
    except:
        # We'd be here with an invalid orientation value or some random error?
        logger.warn("Error applying EXIF Orientation tag")
    return im


def containsEmoji(content):
    if not content:
        return False
    content_unicode = safe_unicode(content)
    for each in content_unicode:
        if u"\U0001F600" <= each and each <= u"\U0001F64F":
            return True
        elif u"\U0001F300" <= each and each <= u"\U0001F5FF":
            return True
        elif u"\U0001F680" <= each and each <= u"\U0001F6FF":
            return True
        elif u"\U0001F1E0" <= each and each <= u"\U0001F1FF":
            return True
        else:
            continue
    return False


def log_exception(e):
    if isinstance(e, BusinessException):
        # 应用捕获异常无需记录Error日志，也无需打印异常堆栈
        logger.warn(e.msg)
    else:
        logger.exception(e)


def response_ratelimit(msg=''):
    result_msg = RATE_LIMIT[1]
    if msg:
        result_msg = msg
    result = {'c': RATE_LIMIT[0], 'm': RATE_LIMIT[1]}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=200)


def gen_chat_root_user(school_code):
    result = list()
    for i in xrange(3):
        huanxin_id = 'root_%s_%d' % (school_code, i + 1)
        result.append(huanxin_id)
    return result


def paging_by_lastid(list_after_lastid_filter, rows):
    rows = int(rows)
    total = len(list_after_lastid_filter)
    max_page = total / rows
    if total % rows != 0:
        max_page += 1

    paged_list = list_after_lastid_filter[:rows]

    result = collections.OrderedDict()
    result['max_page'] = int(max_page)
    result['total'] = int(total)
    result['page'] = 0
    result['data_list'] = list()
    return paged_list, result


def paging_by_page(raw_list, rows, page):
    page = int(page)
    rows = int(rows)
    total = len(raw_list)
    max_page = total / rows
    if total % rows != 0:
        max_page += 1

    if total >= (page - 1) * rows:
        start = (page - 1) * rows
        end = start + rows
        paged_list = raw_list[start:end]
    else:
        paged_list = []

    result = collections.OrderedDict()
    result['max_page'] = int(max_page)
    result['total'] = int(total)
    result['page'] = int(page)
    result['data_list'] = list()
    return paged_list, result


def getpages(cnt, page, size):
    """
     分页，这种方式比Paginator更高效一些
    :param:总行数， 当前页码  ，每页行数
    :return: 总页数，本次开始行数，本次结束行数
    """
    # 分页，这种方式比Paginator更高效一些
    page = int(page)
    size = int(size)
    num_pages = math.ceil(float(cnt) / size)  # 总页数
    # if page > num_pages:
    #     raise BusinessException(MOMENT_NORECORD)
    cur_start = (page - 1) * size
    cur_end = page * size
    return num_pages, cur_start, cur_end


def url(domain, filename):
    if not filename:
        return ''
    return urljoin(domain, filename)

