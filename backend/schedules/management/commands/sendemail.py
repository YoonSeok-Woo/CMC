from django.core.management import BaseCommand
from schedules.models import TodaySchedule
from accounts.views import send_mail
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 지금 보내야하는 알림이 있다면
        today_schedules = list(TodaySchedule.objects.filter(todayschedule_time__hour=datetime.now().hour,
            todayschedule_time__minute=(datetime.now().minute)))

        for schedule in today_schedules:
            schedule_title = schedule.todayschedule_title
            user_email = schedule.todayschedule_user_id

            send_mail(user_email, '사만코 운동 알림 🔥', 
        schedule_title + '운동 할 시간입니다 🧘‍♀️')
            
