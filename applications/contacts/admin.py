# -*- coding: utf-8 -*-

from django.contrib import admin

from applications.contacts.models import *


# for models.Group
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'account', 'user_type', 'school', 'update_time', 'is_del']
    list_filter = ['school', 'is_del']
    readonly_fields = ['id', 'account', 'user_type', 'school', 'update_time', 'create_time']
    search_fields = ['name']

admin.site.register(Group, GroupAdmin)


# for models.GroupMember
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'account', 'user_type', 'school', 'update_time', 'is_del']
    readonly_fields = ['id', 'account', 'user_type', 'school', 'update_time', 'create_time']
    list_filter = ['school', 'is_del']

admin.site.register(GroupMember, GroupMemberAdmin)






