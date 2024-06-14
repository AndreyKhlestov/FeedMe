from django.contrib import admin

from admin_panel.telegram.forms import MailingForm
from admin_panel.telegram.models import (
    Category, Feed, TgUser, Mailing, TypeFeed, UnitMeasure, FeedAmount,
    TgUserCategory, TradingPoint, TransferReport, ReceivingReport,
    FinalDeliveryReport, TransferReportPhoto, ReceivingReportPhoto,
    FinalDeliveryReportPhoto, Report, ReportImage
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
        return app_list


bot_admin = BotAdminSite()


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


@admin.register(FeedAmount, site=bot_admin)
class FeedAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'feed', 'amount',)


@admin.register(Report, site=bot_admin)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'trading_point',
        'wet_cats',
        'dry_cats',
        'wet_dogs',
        'dry_dogs',
        'date',
    )


@admin.register(ReportImage, site=bot_admin)
class ReportImageAdmin(admin.ModelAdmin):
    list_display = (
        'report',
        'image'
    )


class TransferReportPhotoInline(admin.TabularInline):
    model = TransferReportPhoto
    extra = 1


@admin.register(TransferReport, site=bot_admin)
class TransferReportAdmin(admin.ModelAdmin):
    inlines = [TransferReportPhotoInline]


class ReceivingReportPhotoInline(admin.TabularInline):
    model = ReceivingReportPhoto
    extra = 0


@admin.register(ReceivingReport, site=bot_admin)
class ReceivingReportAdmin(admin.ModelAdmin):
    inlines = [ReceivingReportPhotoInline]


class FinalDeliveryReportPhotoInline(admin.TabularInline):
    model = FinalDeliveryReportPhoto
    extra = 0


@admin.register(FinalDeliveryReport, site=bot_admin)
class FinalDeliveryReportAdmin(admin.ModelAdmin):
    inlines = [FinalDeliveryReportPhotoInline]

