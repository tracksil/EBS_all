from django.db.models import Sum
from rest_framework import serializers

from apps.times.models import Time


class TimeTaskSerializer(serializers.ModelSerializer):
    sum_minutes = serializers.SerializerMethodField()

    def get_sum_minutes(self, obj):
        return obj.task.time_set.aggregate(sum_minutes=Sum('minutes'))['sum_minutes']

    class Meta:
        model = Time
        fields = (
            'task',
            'sum_minutes',
        )


class TimeTaskSerializerLog(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = (
            'start',
            'minutes',
            'task',
            'owner',
        )


class TimeTaskSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = (
            'start',
            'end',
            'minutes',
            'owner',
        )
