from django.core.management import BaseCommand
from schedules.models import TodaySchedule
from accounts.views import send_mail
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail("psa9456@naver.com", '사만코 운동 알림 🔥', 
            '운동 할 시간입니다 🧘‍♀️')
            