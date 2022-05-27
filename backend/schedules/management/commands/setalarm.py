from django.core.management import BaseCommand
from ...models import Schedule, TodaySchedule
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        TodaySchedule.objects.all().delete()
        schedule_list = Schedule.objects.all()

        # 오늘 알림을 보내야 하는 스케줄만
        for schedule in schedule_list:
            if schedule.schedule_time.date() >= datetime.date.today():
                TodaySchedule(
                    todayschedule_user_id = schedule.schedule_user_id,
                    todayschedule_title = schedule.schedule_title,
                    todayschedule_time = schedule.schedule_time,
                ).save()