from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from apps.tasks.models import Task, Comment


class TestTasks(TestCase):
    fixtures = ["database"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.get(email="testuser@gmail.com")
        self.client.force_authenticate(self.user)

    def test_tasks_create(self):
        start_len = len(Task.objects.all())
        response = self.client.post(
            reverse('task-list'),
            {
                "title": "firstname2",
                "description": "lastname2",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(start_len + 1, Task.objects.all().count())
        self.assertEqual(Task.objects.filter(title='firstname2').exists(), True)

    def test_tasks_search(self):
        response = self.client.get(
            reverse('task-list'),
            {'search': 'testuser@example.com'},
            content_type="application/json",
        )
        self.assertContains(response, 'testuser@example.com')

    def test_task_completed(self):
        response = self.client.get(
            reverse('task-completed'),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_task_my(self):
        response = self.client.get(
            reverse('task-my'),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_task_read(self):
        response = self.client.get(
            reverse('task-detail', kwargs={'pk': 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'testuser@example.com')

    def test_task_update(self):
        response = self.client.put(
            reverse('task-detail', kwargs={'pk': 1}),
            data={'owner': self.user.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 1)
        self.assertEqual(Task.objects.filter(owner=1).count(), 1)

    def test_task_complete(self):
        response = self.client.post(
            reverse('task-complete', kwargs={'pk': 2}),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.filter(id=2, status=1).count(), 1)

    def test_task_comments_create(self):
        response = self.client.post(
            reverse('comment-list', kwargs={'task_id': 1}),
            data={'text': 'Task 1 comment'},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(task=1, text='Task 1 comment').count(), 1)
        self.assertEqual(mail.outbox[0].subject, "Your task have been commented")

    def test_task_comments_list(self):
        response = self.client.get(
            reverse('comment-list', kwargs={'task_id': 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
