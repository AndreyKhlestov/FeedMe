from django.core.validators import MinValueValidator
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


class Point(models.Model):
    name = models.CharField(verbose_name='Название точки', max_length=150)
    address = models.CharField(verbose_name='Адрес точки', max_length=255)
    phone_number = models.CharField(verbose_name='Номер телефона',
                                    max_length=12)

    class Meta:
        verbose_name = 'Точку'
        verbose_name_plural = 'Точки'


class Report(models.Model):
    name = models.CharField(max_length=100)
    wet_food = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0)])
    dry_food = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0)])
    photo = models.ImageField(upload_to='photos/', blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    received = models.BooleanField(default=True)
    point = models.ForeignKey(Point, on_delete=models.SET_NULL, null=True)
