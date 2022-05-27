from django.contrib import admin
from .models import Schedule, TodaySchedule

# Register your models here.
admin.site.register(Schedule)
admin.site.register(TodaySchedule)