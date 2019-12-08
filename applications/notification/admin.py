#!/usr/bin/env python
# coding=utf-8
from django.contrib import admin
from models import *


class NotifyBaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'user_type', 'user_school', 'intro', 'content', 'type', 'create_time', 'is_del']
    exclude = ('title', 'has_voice', 'has_image', 'has_video', 'has_file', 'update_time')
    list_filter = ['account', 'user_type', 'user_school', 'type', 'is_del']

admin.site.register(NotifyBase, NotifyBaseAdmin)


