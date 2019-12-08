# -*- coding=utf-8 -*-

import logging

from django.core.management.base import BaseCommand, CommandError

from applications.common import services
from utils import auth_check

logger = logging.getLogger('django_command')


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--class_id', help="")

    def handle(self, *args, **options):
        class_id = options['class_id']
        clazz = auth_check.check_get_class(int(class_id))
        members = services.get_class_member(clazz, flat=True)
        logger.info('class %s member count: %d: ' % (class_id, len(members)))
        logger.info(members)
