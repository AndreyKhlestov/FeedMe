from django.contrib import admin
from django.urls import reverse

from admin_panel.telegram.forms import MailingForm
from admin_panel.telegram.models import TgUser, Button, Mailing


# from django.forms import Textarea



class BotAdminSite(admin.AdminSite):
    site_title = "Управление ботом"
    site_header = "Управление ботом"
    index_title = ""

    def get_app_list(self, request, app_label=None):
        # Построение словаря с информацией о приложениях
        app_dict = self._build_app_dict(request)
        # Сортировка приложений (возможно) по id - в порядке регистрации
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # new_models = [
        #     {
        #         "name": "Статистика",
        #         "admin_url": reverse('tg:statistics'),
        #         "view_only": True
        #     },
        # ]
        # for app in app_list:
        #     app['models'].extend(new_models)

        return app_list


bot_admin = BotAdminSite()


@admin.register(TgUser, site=bot_admin)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'bot_unblocked', 'is_unblocked')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Если редактируется существующий объект
            return self.readonly_fields + (
                'id', 'full_name', 'url', 'username', 'bot_unblocked')
        return self.readonly_fields

    # def has_add_permission(self, request):
    #     """Запрещаем добавление новых объектов"""
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     """Запрещаем редактирование объектов"""
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     """Запрещаем удаление объектов"""
    #     return False


# class ButtonInline(admin.StackedInline):
#     model = Button
#     extra = 0


# @admin.register(Mailing)
# class MailingAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
#     }
#     list_display = ('text', 'mail_date', 'is_send')
#     readonly_fields = ('is_send',)
#     inlines = [ButtonInline]


@admin.register(Mailing, site=bot_admin)
class MailingAdmin(admin.ModelAdmin):
    add_form_template = 'form_mailing.html'
    list_display = (
        'pk',
        'media_type',
        'text',
        'date_malling',
        'is_sent',
    )

    list_display_links = ('pk', 'media_type',)
    empty_value_display = '-пусто-'
    readonly_fields = ('is_sent',)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['form'] = MailingForm()
        return super().add_view(request, form_url, extra_context)

    class Meta:
        verbose_name_plural = 'Рассылка'
