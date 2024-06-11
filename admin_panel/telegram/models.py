from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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
    name = models.CharField(verbose_name='Наименование', max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)


class TgUser(CreatedModel):
    id = models.BigIntegerField(
        verbose_name='ID пользователя в Telegram', primary_key=True)
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=255,
        null=True,
        default=None
    )
    full_name = models.CharField(
        verbose_name='Полное имя пользователя',
        max_length=255,
        null=True,
        default=None
    )
    url = models.CharField(
        verbose_name='Ссылка на пользователя', max_length=255, unique=True)
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=12,
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


@receiver(pre_delete, sender=Mailing)
def delete_related_file(sender, instance, **kwargs):
    # Проверка на наличие файла и его удаление
    if instance.file:
        storage, path = instance.file.storage, instance.file.path
        storage.delete(path)


class Button(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        verbose_name='Рассылка',
        related_name='buttons',
        on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name='Текст кнопки', max_length=64)
    link = models.CharField(verbose_name='Ссылка', max_length=1024)

    class Meta:
        verbose_name = 'Кнопку для рассылки'
        verbose_name_plural = 'Кнопки для рассылки'


class TypeFeed(CreateNameModel):
    """Тип корма."""
    class Meta:
        verbose_name = 'Тип корма'
        verbose_name_plural = 'Типы кормов'


class Category(CreateNameModel):
    """Категория."""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


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

    class Meta:
        verbose_name = 'Корм'
        verbose_name_plural = 'Корма'

    def __str__(self) -> str:
        return (
            f'#{self.type_feed.name} '
            f'{self.category.name} '
            f'{self.unit_measure.name}'
        )


class FeedAmount(models.Model):
    """Корм и его количество."""
    feed = models.ForeignKey(
        Feed,
        verbose_name='Корм',
        related_name='feeds',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(verbose_name='Кол-во')
