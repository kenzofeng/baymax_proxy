from django.contrib import admin

from .models import Project, Job, Job_Test, Node, Job_Log, Job_Test_Distributed_Result, Job_Test_Result, Test_Map, Mail, \
    Type


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


class NodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'aws_instance_id', 'public_ip', 'private_ip', 'port', 'status']
    actions = ['Set_Status_Done']

    def Set_Status_Done(self, request, queryset):
        queryset.update(status='Done')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


class job_test_Inline(admin.TabularInline):
    model = Job_Test
    extra = 3


class JobTestsAdmin(admin.ModelAdmin):
    list_display = ['job', 'robot_parameter', 'name', 'status']


class JobAdmin(admin.ModelAdmin):
    list_display = ['pk', 'project', 'status', 'start_time', 'end_time', 'disable']
    inlines = [job_test_Inline]


class Job_LogAdmin(admin.ModelAdmin):
    list_display = ['job']


class Test_Map_Admin(admin.ModelAdmin):
    list_display = ['project', 'test', 'use', 'robot_parameter']


class MailAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Job_Test, JobTestsAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Job_Log, Job_LogAdmin)
admin.site.register(Job_Test_Distributed_Result)
admin.site.register(Job_Test_Result)
admin.site.register(Test_Map, Test_Map_Admin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Type, TypeAdmin)
