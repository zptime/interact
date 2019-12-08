# -*- coding=utf-8 -*-

import logging
from django.core.management.base import BaseCommand, CommandError

from applications.common import services

logger = logging.getLogger('django_command')


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        all_in_use = True
        images = services.get_media_image_redundant()
        if len(images) > 0:
            logger.info('%d images not use, need remove ' % len(images))
            logger.info(images)
            all_in_use= False

        videos = services.get_media_video_redundant()
        if len(videos) > 0:
            logger.info('%d videos not use, need remove ' % len(videos))
            logger.info(videos)
            all_in_use = False

        voices = services.get_media_voice_redundant()
        if len(voices) > 0:
            logger.info('%d voices not use, need remove ' % len(voices))
            logger.info(voices)
            all_in_use = False

        files = services.get_media_file_redundant()
        if len(files) > 0:
            logger.info('%d files not use, need remove ' % len(files))
            logger.info(files)
            all_in_use = False

        if all_in_use:
            logger.info('all media are in use')
