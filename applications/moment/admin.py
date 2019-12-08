# -*- coding: utf-8 -*-

from django.contrib import admin

from applications.moment.models import *


class MomentBaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'user_type', 'user_school', 'content', 'moment_type', 'has_voice', 'has_image', 'has_video', 'has_file', 'read_count', 'like_count', 'reply_count', 'create_time', 'update_time', 'is_del']
    list_filter = ['user_school']  # 过滤字段
    search_fields = ['account', 'content']

admin.site.register(MomentBase, MomentBaseAdmin)


class MomentCircleSchoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'moment', 'create_time', 'update_time', 'is_del']
    list_filter = ['id']  # 过滤字段
    search_fields = ['moment']

admin.site.register(MomentCircleSchool, MomentCircleSchoolAdmin)


class MomentCircleClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'moment', 'clazz', 'create_time', 'update_time', 'is_del']
    list_filter = ['id']  # 过滤字段
    search_fields = ['moment', 'clazz']

admin.site.register(MomentCircleClass, MomentCircleClassAdmin)