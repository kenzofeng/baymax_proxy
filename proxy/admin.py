# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Svn, Project, Job, Job_Test, Node


class SvnAdmin(admin.ModelAdmin):
    list_display = ['name']


class NodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'status']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


class job_test_Inline(admin.TabularInline):
    model = Job_Test
    extra = 3


class JobTestsAdmin(admin.ModelAdmin):
    list_display = ['job', 'robot_parameter', 'name', 'status']


class JobAdmin(admin.ModelAdmin):
    list_display = ['project', 'status', 'start_time', 'end_time']
    inlines = [job_test_Inline]


admin.site.register(Svn, SvnAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Job_Test, JobTestsAdmin)
admin.site.register(Node, NodeAdmin)
