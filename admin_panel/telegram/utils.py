import uuid
import os

# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from .models import TgUserCategory, TypeFeed, Category, UnitMeasure


def get_unique_file_path(instance, filename):
    """Создание уникального имени для файла"""
    extension = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join(instance._meta.model_name, unique_filename)


# @receiver(post_migrate)
# def create_default_entries(sender, **kwargs):
#     # Проверка и создание категорий пользователей
#     categories = ['Category1', 'Category2', 'Category3']
#     for category in categories:
#         TgUserCategory.objects.get_or_create(title=category)

#     # Проверка и создание типов кормов
#     type_feeds = ['Type1', 'Type2', 'Type3']
#     for type_feed in type_feeds:
#         TypeFeed.objects.get_or_create(name=type_feed)

#     # Проверка и создание категорий кормов
#     categories = ['FeedCategory1', 'FeedCategory2', 'FeedCategory3']
#     for category in categories:
#         Category.objects.get_or_create(name=category)

#     # Проверка и создание единиц измерения
#     units = ['kg', 'g', 'liter']
#     for unit in units:
#         UnitMeasure.objects.get_or_create(name=unit)
