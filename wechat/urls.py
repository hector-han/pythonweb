from django.urls import path
from . import views

urlpatterns = [
    path('main', views.wechat_main, name='wechat_main'),
]

