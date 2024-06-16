from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver

from admin_panel.django_settings.s3_storage import MediaStorage
from admin_panel.telegram.utils import get_unique_file_path


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class CreateNameModel(models.Model):
    """Абстрактная модель. Добавляет наименование."""
    name = models.CharField(
        verbose_name='Наименование',
        unique=True,
        max_length=32
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)


class TgUserCategory(models.Model):
    """Модель категории для пользователя"""
    title = models.CharField(
        verbose_name='Название категории',
        max_length=32,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категорию пользователя'
        verbose_name_plural = 'Категории пользователя'

    def __str__(self) -> str:
        return self.title


class TgUser(CreatedModel):
    """Модель пользователя"""
    id = models.BigIntegerField(
        verbose_name='ID пользователя в Telegram',
        null=True,
        blank=True,
        default=None,
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=32,
        null=True,
        blank=True,
        default=None,
    )
    full_name = models.CharField(
        verbose_name='ФИО',
        max_length=255,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=12,
        unique=True,
        primary_key=True,
        help_text='Номер телефона вводить в формате +7*******',
    )
    passport_photo = models.ImageField(
        verbose_name='Фото паспорта',
        upload_to='user_data/',
        null=True,
        blank=True,
        default=None
    )
    email = models.EmailField(verbose_name='Почта', unique=True)
    category = models.ForeignKey(
        TgUserCategory,
        verbose_name='Категория пользователя',
        on_delete=models.PROTECT,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        max_length=64,
        null=True,
        blank=True,
        default=None
    )
    bot_unblocked = models.BooleanField(
        verbose_name='Бот разблокирован пользователем', default=True)
    is_unblocked = models.BooleanField(
        verbose_name='Пользователь разблокирован', default=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'#{self.id} {self.full_name}'


class TradingPoint(models.Model):
    address = models.CharField(
        verbose_name='Адрес точки',
        max_length=200
    )
    title = models.CharField(
        verbose_name='Название точки',
        max_length=80
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=200,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Торговую точку'
        verbose_name_plural = 'Торговые точки'

    def __str__(self) -> str:
        return self.title


class Mailing(models.Model):
    CHOICES = (
        ("no_media", 'Без медиа'),
        ("photo", 'Фото'),
        ("video", 'Видео'),
        ("document", 'Документ'),
    )
    media_type = models.CharField(
        max_length=50,
        help_text='Тип медиа',
        verbose_name='Тип медиа',
        choices=CHOICES
    )
    text = models.TextField(
        max_length=4096,
        help_text='Текст рассылки',
        verbose_name='Текст',
        blank=True,
        null=True,
    )
    file = models.FileField(
        help_text='Файл для рассылки',
        verbose_name='Файл',
        upload_to="files_mailing",
        blank=True,
        null=True,
    )
    date_malling = models.DateTimeField(
        help_text='Дата рассылки',
        verbose_name='Дата',
    )
    is_sent = models.BooleanField(
        help_text='Статус отправки',
        verbose_name='Статус отправки',
        default=False
    )

    class Meta:
        verbose_name = 'Рассылки'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return str(self.pk)


class TypeFeed(CreateNameModel):
    """Тип корма."""
    class Meta:
        verbose_name = 'Тип корма'
        verbose_name_plural = 'Типы кормов'


class Category(CreateNameModel):
    """Категория."""
    class Meta:
        verbose_name = 'Категория корма'
        verbose_name_plural = 'Категории корма'


class UnitMeasure(CreateNameModel):
    """Единица измерения."""
    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Feed(models.Model):
    """Корм."""
    type_feed = models.ForeignKey(
        TypeFeed,
        verbose_name='Тип',
        related_name='type_feeds',
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='categorys',
        on_delete=models.PROTECT

    )
    unit_measure = models.ForeignKey(
        UnitMeasure,
        verbose_name='Единица измерения',
        related_name='unit_measures',
        on_delete=models.PROTECT
    )
    image_url = models.URLField(
        verbose_name='Ссылка на иконку',
        default='https://icon666.com/r/_thumb/rcl/rcls4ll64y6q_64.png'
    )
    name = models.CharField(
        verbose_name='Название на сайте',
        max_length=32,
    )

    class Meta:
        verbose_name = 'Корм'
        verbose_name_plural = 'Корма'
        constraints = [
            models.UniqueConstraint(
                fields=['type_feed', 'category', 'unit_measure'],
                name='unique_feed'
            )
        ]

    def __str__(self) -> str:
        return (
            f'{self.name} ({self.unit_measure.name})'
        )


class ReportBase(CreatedModel):
    """Абстрактная модель отчета."""
    user = models.ForeignKey(
        TgUser,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='%(class)s_user'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        max_length=256,
        null=True,
        blank=True,
        default=None
    )

    class Meta:
        abstract = True


class ReceivingReport(ReportBase):
    """Модель отчета по получению корма из точки выдачи."""
    trading_point = models.ForeignKey(
        TradingPoint,
        verbose_name='Точка выдачи',
        on_delete=models.PROTECT,
        related_name='receiving_reports'
    )

    def __str__(self):
        return (f'Получение корма №{self.pk} с точки '
                f'{self.trading_point} пользователем {self.user}')

    class Meta:
        verbose_name = 'Отчет по получению корма'
        verbose_name_plural = 'Отчеты по получению корма'


class TransferReport(ReportBase):
    """Модель отчета по передаче корма."""
    recipient = models.ForeignKey(
        TgUser,
        verbose_name='Получатель',
        on_delete=models.PROTECT,
        related_name='transfer_reports'
    )
    approval = models.BooleanField(
        verbose_name='Подтверждение передачи',
        default=False
    )

    def __str__(self):
        return (f'Передача корма №{self.pk} от '
                f'{self.user} к {self.recipient}')

    class Meta:
        verbose_name = 'Отчет по передаче корма'
        verbose_name_plural = 'Отчеты по передаче корма'


class FinalDeliveryReport(ReportBase):
    """Модель отчета по конечной выдаче корма."""
    address = models.CharField(
        verbose_name='Адрес конечной точки выдачи корма',
        max_length=200,
    )

    def __str__(self):
        return (f'Конечная выдача корма №{self.pk} пользователем {self.user}'
                f'по адресу: {self.address}')

    class Meta:
        verbose_name = 'Отчет по конечной выдаче корма'
        verbose_name_plural = 'Отчеты по конечной выдаче корма'


class ReportPhoto(models.Model):
    """Модель для фотографий отчетов."""
    photo = models.ImageField(
        upload_to=get_unique_file_path,
        storage=MediaStorage(),
    )
    receiving_report = models.ForeignKey(
        ReceivingReport,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
    )
    transfer_report = models.ForeignKey(
        TransferReport,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
    )
    delivery_report = models.ForeignKey(
        FinalDeliveryReport,
        on_delete=models.CASCADE,
        related_name='photos',
        null=True,
    )


class FeedAmount(models.Model):
    """Корм и его количество."""
    feed = models.ForeignKey(
        Feed,
        verbose_name='Корм',
        related_name='feeds',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name='Кол-во',
        default=0,
        validators=(MinValueValidator(0),)
    )
    receiving_report = models.ForeignKey(
        ReceivingReport,
        on_delete=models.CASCADE,
        related_name='feeds_amount',
        null=True,
    )
    transfer_report = models.ForeignKey(
        TransferReport,
        on_delete=models.CASCADE,
        related_name='feeds_amount',
        null=True,
    )
    delivery_report = models.ForeignKey(
        FinalDeliveryReport,
        on_delete=models.CASCADE,
        related_name='feeds_amount',
        null=True,
    )
    tg_user = models.ForeignKey(
        TgUser,
        on_delete=models.CASCADE,
        related_name='feeds_amount',
        null=True,
    )

    class Meta:
        verbose_name = 'Данные о корме'
        verbose_name_plural = 'Данные о кормах'

    def __str__(self) -> str:
        return f'{self.feed} - {self.amount}'


@receiver(pre_delete, sender=Mailing)
def delete_related_file(sender, instance, **kwargs):
    # Проверка на наличие файла и его удаление
    if instance.file:
        storage, path = instance.file.storage, instance.file.path
        storage.delete(path)


@receiver(pre_save, sender=TgUser)
def delete_related_file_edit(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_instance = TgUser.objects.filter(pk=instance.pk).first()

    if (old_instance and old_instance.passport_photo and
            old_instance.passport_photo != instance.passport_photo):
        old_instance.passport_photo.delete(save=False)
        # save определяет - будет ли модель сохранена после удаления файла.


@receiver(pre_save, sender=TransferReport)
def update_feed_amount_on_transfer_report(sender, instance, **kwargs):
    if instance.pk:
        old_instance = TransferReport.objects.get(pk=instance.pk)
        if old_instance.approval is False and instance.approval is True:
            for feed_amount in instance.feeds_amount.all():
                sender_feed_amount = FeedAmount.objects.filter(
                    tg_user=instance.user,
                    feed=feed_amount.feed
                ).first()

                # Уменьшаем количество корма у пользователя-отправителя
                sender_feed_amount.amount -= feed_amount.amount
                sender_feed_amount.save()

                recipient_feed_amount = FeedAmount.objects.filter(
                    tg_user=instance.recipient,
                    feed=feed_amount.feed,
                ).first()
                if recipient_feed_amount:
                    recipient_feed_amount.amount += feed_amount.amount
                    recipient_feed_amount.save()
                else:
                    FeedAmount.objects.create(
                        tg_user=instance.recipient,
                        feed=feed_amount.feed,
                        amount=feed_amount.amount
                    )


@receiver(post_save, sender=FeedAmount)
def update_feed_amount_on_report(sender, instance, created, **kwargs):
    if instance.amount == 0:
        instance.delete()

    if created:
        if instance.receiving_report:
            tg_user = instance.receiving_report.user
            feed_amount_user = tg_user.feeds_amount.filter(
                feed=instance.feed
            ).first()
            if feed_amount_user:
                feed_amount_user.amount += instance.amount
                feed_amount_user.save()
            else:
                FeedAmount.objects.create(
                    tg_user=tg_user,
                    feed=instance.feed,
                    amount=instance.amount
                )

        elif instance.delivery_report:
            tg_user = instance.delivery_report.user
            feed_amount_user = tg_user.feeds_amount.filter(
                feed=instance.feed
            ).first()
            if feed_amount_user:
                feed_amount_user.amount -= instance.amount
                feed_amount_user.save()

        elif instance.transfer_report and instance.transfer_report.approval:
            tg_user = instance.transfer_report.user
            sender_feed_amount = tg_user.feeds_amount.filter(
                feed=instance.feed
            ).first()

            # Уменьшаем количество корма у пользователя-отправителя
            sender_feed_amount.amount -= instance.amount
            sender_feed_amount.save()

            recipient = instance.transfer_report.recipient
            recipient_feed_amount = recipient.feeds_amount.filter(
                feed=instance.feed
            ).first()
            if recipient_feed_amount:
                recipient_feed_amount.amount += instance.amount
                recipient_feed_amount.save()
            else:
                FeedAmount.objects.create(
                    tg_user=recipient,
                    feed=instance.feed,
                    amount=instance.amount
                )
