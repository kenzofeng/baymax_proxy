import pytz
from rest_framework import serializers

from .models import Project, Test_Map, Job, Job_Test, Node

sh = pytz.timezone('Asia/Shanghai')


class JobTestSerializer(serializers.ModelSerializer):
    log = serializers.SerializerMethodField()

    class Meta:
        model = Job_Test
        fields = ('id', 'log', 'name', 'app', 'robot_parameter', 'status', 'revision_number')

    def get_log(self, obj):
        return obj.job_test_result.id if hasattr(obj, "job_test_result") else ""


class JobSerializer(serializers.ModelSerializer):
    job_test_set = JobTestSerializer(many=True, read_only=True)
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'pk', 'project', 'servers', 'start_time', 'end_time', 'status', 'job_test_set', 'comments',
            'project_version')

    def get_start_time(self, obj):
        return obj.start_time.astimezone(sh).strftime("%Y-%m-%d %H:%M:%S") if obj.start_time is not None else ""

    def get_end_time(self, obj):
        return obj.end_time.astimezone(sh).strftime("%Y-%m-%d %H:%M:%S") if obj.end_time is not None else ""

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('job_test_set')
        return queryset


class ProjectSerializer(serializers.ModelSerializer):
    nodes = serializers.SerializerMethodField(read_only=False)
    maps = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = Project
        fields = ('pk', 'name', 'email', 'version', 'nodes', 'maps')

    def get_nodes(self, obj):
        return [node.name for node in obj.node_set.all()]

    def get_maps(self, obj):
        return TestMapSerializer(Test_Map.objects.filter(project=obj.name), many=True).data

    def validate(self, attrs):
        attrs['maps'] = self.initial_data['maps']
        attrs['nodes'] = self.initial_data['nodes']
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        instance.version = validated_data.get('version')
        maps = Test_Map.objects.filter(project=instance.pk)
        for m in maps:
            m.delete()
        for map in validated_data.get('maps'):
            m = Test_Map()
            m.project = instance.pk
            m.test = map['test']
            m.source_type = map['source_type']
            m.source_url = map['source_url']
            m.source_branch = map['source_branch']
            m.robot_parameter = map['robot_parameter']
            m.app = map['app']
            m.use = map['use']
            m.save()
        instance.node_set.clear()
        for node in validated_data.get('nodes'):
            n = Node.objects.get(name=node)
            n.projects.add(instance)
            n.save()
        instance.save()
        return instance

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('node_set')
        return queryset


class TestMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_Map
        fields = (
        'pk', 'project', 'test', 'source_type', 'source_url', 'source_branch', 'robot_parameter', 'app', 'use')
