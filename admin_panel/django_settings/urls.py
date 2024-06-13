from django.urls import path, include
from admin_panel.telegram.admin import bot_admin

urlpatterns = [
    path('telegram/', include('admin_panel.telegram.urls')),
    path('', bot_admin.urls),

]
