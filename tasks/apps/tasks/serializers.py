from apps.tasks.models import Task, Comment
from rest_framework import serializers


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
        )


class TasksSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
        )


class TaskDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskChangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "owner"
        )


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
        )


class CommentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "text",
        )


class CommentTaskSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
        )
