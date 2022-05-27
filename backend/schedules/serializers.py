from rest_framework import serializers
from .models import Schedule, TodaySchedule

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ('schedule_user_id',)

class TodayScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodaySchedule
        fields = '__all__'
        read_only_fields = ('todayschedule_user_id',)