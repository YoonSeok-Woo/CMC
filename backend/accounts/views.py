from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import random
import requests
from .models import User
from .serializers import UserSerializer, ProfileSerializer, ProfilePutSerializer

# smtp
from email.message import EmailMessage
from smtplib import SMTP_SSL
from pathlib import Path

# kakao login
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# google login
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.models import SocialAccount

BASE_URL = 'https://j6a502.p.ssafy.io'
BASE_SERVER_URL = 'https://j6a502.p.ssafy.io:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + "googlecallback"

# 이메일 전송
def send_mail(받는사람, 제목, 본문, 첨부파일=False):
    MY_ID = settings.EMAIL_HOST_USER
    MY_PW = settings.EMAIL_HOST_PASSWORD

    # 템플릿 생성
    msg = EmailMessage()
    # 보내는 사람 / 받는 사람 / 제목 입력
    msg["From"] = MY_ID
    msg["To"] = 받는사람
    msg["Subject"] = 제목
    # 본문 구성
    msg.set_content(본문)
    
    # 파일 첨부
    if 첨부파일:
        파일명 = Path(첨부파일).name
        with open(첨부파일, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=파일명)
            msg.add_header('Content-Disposition', 'attachment', filename=파일명)
    with SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MY_ID, MY_PW)
        smtp.send_message(msg)

# 인증코드 만들기
def email_random_code():
    string_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    random_code = ""
    
    for _ in range(8):
        random_code += random.choice(string_pool)
    
    return random_code

# 회원가입시 이메일 인증
@api_view(['POST'])
@permission_classes([AllowAny])
def email_auth(request):
    # 이메일 중복검사
    if get_user_model().objects.filter(email=request.data.get('email')).exists():
        return Response({'status': 1})
    # 인증번호
    code = email_random_code()
    try:
        send_mail(request.data.get('email'), '사만코 이메일 인증 요청', 
        '다음 인증코드를 입력해주세요 ' + code)
    except:
        
        return Response({'status': 3})
    return Response({'status': 2, 'code': code})

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):

    serializer = UserSerializer(data=request.data)

	# validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # send_mail(user.email, '사만코 이메일 인증 요청', '인증번호입니다.')
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다. (write_only)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_temp_password(request):
    
    # user 테이블에서 해당 이메일 확인
    if not get_user_model().objects.filter(email=request.data.get('email')).exists():
        return Response({'message': '존재하지 않는 유저'}, status=status.HTTP_204_NO_CONTENT)

    # 소셜 가입 유저인지 확인
    user = get_user_model().objects.get(email=request.data.get('email'))
    try:
        social_user = SocialAccount.objects.get(user=user)
        if social_user.provider == 'google':
            return Response({'message': 'google'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        elif social_user.provider == 'kakao':
            return Response({'message': 'kakao'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    except:
        pass

    # 임시 비밀번호 전송
    code = email_random_code()
    send_mail(request.data.get('email'), '사만코 임시 비밀번호 발송', 
    '다음 비밀번호로 로그인 해주세요 ' + code)
    
    # 임시비밀번호로 다시 저장
    user.set_password(code)
    user.save()        
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def password_change(request):
    user = get_user_model().objects.get(email=request.user.email)
    # 이전 비밀번호가 맞는지 확인
    user.set_password(request.data.get('newPassword'))
    user.save()
    return Response(status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT'])
def profile(request):
    me = get_user_model().objects.get(pk=request.user.id)

    if request.method == 'GET':
        serializer = ProfileSerializer(me)
        return Response(serializer.data)

    elif request.method == 'PUT':

        if request.data.get('user_phone'):
            pass
        else:
            request.data['user_phone'] = " "

        serializer = ProfilePutSerializer(me, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request):
    user = get_user_model().objects.get(user_email=request.data.get('user_email'))
    if user:
        user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_kakao(request):
    print(request.data)
    access_token = request.data.get('access_token')
    code = request.data.get('code')

    # 내 정보 조회
    url = "https://kapi.kakao.com/v2/user/me"

    response = requests.get(url, headers={
        "Authorization": "Bearer " + access_token
    })

    email = response.json().get('kakao_account').get('email')
    print(email)
    # 회원가입 로그인 진행
    # SNS 가입 유저 확인
    try:
        user = get_user_model().objects.get(email=email)
        print(1)
        social_user = SocialAccount.objects.get(user=user)
        print(2)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Kakao로 가입된 유저

        return JsonResponse({'valid': True}, status=status.HTTP_200_OK)
    # 기존에 가입된 유저가 없으면 새로 가입
    except User.DoesNotExist:

        return JsonResponse({'valid': True}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def signup_google(request):
    access_token = request.data.get('access_token')
    code = request.data.get('code')

    # 회원가입 로그인 진행
    # SNS 가입 유저 확인
    try:
        user = get_user_model().objects.get(email=request.data.get('email'))
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'valid': True}, status=status.HTTP_200_OK)
    # 기존에 가입된 유저가 없으면 새로 가입
    except User.DoesNotExist:

        return JsonResponse({'valid': True}, status=status.HTTP_200_OK)

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client

