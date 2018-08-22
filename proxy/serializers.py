from models import Project, Test_Map, Node, Job, Job_Test
from rest_framework import serializers
import pytz

sh = pytz.timezone('Asia/Shanghai')


class JobTestSerializer(serializers.ModelSerializer):
    log = serializers.SerializerMethodField()

    class Meta:
        model = Job_Test
        fields = ('id', 'log', 'name', 'robot_parameter', 'project_branch', 'project_sha', 'status', 'revision_number')

    def get_log(self, obj):
        return obj.job_test_result.id


class JobSerializer(serializers.ModelSerializer):
    job_test_set = JobTestSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ('pk','project', 'start_time', 'end_time', 'status', 'job_test_set')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('job_test_set')
        return queryset


class ProjectSerializer(serializers.ModelSerializer):
    nodes = serializers.SerializerMethodField()
    maps = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('pk', 'name', 'email', 'nodes', 'maps')

    def get_nodes(self, obj):
        return [node.name for node in  obj.node_set.all()]

    def get_maps(self, obj):
        return TestMapSerializer(Test_Map.objects.filter(project=obj.name), many=True).data

    def update(self, instance, validated_data):
        # instance.job_status =validated_data.get('job_status', instance.job_status)
        # instance.job_cron = validated_data.get('job_cron', instance.job_cron)
        # instance.save()
        return instance

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('node_set')
        return queryset


class TestMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_Map
        fields = ('pk', 'project', 'test', 'testurl', 'robot_parameter', 'use')


