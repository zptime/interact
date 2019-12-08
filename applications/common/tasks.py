# coding:utf-8

from __future__ import absolute_import, unicode_literals

import logging
import os
import shutil

from PIL import Image

from applications.common.models import SysVideo, SysVoice
from interact.celery import interact_app
from django.conf import settings
from utils import file_storage
from utils import s3_storage
from utils import tools
from utils.constant import *


logger = logging.getLogger(__name__)

# 覆盖django的日志，打印到celery的log中
# from celery.utils.log import get_task_logger
# logger_task = get_task_logger(__name__)


# @interact_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'default_retry_delay' : 90})
# def compress_mp4(video_id):
#     logger.info('compress video %d ...' % video_id)
#     COMPRESS_TMP_PATH = 'video_compress'
#     COMPRESS_TMP_PATH_ABS = file_storage.safe_folder(os.path.join(settings.TEMP_DIR, COMPRESS_TMP_PATH))
#     video = SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).first()
#     if not video:
#         return
#     SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(video_compressed_status=VIDEO_COMPRESS_STATUS_ING)
#
#     media_path = settings.MEDIA_PATH_PROTECT if video.is_protected == TRUE_INT else settings.MEDIA_PATH_PUBLIC
#     raw_fname = video.video_url[video.video_url.rfind('/') + 1:]
#     compressed_fname = raw_fname[:raw_fname.rfind('.')] + '_compressed_480.mp4'
#     # 转换后文件保存的相对路径
#     relative_path = file_storage.gen_path(os.path.join(media_path, video.user_school.code, 'video'), compressed_fname)
#     if settings.USE_S3:
#         logger.info('download (s3) video %d to compress' % video_id)
#         # 下载原始视频到本地临时目录
#         _key = video.video_url
#         _local_temp_path = os.path.join(COMPRESS_TMP_PATH_ABS, raw_fname)
#         _local_temp_path_after = os.path.join(COMPRESS_TMP_PATH_ABS, compressed_fname)
#         s3_storage.get_operator().download_file(_key, _local_temp_path)
#         # 转码生成新视频文件
#         is_succ = tools.compress_mp4(_local_temp_path, _local_temp_path_after)
#         if is_succ:
#             logger.info('compress video successfully, and start uploading to s3 ...')
#             raw_md5 = s3_storage.get_operator().upload_local_file(_local_temp_path_after, relative_path)
#             logger.info('upload compressed video to s3 successfully')
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(
#                 video_compressed_status=VIDEO_COMPRESS_STATUS_SUCC,
#                 video_compressed_url=relative_path)
#         else:
#             logger.info('compress video fail')
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(
#                 video_compressed_status=VIDEO_COMPRESS_STATUS_FAIL)
#         file_storage.safe_delete(_local_temp_path)
#         file_storage.safe_delete(_local_temp_path_after)
#     else:
#         logger.info('use local video %d to compress' % video_id)
#         _local_temp_path_after = os.path.join(COMPRESS_TMP_PATH_ABS, compressed_fname)
#         # 转码生成新视频文件
#         is_succ = tools.compress_mp4(os.path.join(settings.BASE_DIR, video.video_url), _local_temp_path_after)
#         if is_succ:
#             logger.info('compress video successfully')
#             shutil.move(_local_temp_path_after, os.path.join(settings.BASE_DIR, relative_path))
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(
#                 video_compressed_status=VIDEO_COMPRESS_STATUS_SUCC,
#                 video_compressed_url=relative_path)
#         else:
#             logger.info('compress video fail')
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(
#                 video_compressed_status=VIDEO_COMPRESS_STATUS_FAIL)
#             file_storage.safe_delete(_local_temp_path_after)


@interact_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'default_retry_delay' : 90})
def convert(video_id):
    logger.info('convert and compress video %d ...' % video_id)
    CONVERT_TMP_PATH = 'video_convert'
    CONVERT_TMP_PATH_ABS = file_storage.safe_folder(os.path.join(settings.TEMP_DIR, CONVERT_TMP_PATH))
    video = SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).first()
    if not video:
        return
    SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(video_converted_status=VIDEO_CONVERT_STATUS_ING)

    media_path = settings.MEDIA_PATH_PROTECT if video.is_protected == TRUE_INT else settings.MEDIA_PATH_PUBLIC
    raw_fname = video.video_url[video.video_url.rfind('/')+1:]
    converted_fname = raw_fname[:raw_fname.rfind('.')] + '_converted.mp4'
    # 转换后文件保存的相对路径
    relative_path = file_storage.gen_path(os.path.join(media_path, video.user_school.code, 'video'), converted_fname)

    # 截图相关信息
    SNAP_TMP_PATH = 'video_snapshot'
    SNAP_TMP_PATH_ABS = file_storage.safe_folder(os.path.join(settings.TEMP_DIR, SNAP_TMP_PATH))
    snap_fname = raw_fname[:raw_fname.rfind('.')] + '_snapshot.png'
    snap_relative_path = file_storage.gen_path(os.path.join(media_path, video.user_school.code, 'video_snapshot'), snap_fname)

    if settings.USE_S3:
        logger.info('download (s3) video %d to convert and compress' % video_id)
        # 下载原始视频到本地临时目录
        _key = video.video_url
        _local_temp_path = os.path.join(CONVERT_TMP_PATH_ABS, raw_fname)
        _local_temp_path_after = os.path.join(CONVERT_TMP_PATH_ABS, converted_fname)

        _local_temp_path_snapshot = os.path.join(SNAP_TMP_PATH_ABS, snap_fname)

        s3_storage.get_operator().download_file(_key, _local_temp_path)

        # 转码生成新视频文件
        is_succ = tools.convert_and_compress(_local_temp_path, _local_temp_path_after)
        if is_succ:
            logger.info('convert and compress video successfully, and start uploading to s3 ...')
            raw_md5 = s3_storage.get_operator().upload_local_file(_local_temp_path_after, relative_path)
            logger.info('upload converted video to s3 successfully')
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(
                video_converted_status=VIDEO_CONVERT_STATUS_SUCC,
                video_converted_url=relative_path,)
        else:
            logger.info('convert and compress video fail')
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(
                video_converted_status=VIDEO_CONVERT_STATUS_FAIL)

        is_snap_succ = tools.video_snapshot(_local_temp_path_after, _local_temp_path_snapshot)  # 截图使用压缩后的视频文件
        if is_snap_succ:
            logger.info('snapshot video successfully, and start uploading to s3 ...')
            raw_md5 = s3_storage.get_operator().upload_local_file(_local_temp_path_snapshot, snap_relative_path)
            logger.info('upload snapshot video to s3 successfully')
            snapshot_square = Image.open(_local_temp_path_snapshot).size
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT) \
                .update(video_snapshot_status=VIDEO_SNAPSHOT_STATUS_SUCC,
                        video_square='%d,%d' % (snapshot_square[0], snapshot_square[1]),
                        video_snapshot_url=snap_relative_path)
        else:
            logger.error('snapshot video fail')
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT) \
                .update(video_snapshot_status=VIDEO_SNAPSHOT_STATUS_FAIL)

        file_storage.safe_delete(_local_temp_path)
        file_storage.safe_delete(_local_temp_path_snapshot)
        file_storage.safe_delete(_local_temp_path_after)
    else:
        logger.info('use local video %d to convert and compress' % video_id)
        _local_temp_path_after = os.path.join(CONVERT_TMP_PATH_ABS, converted_fname)
        _local_temp_path_snapshot = os.path.join(SNAP_TMP_PATH_ABS, snap_fname)

        # 转码生成新视频文件
        is_succ = tools.convert_and_compress(os.path.join(settings.BASE_DIR, video.video_url), _local_temp_path_after)
        if is_succ:
            logger.info('convert and compress video successfully')
            shutil.copy(_local_temp_path_after, os.path.join(settings.BASE_DIR, relative_path))
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(
                video_converted_status=VIDEO_CONVERT_STATUS_SUCC,
                video_converted_url=relative_path,)
        else:
            logger.info('convert and compress video fail')
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(video_converted_status = VIDEO_CONVERT_STATUS_FAIL)            

        is_snap_succ = tools.video_snapshot(_local_temp_path_after, _local_temp_path_snapshot)  # 截图使用压缩后的视频文件
        if is_snap_succ:
            logger.info('snapshot video successfully')
            snapshot_square = Image.open(_local_temp_path_snapshot).size
            shutil.move(_local_temp_path_snapshot, os.path.join(settings.BASE_DIR, snap_relative_path))
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT) \
                .update(video_square='%d,%d' % (snapshot_square[0], snapshot_square[1]),
                        video_snapshot_status=VIDEO_SNAPSHOT_STATUS_SUCC,
                        video_snapshot_url=relative_path)
        else:
            logger.info('snapshot video fail')
            SysVideo.objects.filter(id=video_id, is_del=FALSE_INT) \
                .update(video_snapshot_status=VIDEO_SNAPSHOT_STATUS_FAIL)
            file_storage.safe_delete(_local_temp_path_snapshot)
        file_storage.safe_delete(_local_temp_path_after)    


