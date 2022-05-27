from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', views.signup),
    path('email_auth/', views.email_auth),
    path('temp_password/', views.send_temp_password),
    path('password/', views.password_change),
    path('profile/', views.profile),
    path('delete-user/', views.delete_user),
    path('login/', obtain_jwt_token),
    path('kakaologin/', views.signup_kakao),
    path('kakao/login/finish/', views.KakaoLogin.as_view()),
    path('googlelogin/', views.signup_google),
    path('google/login/finish/', views.GoogleLogin.as_view()),
    path('api-token-auth/', obtain_jwt_token),
]
