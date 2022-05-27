from django.core.management import BaseCommand
from schedules.models import TodaySchedule
from django.contrib.auth import get_user_model
from datetime import datetime
import requests
import json

class Command(BaseCommand):

    def handle(self, *args, **options):

        code = ""

        # 토큰 발급
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type" : "authorization_code",
            "client_id" : "",
            "redirect_url" : "http://localhost:8000/api/v1/schedules/alarm",
            "code" : code
        }
        response = requests.post(url, data=data).json()
        access_token = response.get("access_token")

        # 친구 목록 가져오기
        friend_list_url = "https://kapi.kakao.com/v1/api/talk/friends" 
        header = {
            "Authorization": "Bearer " + access_token
        }

        result = json.loads(requests.get(friend_list_url, headers=header).text)
        friends_list = result.get("elements")
        
        id_list = {}
        for friend in friends_list:
            friend_kakao_id = friend.get('id')
            friend_uuid = friend.get("uuid")
            id_list[friend_kakao_id] = friend_uuid

        # 지금 보내야하는 알림이 있다면
        today_schedules = list(TodaySchedule.objects.filter(todayschedule_time__month=datetime.now().hour-12,
            todayschedule_time__minute=datetime.now().minute))

        for schedule in today_schedules:
            schedule_title = schedule.todayschedule_title
            user_email = schedule.todayschedule_user_id
            user = get_user_model().objects.get(email=user_email)
            kakao_id = user.user_kakao_id
            uuid = id_list.get(int(kakao_id))

            # 메시지 보내기
            url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            data = {
                "receiver_uuids": '["{}"]'.format(uuid),
                "template_object" : json.dumps({ "object_type" : "text",
                                                "text" : schedule_title + "운동 할 시간입니다",
                                                "link" : {
                                                            "web_url" : "http://j6a502.p.ssafy.io/",
                                                            "mobile_web_url" : "http://j6a502.p.ssafy.io/"
                                                        }
                })
            }

            response = requests.post(url, headers=headers, data=data)