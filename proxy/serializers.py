from models import Project, Test_Map, Node, Job, Job_Test, Node
from rest_framework import serializers
import pytz

sh = pytz.timezone('Asia/Shanghai')


class JobTestSerializer(serializers.ModelSerializer):
    log = serializers.SerializerMethodField()

    class Meta:
        model = Job_Test
        fields = ('id', 'log', 'name', 'app', 'robot_parameter', 'status', 'revision_number')

    def get_log(self, obj):
        return obj.job_test_result.id if hasattr(obj,"job_test_result") else ""


class JobSerializer(serializers.ModelSerializer):
    job_test_set = JobTestSerializer(many=True, read_only=True)
    servers = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('pk', 'project', 'servers', 'start_time', 'end_time', 'status', 'job_test_set')

    def get_servers(self, obj):
        return [{"name": server, "ip": Node.objects.get(name=server).host} for server in obj.servers.split(":")]

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
        fields = ('pk', 'name', 'email', 'nodes', 'maps')

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
        maps = Test_Map.objects.filter(project=instance.pk)
        for m in maps:
            m.delete()
        for map in validated_data.get('maps'):
            m = Test_Map()
            m.project = instance.pk
            m.test = map['test']
            m.testurl = map['testurl']
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
        fields = ('pk', 'project', 'test', 'testurl', 'robot_parameter', 'app', 'use')
