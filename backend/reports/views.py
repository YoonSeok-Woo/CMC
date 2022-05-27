from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import TimeReport, Ranking
from .serializers import TimeReportSerializer, RankingSerializer
from django.db.models import Q, Max
import datetime 
from dateutil.relativedelta import relativedelta

# Create your views here.
@api_view(['GET'])
def timereportlist_get(request):
    start_date = datetime.datetime.today()-relativedelta(years=1)
    end_date = datetime.date.today()
    timereport_list = list(TimeReport.objects.filter(
        Q (timereport_user_id=request.user.id) & 
        Q (timereport_day__range=[start_date, end_date])))
    serializers = TimeReportSerializer(timereport_list, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def timereport_lastday(request):
    time_report = TimeReport.objects.filter(timereport_user_id=request.user).aggregate(Max('timereport_day'))
    return Response(time_report)

@api_view(['POST'])
def timereport(request):

    if TimeReport.objects.filter(Q(timereport_user_id = request.user) & Q(timereport_day=datetime.date.today())).exists():
        report = get_object_or_404(TimeReport, timereport_user_id = request.user, timereport_day = datetime.date.today())
        serializer = TimeReportSerializer(report, data={
            'timereport_day' : datetime.date.today(),
            'timereport_time' : report.timereport_time + int(request.data.get('timereport_time')),
        })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        # 랭킹 업데이트 (그날의 두번째 운동이니까 시간만 업데이트)
        ranking = Ranking.objects.get(ranking_user_id=request.user)
        rank_serializer = RankingSerializer(ranking, data={
            'ranking_time' : ranking.ranking_time + int(request.data.get('timereport_time')),
        })
        if rank_serializer.is_valid(raise_exception=True):
            rank_serializer.save()

        return Response(serializer.data)

    else:
        serializer = TimeReportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(timereport_user_id = request.user)
            serializer.save()

        # 랭킹 업데이트 (그날의 처음 운동이니까 날짜와 시간 모두 업데이트)
        if Ranking.objects.filter(ranking_user_id=request.user).exists():
            ranking = Ranking.objects.get(ranking_user_id=request.user)
            # 만약 마지막 운동 날짜가 어제라면
            if ranking.ranking_last_day == datetime.date.today()-datetime.timedelta(1):
                consecutive_days = ranking.ranking_consecutive_days + 1
            else:
                consecutive_days = 0

            max_consecutive_days = max(ranking.ranking_max_consecutive_days, ranking.ranking_consecutive_days + 1)
            rank_serializer = RankingSerializer(ranking, data={
                'ranking_time' : ranking.ranking_time + int(request.data.get('timereport_time')),
                'ranking_day' : ranking.ranking_day + 1,
                'ranking_consecutive_days' : consecutive_days,
                'ranking_max_consecutive_days' : max_consecutive_days,
            })
        else:
            rank_serializer = RankingSerializer(data={
                'ranking_time' : int(request.data.get('timereport_time')),
                'ranking_day' : 1,
                'ranking_consecutive_days' : 1,
                'ranking_max_consecutive_days' : 1,
            })
        if rank_serializer.is_valid(raise_exception=True):
            rank_serializer.save(ranking_user_id=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def rank(request):

    total = len(get_user_model().objects.all())
    if Ranking.objects.filter(ranking_user_id=request.user).exists():
        ranking = Ranking.objects.get(ranking_user_id=request.user)
        time_ranking = Ranking.objects.filter(ranking_time__lte = ranking.ranking_time).count()
        days_ranking = Ranking.objects.filter(ranking_day__lte = ranking.ranking_day).count()
        consecutive_days_ranking = Ranking.objects.filter(ranking_max_consecutive_days__lte = ranking.ranking_max_consecutive_days).count()
        context = {
            'time_ranking' : time_ranking,
            'days_ranking' : days_ranking,
            'consecutive_days_ranking' : consecutive_days_ranking,
            'total' : total,
        }
        return Response(context)
    else:
        context = {
            'time_ranking' : 0,
            'days_ranking' :0,
            'consecutive_days_ranking' : 0,
            'total' : total,
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)
