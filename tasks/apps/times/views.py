from django.db.models import Sum
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.pagination import CustomPagination
from apps.times.models import Time
from apps.times.serializers import TimeTaskSerializer, TimeTaskSerializerList, TimeTaskSerializerLog


class TimeCustomViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    pass


class TimeCustomTaskViewSet(mixins.ListModelMixin,
                            GenericViewSet):
    pass


class TimeViewSet(TimeCustomViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeTaskSerializer
    lookup_field = 'task_id'
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return TimeTaskSerializerLog
        else:
            return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'month':
            queryset = queryset.filter(owner=self.request.user, start__month=timezone.now().month)
        elif self.action == 'top':
            queryset = queryset.filter(start__month=timezone.now().month)
        return queryset

    @action(detail=False)
    def month(self, request, *args, **kwargs):
        return self.list(request)

    @action(detail=False, pagination_class=None)
    @method_decorator(cache_page(60))
    def top(self, request, *args, **kwargs):

        task_minutes = (
            self.get_queryset().values('task')
            .annotate(sum_minutes=Sum('minutes'))
            .values('task__id', 'task__title', 'sum_minutes')
        )

        top_tasks = task_minutes.order_by('-sum_minutes')[:20]

        return Response(top_tasks)


class TaskTimeViewSet(TimeCustomTaskViewSet):
    queryset = Time.objects.all()
    serializer_class = TimeTaskSerializerList
    lookup_field = 'task_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'end':
            queryset = queryset.filter(**self.kwargs, minutes=0, owner=self.request.user)
        else:
            queryset = queryset.filter(**self.kwargs)
        return queryset

    @action(detail=False, pagination_class=None)
    def start(self, request, *args, **kwargs):
        times, created = self.get_queryset().get_or_create(
            task_id=self.kwargs['task_id'],
            owner=request.user,
            minutes=0
        )
        if created:
            return Response(status.HTTP_201_CREATED)
        else:
            return Response("You already work on this task", status.HTTP_400_BAD_REQUEST)

    @action(detail=False, pagination_class=None)
    def end(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.end = timezone.now()
        instance.minutes = int((instance.end - instance.start).total_seconds() / 60)
        instance.save()

        return Response(status.HTTP_200_OK)
