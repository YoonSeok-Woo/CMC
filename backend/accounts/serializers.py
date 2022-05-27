from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'user_phone', 'user_name',)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'user_name', 'user_type', 'user_profile_image', 'user_notice', 'user_phone', 'user_kakao_id',)


class ProfilePutSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('user_name', 'user_profile_image', 'user_notice', 'user_phone', 'user_kakao_id',)