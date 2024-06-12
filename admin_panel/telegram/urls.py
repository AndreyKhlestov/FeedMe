from django.urls import path

from admin_panel.telegram import views

app_name = 'tg'

urlpatterns = [
    path('mailing', views.mailing, name='mailing'),
    path('report/<int:user_id>/', views.report, name='report'),
]
