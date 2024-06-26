from django.contrib import admin
from django.urls import reverse

from admin_panel.telegram.forms import (
    MailingForm, FeedAmountForm, ReportPhotoForm, TgUserForm
)
from admin_panel.telegram.models import (
    Category, Feed, TgUser, Mailing, TypeFeed, UnitMeasure, FeedAmount,
    TgUserCategory, TradingPoint, TransferReport, ReceivingReport, ReportPhoto,
    FinalDeliveryReport,
)


class BotAdminSite(admin.AdminSite):
    site_title = "Управление ботом"
    site_header = "Управление ботом"
    index_title = ""

    def get_app_list(self, request, app_label=None):
        # Построение словаря с информацией о приложениях
        app_dict = self._build_app_dict(request)
        # Сортировка приложений (возможно) по id - в порядке регистрации
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        new_models = [
            {
                "name": "Статистика",
                "admin_url": reverse('tg:statistics'),
                "view_only": True
            },
        ]
        for app in app_list:
            app['models'].extend(new_models)

        return app_list


bot_admin = BotAdminSite()


class FeedAmountInline(admin.TabularInline):
    model = FeedAmount
    extra = 0
    form = FeedAmountForm


@admin.register(TgUser, site=bot_admin)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number',
        'full_name',
        'email',
        'category',
        'bot_unblocked',
        'is_unblocked',
    )
    inlines = [FeedAmountInline]
    form = TgUserForm

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + (
                'id', 'username', 'bot_unblocked')
        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            # Если создается новый объект, убираем hidden_field из формы
            hidden_fields = ['id', 'username']
            for field in hidden_fields:
                form.base_fields.pop(field, None)
        return form

    def get_inline_instances(self, request, obj=None):
        """Использование inline формы только для уже созданной модели"""
        inline_instances = []
        if obj:
            for inline_class in self.inlines:
                inline = inline_class(self.model, self.admin_site)
                inline_instances.append(inline)
        return inline_instances


@admin.register(TgUserCategory, site=bot_admin)
class TgUserCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(TradingPoint, site=bot_admin)
class TradingPointAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'address',)


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


@admin.register(TypeFeed, site=bot_admin)
class TypeFeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category, site=bot_admin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(UnitMeasure, site=bot_admin)
class UnitMeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Feed, site=bot_admin)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_feed', 'category', 'unit_measure')


class ReportPhotoInline(admin.TabularInline):
    model = ReportPhoto
    extra = 0
    form = ReportPhotoForm


@admin.register(ReceivingReport, site=bot_admin)
class ReceivingReportAdmin(admin.ModelAdmin):
    list_display = ('created',)
    inlines = [ReportPhotoInline, FeedAmountInline]

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(TransferReport, site=bot_admin)
class TransferReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'created')
    inlines = [ReportPhotoInline, FeedAmountInline]

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(FinalDeliveryReport, site=bot_admin)
class FinalDeliveryReportAdmin(admin.ModelAdmin):
    inlines = [ReportPhotoInline, FeedAmountInline]

    def has_change_permission(self, request, obj=None):
        return False
