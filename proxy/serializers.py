from models import Project, Test_Map, Node, Job, Job_Test
from rest_framework import serializers
import pytz

sh = pytz.timezone('Asia/Shanghai')


class JobSerializer(serializers.ModelSerializer):
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    tests = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('project', 'start', 'end', 'status', 'tests')

    def get_start(self, obj):
        return obj.start_time.astimezone(sh).strftime("%Y-%m-%d %H:%M:%S")

    def get_end(self, obj):
        return obj.end_time.astimezone(sh).strftime("%Y-%m-%d %H:%M:%S")

    def get_tests(self, obj):
        return JobTestSerializer(obj.job_test_set.all(), many=True).data


class JobTestSerializer(serializers.ModelSerializer):
    log = serializers.SerializerMethodField()

    class Meta:
        model = Job_Test
        fields = ('id', 'log', 'name', 'robot_parameter', 'project_branch', 'project_sha', 'status', 'revision_number')

    def get_log(self, obj):
        return obj.job_test_result.id


class ProjectSerializer(serializers.ModelSerializer):
    nodes = serializers.SerializerMethodField()
    maps = serializers.SerializerMethodField()
    allnodes = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('pk', 'name', 'email', 'nodes', 'maps', 'allnodes')

    def get_nodes(self, obj):
        return NodeSerializer(obj.node_set.all(), many=True).data

    def get_maps(self, obj):
        return TestMapSerializer(Test_Map.objects.filter(project=obj.name), many=True).data

    def get_allnodes(self, obj):
        return NodeSerializer(Node.objects.all(), many=True).data


class TestMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test_Map
        fields = ('pk', 'project', 'test', 'testurl', 'robot_parameter', 'use')


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("host", 'name')
