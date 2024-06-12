from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings
from admin_panel.telegram.admin import bot_admin

urlpatterns = [
    path('telegram/', include('admin_panel.telegram.urls')),
    path('', bot_admin.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
