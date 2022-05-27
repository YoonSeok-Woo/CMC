from django.db import models
from django.conf import settings

class TimeReport(models.Model):
    timereport_id = models.AutoField(primary_key=True)
    timereport_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='time_report', on_delete=models.CASCADE)
    timereport_day = models.DateField(auto_now=True)
    timereport_time = models.IntegerField()

class Ranking(models.Model):
    ranking_user_id = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='ranking', on_delete=models.CASCADE, primary_key=True)
    ranking_time = models.IntegerField(default=0)
    ranking_day = models.IntegerField(default=0)
    ranking_last_day = models.DateField(auto_now_add=True)
    ranking_consecutive_days = models.IntegerField(default=0)
    ranking_max_consecutive_days = models.IntegerField(default=0)