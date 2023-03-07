from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from apps.times.models import Time


class TestTimes(TestCase):
    fixtures = ["database"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.get(email="testuser@gmail.com")
        self.client.force_authenticate(self.user)

    def test_time_start(self):
        start_len = len(Time.objects.all())
        response = self.client.get(
            reverse('time-start', kwargs={'task_id': 2}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(start_len + 1, Time.objects.all().count())

        response = self.client.get(
            reverse('time-start', kwargs={'task_id': 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "You already work on this task")

    def test_time_save_log(self):
        start_len = Time.objects.all().count()
        response = self.client.post(
            '/time',
            data={
                "start": "2023-02-23",
                "minutes": 90,
                "task": 1,
                "owner": 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Time.objects.all().count(), start_len+1)

    def test_time_end(self):

        response = self.client.get(
            reverse('time-end', kwargs={'task_id': 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Time.objects.filter(end=None).count(), 1)

    @freeze_time('2023-02-22')
    def test_time_top(self):
        cache.clear()
        response = self.client.get(
            reverse('time-top'),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertGreater(response.data[0]['sum_minutes'], response.data[1]['sum_minutes'])

    def test_time_month(self):
        response = self.client.get(
            reverse('time-month'),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_time_list_time(self):
        response = self.client.get(
            reverse('time-list'),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_task_logs_list(self):
        response = self.client.get(
            reverse('time-list', kwargs={'task_id': 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
