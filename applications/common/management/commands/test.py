# -*- coding=utf-8 -*-

import logging

import requests
from django.core.management.base import BaseCommand, CommandError

from applications.common import services

logger = logging.getLogger('django_command')


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        files = {
            "voice": ('test.amr', open('/home/tmp/test.amr', "rb")),
        }
        upload_request_path = 'http://127.0.0.1:8002/api/common/upload/voice'
        logger.info('visit local-server %s to upload wx-voice' % upload_request_path)
        response = requests.post(
            upload_request_path,
            cookies={'sessionid': '736uf9k0sry6zf21cy7bmkn99reh6vdp'},
            data={'duration': '20'},
            files=files,
            timeout=30)
        return response
