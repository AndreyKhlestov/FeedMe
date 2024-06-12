from django.conf import settings
from django.urls import path

from admin_panel.telegram import views
from django.conf.urls.static import static


app_name = 'tg'

urlpatterns = [
    path('mailing/', views.mailing, name='mailing'),
    path('report/<int:user_id>/', views.report, name='report'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
