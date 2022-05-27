from django.urls import path
from . import views

urlpatterns = [
    path('schedules/', views.schedule),
    path('schedules/<int:schedule_pk>/', views.schdeule_detail),
    path('monthly_schedule/<int:year>/<int:month>/', views.monthly_schedule),
]
