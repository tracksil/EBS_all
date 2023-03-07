import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.tasks.models import Task
from apps.times.models import Time


class Command(BaseCommand):
    help = 'Adds 25,000 random tasks and 50,000 time logs'

    def handle(self, *args, **options):
        if not User.objects.exists():
            user = User.objects.create_user(username='default_user', password='password')
        else:
            user = None

        tasks = []
        for i in range(25000):
            task = Task(
                title=f'Task {i}',
                description=f'This is task number {i}',
                status=random.choice([True, False]),
                owner=user or User.objects.order_by('?').first()
            )
            tasks.append(task)

        Task.objects.bulk_create(tasks)

        times = []
        for i in range(50000):
            time = Time(
                start=timezone.now(),
                end=None,
                minutes=random.randint(1, 120),
                task=Task.objects.order_by('?').first(),
                owner=user or User.objects.order_by('?').first()
            )
            times.append(time)

        Time.objects.bulk_create(times)

        self.stdout.write(self.style.SUCCESS('Successfully added 25,000 tasks and 50,000 time logs'))
