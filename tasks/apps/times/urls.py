from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.times.views import TimeViewSet, TaskTimeViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'time', TimeViewSet)
router.register(r'tasks/(?P<task_id>\d+)?/logs', TaskTimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
