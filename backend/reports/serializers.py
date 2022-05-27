from rest_framework import serializers
from .models import TimeReport, Ranking

class TimeReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeReport
        fields = '__all__'
        read_only_fields = ('timereport_user_id',)

class RankingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ranking
        fields = '__all__'
        read_only_fields = ('ranking_user_id',)