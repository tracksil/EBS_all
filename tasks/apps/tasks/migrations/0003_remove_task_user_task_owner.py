# Generated by Django 4.1.6 on 2023-02-15 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.IntegerField(default=1),
        ),
    ]
