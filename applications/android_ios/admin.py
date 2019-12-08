# -*- coding: utf-8 -*-

from django.contrib import admin

from applications.android_ios.models import *


# for models.MobileDef
class MobileDefAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'latest_version', 'latest_version_url', 'support_version', 'update_time', 'is_del']
    readonly_fields = ['id', 'update_time', 'create_time']

admin.site.register(MobileDef, MobileDefAdmin)


# for models.MobileHistory
class MobileHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'version', 'download_count', 'create_time', 'is_del']
    readonly_fields = ['id', 'update_time', 'create_time']
    list_filter = ['is_del', 'type']
admin.site.register(MobileHistory, MobileHistoryAdmin)


# for models.MobileService
class MobileServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'support_user_type', 'support_device', 'is_heartbeat', 'update_time','is_del']
    readonly_fields = ['id', 'update_time', 'create_time']

admin.site.register(MobileService, MobileServiceAdmin)




