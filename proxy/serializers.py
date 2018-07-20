from models import Project, Test_Map, Node
from rest_framework import serializers


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
