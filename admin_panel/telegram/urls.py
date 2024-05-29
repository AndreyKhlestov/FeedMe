from django.urls import path

from . import views

app_name = 'tg'

urlpatterns = [
    path('mailing', views.mailing, name='mailing'),
]
