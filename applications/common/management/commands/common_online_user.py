# -*- coding=utf-8 -*-

import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from applications.common import services
from utils import auth_check

logger = logging.getLogger('django_command')


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--verbose', help="")

    def handle(self, *args, **options):
        from django.core.cache import cache
        keys = cache.keys(settings.LASTSEEN_PREFIX + "*")
        # iter = cache.iter_keys(settings.LASTSEEN_PREFIX + "*")
        logger.info('%d users online' % len(keys))
        verbose = options['verbose']
        if verbose:
            logger.info('users_online_list:')
            for each in keys:
                logger.info(cache.get(each))



