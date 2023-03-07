from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tasks.views import TaskViewSet, CommentViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'tasks/(?P<task_id>\d+)?/comments', CommentViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
