from django.apps import AppConfig


class DjangoDBConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel.telegram'
    verbose_name = 'админ панель'

    # def ready(self):
    #     import admin_panel.telegram.signals
