from django.contrib import admin

from admin_panel.telegram.forms import MailingForm
from admin_panel.telegram.models import (TgUser, Mailing,
                                         TgUserCategory, TradingPoint)


class BotAdminSite(admin.AdminSite):
    site_title = "Управление ботом"
    site_header = "Управление ботом"
    index_title = ""

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


bot_admin = BotAdminSite()


@admin.register(TgUser, site=bot_admin)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'full_name',
        'phone_number',
        'email',
        'category',
        'bot_unblocked',
        'is_unblocked',
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                'id', 'username', 'bot_unblocked')
        return self.readonly_fields


@admin.register(TgUserCategory, site=bot_admin)
class TgUserCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(TradingPoint, site=bot_admin)
class TradingPointAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'address',
    )


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
