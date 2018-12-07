from django.contrib import admin

from .models import Svn, Project, Job, Job_Test, Node, Job_Log


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
    list_display = ['pk', 'project', 'status', 'start_time', 'end_time']
    inlines = [job_test_Inline]


class Job_LogAdmin(admin.ModelAdmin):
    list_display = ['job']


admin.site.register(Svn, SvnAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Job_Test, JobTestsAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Job_Log, Job_LogAdmin)
