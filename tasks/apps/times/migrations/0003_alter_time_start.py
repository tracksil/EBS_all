# Generated by Django 4.1.6 on 2023-02-21 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0002_alter_time_minutes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 21, 11, 14, 32, 878375, tzinfo=datetime.timezone.utc)),
        ),
    ]