# @interact_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'default_retry_delay' : 90})
# def snapshot(video_id):
#     logger.info('snapshot video %d ...' % video_id)
#     SNAP_TMP_PATH = 'video_snapshot'
#     SNAP_TMP_PATH_ABS = file_storage.safe_folder(os.path.join(settings.TEMP_DIR, SNAP_TMP_PATH))
#     video = SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).first()
#     if not video:
#         return
#     SysVideo.objects.filter(id=video_id, is_del=FALSE_INT).update(video_snapshot_status=VIDEO_SNAPSHOT_STATUS_ING)
#     media_path = settings.MEDIA_PATH_PROTECT if video.is_protected == TRUE_INT else settings.MEDIA_PATH_PUBLIC
#     video_fname = video.video_url[video.video_url.rfind('/') + 1:]
#     converted_pic_name = video_fname[:video_fname.rfind('.')] + '_snapshot.png'
#
#     relative_path = file_storage.gen_path(os.path.join(media_path, video.user_school.code, 'video_snapshot'), converted_pic_name)
#     if settings.USE_S3:
#         logger.info('download (s3) video %d to snapshot' % video_id)
#         # 下载原始视频到本地临时目录
#         _key = video.video_url
#         _local_temp_path = os.path.join(SNAP_TMP_PATH_ABS, video_fname)
#         _local_temp_path_snapshot = os.path.join(SNAP_TMP_PATH_ABS, converted_pic_name)
#         s3_storage.get_operator().download_file(_key, _local_temp_path)
#
#         is_succ = tools.video_snapshot(_local_temp_path, _local_temp_path_snapshot)
#         if is_succ:
#             logger.info('snapshot video successfully, and start uploading to s3 ...')
#             raw_md5 = s3_storage.get_operator().upload_local_file(_local_temp_path_snapshot, relative_path)
#             logger.info('upload snapshot video to s3 successfully')
#             snapshot_square = Image.open(_local_temp_path_snapshot).size
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT)\
#                 .update(video_snapshot_status=VIDEO_SNAPSHOT_STATUS_SUCC,
#                         video_square='%d,%d' % (snapshot_square[0], snapshot_square[1]),
#                         video_snapshot_url=relative_path)
#         else:
#             logger.error('snapshot video fail')
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT) \
#                 .update(video_snapshot_status=VIDEO_SNAPSHOT_STATUS_FAIL)
#         file_storage.safe_delete(_local_temp_path)
#         file_storage.safe_delete(_local_temp_path_snapshot)
#     else:
#         logger.info('use local video %d to snapshot' % video_id)
#         _local_temp_path_snapshot = os.path.join(SNAP_TMP_PATH_ABS, converted_pic_name)
#
#         is_succ = tools.video_snapshot(os.path.join(settings.BASE_DIR, video.video_url), _local_temp_path_snapshot)
#         if is_succ:
#             logger.info('snapshot video successfully')
#             snapshot_square = Image.open(_local_temp_path_snapshot).size
#             shutil.move(_local_temp_path_snapshot, os.path.join(settings.BASE_DIR, relative_path))
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT) \
#                 .update(video_square='%d,%d' % (snapshot_square[0], snapshot_square[1]),
#                         video_snapshot_status=VIDEO_SNAPSHOT_STATUS_SUCC,
#                         video_snapshot_url=relative_path)
#         else:
#             logger.info('snapshot video fail')
#             SysVideo.objects.filter(id=video_id, is_del=FALSE_INT) \
#                 .update(video_snapshot_status=VIDEO_SNAPSHOT_STATUS_FAIL)
#             file_storage.safe_delete(_local_temp_path_snapshot)


