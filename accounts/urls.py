from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('login/',login,name="login") ,
    path('',login,name="login") ,
    path('signup/',signup,name="signup") ,
    path('forgot_pass/',forgot_pass,name="forgot_pass") ,
    path('new_pass/<token>',new_pass,name="new_pass") ,
    path('logout/',logout,name="logout") ,
]