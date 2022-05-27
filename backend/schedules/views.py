from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import TodaySchedule, Schedule
from .serializers import ScheduleSerializer, TodayScheduleSerializer
from datetime import datetime


# Create your views here.
@api_view(['POST'])
def schedule(request):

    date_time_str = request.data.get('schedule_time')
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

    # 만약 오늘 스케줄을 생성한다면
    if date_time.date() == datetime.today().date():
        todayserializer = TodayScheduleSerializer(data =
            {'todayschedule_title' : request.data.get('schedule_title'),
            'todayschedule_time': date_time})
        if todayserializer.is_valid(raise_exception=True):
            todayserializer.save(todayschedule_user_id=request.user)
    serializer = ScheduleSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(schedule_user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT'])
def schdeule_detail(request, schedule_pk):

    schedule = get_object_or_404(Schedule, schedule_id=schedule_pk)

    # 권한 확인
    if not request.user.schedule.filter(schedule_id=schedule_pk).exists():
        return Response({'권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        # 날짜 검사
        date_time_str = request.data.get('schedule_time')   
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        # 오늘 일정 수정
        if date_time.date() == datetime.today().date():
            today_schedule = TodaySchedule.objects.filter(todayschedule_title = schedule.schedule_title, todayschedule_user_id = request.user.id)[0]
            print(today_schedule)
            todayserializer = TodayScheduleSerializer(today_schedule,
                        data = {'todayschedule_title' : request.data.get('schedule_title'),
                                'todayschedule_time' : request.data.get('schedule_time')
                                })
            if todayserializer.is_valid(raise_exception=True):
                todayserializer.save()  

        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)                  

    if request.method == 'DELETE':
        # 날짜 검사
        date_time = schedule.schedule_time
        # 오늘 일정 삭제
        if date_time.date() == datetime.today().date():
            today_schedule = TodaySchedule.objects.filter(todayschedule_title = schedule.schedule_title, todayschedule_user_id = request.user.id)
            today_schedule.delete()
        schedule.delete()
        return Response({'id': schedule_pk}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def monthly_schedule(request, year, month):

    schedule_list = list(Schedule.objects.filter(
        Q (schedule_user_id=request.user.id) & 
        Q (schedule_time__year=year, schedule_time__month=month)))
        
    serializers = ScheduleSerializer(schedule_list, many=True)
    return Response(serializers.data)