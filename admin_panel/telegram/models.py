from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, pre_save
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
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

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
        max_length=200
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
        constraints = [
            models.UniqueConstraint(
                fields=['type_feed', 'category', 'unit_measure'],
                name='unique_feed'
            )
        ]

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
    amount = models.IntegerField(
        verbose_name='Кол-во',
        default=0,
        validators=(MinValueValidator(0),)
    )


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
            old_instance.passport_photo != instance.passport_photo
    ):
        old_instance.passport_photo.delete(save=False)
        # save определяет - будет ли модель сохранена после удаления файла.


class Report(models.Model):
    point = models.ForeignKey('TradingPoint', on_delete=models.PROTECT, max_length=100, verbose_name='Торговые точки')
    wet_cats = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0)])
    dry_cats = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0)])
    wet_dogs = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0)])
    dry_dogs = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0)])
    photo = models.FileField(upload_to='photos/', blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)


