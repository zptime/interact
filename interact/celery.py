# -*- coding=utf-8 -*-

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# 环境变量设定需要在引入非第三方包之前
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "interact.settings")

interact_app = Celery('interact')

from django.conf import settings
interact_app.conf.broker_url = settings.CELERY_BROKER_BACKEND   # 'redis://127.0.0.1:6379/0'
interact_app.conf.timezone = 'Asia/Shanghai'

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
interact_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
interact_app.autodiscover_tasks()


@interact_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@interact_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # 本地引用以防止循环引用
    from applications.common.tasks import sync_user_data, clear_media, report

    # 删除残留的临时文件
    sender.add_periodic_task(
        crontab(hour=1, minute=0),  # Execute daily clean at midnight.
        clear_media.s(),
    )

    # 周期性同步用户中心数据
    sender.add_periodic_task(60 * 2, sync_user_data.s())



