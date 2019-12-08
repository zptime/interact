# -*- coding: utf-8 -*-

from django.contrib import admin
from applications.common.models import *


# for models.SysImage
class SysImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_del', 'image_name', 'image_size', 'image_square', 'user_school', 'update_time']
    readonly_fields = ['id', 'update_time', 'create_time']
    list_filter = ['is_del', 'user_school']
    search_fields = ['image_name']

admin.site.register(SysImage, SysImageAdmin)


# for models.SysVoice
class SysVoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_del', 'voice_name', 'voice_duration', 'voice_size', 'voice_type', 'update_time', 'is_del']
    list_filter = ['is_del']
    readonly_fields = ['id', 'update_time', 'create_time']
    search_fields = ['voice_name']

admin.site.register(SysVoice, SysVoiceAdmin)


# for models.SysVideo
class SysVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_del', 'video_name', 'video_duration', 'video_size', 'update_time']
    list_filter = ['is_del']
    readonly_fields = ['id', 'update_time', 'create_time']
    search_fields = ['video_name']

admin.site.register(SysVideo, SysVideoAdmin)


# for models.SysFile
class SysFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_del', 'is_del', 'file_name', 'file_url', 'file_size', 'file_type', 'update_time']
    list_filter = ['is_del', 'file_type']
    readonly_fields = ['id', 'update_time', 'create_time']
    search_fields = ['file_name']

admin.site.register(SysFile, SysFileAdmin)