@interact_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'default_retry_delay' : 90})
def convert_voice(voice_id):
    logger.info('convert voice %d ...' % voice_id)
    CONVERT_TMP_PATH = 'voice_convert'
    CONVERT_TMP_PATH_ABS = file_storage.safe_folder(os.path.join(settings.TEMP_DIR, CONVERT_TMP_PATH))
    voice = SysVoice.objects.filter(id=voice_id).first()
    if not voice:
        return
    voice.voice_converted_status = VOICE_CONVERT_STATUS_ING
    voice.save()
    media_path = settings.MEDIA_PATH_PROTECT if voice.is_protected == TRUE_INT else settings.MEDIA_PATH_PUBLIC
    raw_fname = voice.voice_url[voice.voice_url.rfind('/') + 1:]
    converted_fname = raw_fname[:raw_fname.rfind('.')] + '_converted.mp3'
    # 转换后文件保存的相对路径
    relative_path = file_storage.gen_path(os.path.join(media_path, voice.user_school.code, 'voice'), converted_fname)
    if settings.USE_S3:
        logger.info('download (s3) voice %d to convert' % voice_id)
        # 下载原始音频到本地临时目录
        _key = voice.voice_url
        _local_temp_path = os.path.join(CONVERT_TMP_PATH_ABS, raw_fname)
        _local_temp_path_after = os.path.join(CONVERT_TMP_PATH_ABS, converted_fname)
        s3_storage.get_operator().download_file(_key, _local_temp_path)
        # 转码生成新音频文件
        logger.info('convert voice %s to %s' % (_local_temp_path, _local_temp_path_after))
        is_succ = tools.convert_voice_2_mp3(_local_temp_path, _local_temp_path_after)
        if is_succ:
            logger.info('convert voice successfully, and start uploading to s3 ...')
            raw_md5 = s3_storage.get_operator().upload_local_file(_local_temp_path_after, relative_path)
            logger.info('upload converted voice to s3 successfully')
            voice.voice_converted_status = VOICE_CONVERT_STATUS_SUCC
            voice.voice_converted_url = relative_path
            voice.save()
        else:
            logger.info('convert voice fail')
            voice.voice_converted_status = VOICE_CONVERT_STATUS_FAIL
            voice.save()
        file_storage.safe_delete(_local_temp_path)
        file_storage.safe_delete(_local_temp_path_after)
    else:
        logger.info('use local voice %d to convert' % voice_id)
        _local_temp_path_after = os.path.join(CONVERT_TMP_PATH_ABS, converted_fname)
        # 转码生成新音频文件
        is_succ = tools.convert_voice_2_mp3(os.path.join(settings.BASE_DIR, voice.voice_url), _local_temp_path_after)
        if is_succ:
            logger.info('convert voice successfully')
            shutil.move(_local_temp_path_after, os.path.join(settings.BASE_DIR, relative_path))
            voice.voice_converted_status = VOICE_CONVERT_STATUS_SUCC
            voice.voice_converted_url = relative_path
            voice.save()
        else:
            logger.info('convert voice fail')
            voice.voice_converted_status = VOICE_CONVERT_STATUS_FAIL
            voice.save()
            file_storage.safe_delete(_local_temp_path_after)


@interact_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'default_retry_delay' : 90})
def sync_user_data():
    for model_name in settings.MODEL_SYNC_FROM_USER_CENTER:
        from applications.user_center.sync import refresh_table
        refresh_table(model_name, ignore_update_time=False, uc_domain=None)


@interact_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'default_retry_delay' : 90})
def clear_media():
    try:
        from applications.common.services \
            import clear_media_image, clear_media_file, clear_media_video, clear_media_voice
        logger.info('clear redundant media ...')
        clear_media_image()
        clear_media_file()
        clear_media_video()
        clear_media_voice()
        logger.info('clear redundant media end')
    except Exception as e:
        logger.exception(e)

