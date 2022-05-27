from django.urls import path
from . import views

urlpatterns = [
    path("timereport/year/", views.timereportlist_get),
    path("timereport/lastday/", views.timereport_lastday),
    path("timereport/", views.timereport),
    path('rank/', views.rank)
]

