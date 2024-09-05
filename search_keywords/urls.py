from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('visub/',sub,name="login") ,
    path('check_status/<task_id>/', check_status, name='check_status'),
    path('check_download_status/<task_id>/', check_download_status, name='check_download_status'),
]