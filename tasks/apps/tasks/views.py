import os

from django.contrib.auth.models import User
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import filters
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.tasks.models import Task, Comment
from apps.tasks.serializers import TasksSerializer, TasksSerializerList, TaskDetailsSerializer, TaskChangerSerializer, \
     CommentTaskSerializer, CommentTaskSerializerList


class CommentsCustomViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    pass


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TasksSerializerList
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "create":
            return TasksSerializer
        elif self.action == "retrieve":
            return TaskDetailsSerializer
        elif self.action == "update":
            return TaskChangerSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'my':
            queryset = queryset.filter(owner=self.request.user.id)
        elif self.action == 'completed':
            queryset = queryset.filter(status=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=User.objects.filter(id=self.request.user.id).get())

    def perform_update(self, serializer):
        instance = serializer.save()
        task = Task.objects.get(id=instance.id)

        send_mail(
            "You have new task to do",
            f"You have to do '{task.title}'",
            os.environ.get('EMAIL_HOST_USER'),
            [task.owner],
            fail_silently=False
        )

    @action(detail=False, filter_backends=[])
    def my(self, request, *args, **kwargs):

        return self.list(request)

    @action(detail=False, filter_backends=[])
    def completed(self, request, *args, **kwargs):

        return self.list(request)

    @action(detail=True, methods=['post'])
    @swagger_auto_schema(request_body=no_body)
    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = True
        instance.save()

        if Comment.objects.filter(task=instance.id):
            send_mail(
                "Your task have been done",
                f"You commented task '{instance.title}' have been done.",
                os.environ.get('EMAIL_HOST_USER'),
                [{instance.owner}],
                fail_silently=False
            )
        return Response({"status": "task was made"})


class CommentViewSet(CommentsCustomViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentTaskSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CommentTaskSerializerList
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset().filter(**self.kwargs)

    def perform_create(self, serializer):
        instance = serializer.save(task_id=self.kwargs['task_id'])

        send_mail(
            "Your task have been commented",
            f"You have new comment on '{instance.task.title}'",
            os.environ.get('EMAIL_HOST_USER'),
            [instance.task.owner],
            fail_silently=False
        )
