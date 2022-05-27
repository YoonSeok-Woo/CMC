from django.db import models
from django.conf import settings

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    schedule_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='schedule', on_delete=models.CASCADE)
    schedule_title = models.CharField(max_length=50)
    schedule_time = models.DateTimeField()

class TodaySchedule(models.Model):
    todayschedule_id = models.AutoField(primary_key=True)
    todayschedule_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='today_schedule', on_delete=models.CASCADE)
    todayschedule_title = models.CharField(max_length=50)
    todayschedule_time = models.DateTimeField()