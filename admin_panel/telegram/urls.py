from django.urls import path

from admin_panel.telegram import views

app_name = 'tg'

urlpatterns = [
    path('mailing', views.mailing, name='mailing'),
    path('statistics', views.statistics, name='statistics'),
    path('receiving_report/<int:user_id>/',
         views.create_receiving_report,
         name='report'),
    path('feed_report/<int:user_id>/',
         views.create_feed_report,
         name='feed_report'),
    path('check_phone_number/<int:user_id>/',
         views.check_phone_number,
         name='check_phone_number'),
    path('transfer_report/<int:user_id>/<int:recipient_id>/',
         views.create_transfer_report,
         name='transfer_report'),
    path('success/', views.success, name='success'),
    path('transfer_success/<int:recipient_id>', views.transfer_success, name='transfer_success'),
    path('transfer_bad_success/', views.bad_success, name='bad_success'),
]
