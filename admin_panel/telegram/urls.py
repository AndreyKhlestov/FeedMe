from django.urls import path

from admin_panel.telegram import views

app_name = 'tg'

urlpatterns = [
    path('mailing', views.mailing, name='mailing'),
    path(
        'receiving_report/<int:user_id>/',
        views.create_receiving_report,
        name='report'
    ),

]
