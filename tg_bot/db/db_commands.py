from asgiref.sync import sync_to_async
from aiogram.types.user import User
from django.utils import timezone
from django.contrib.auth.models import User as Model_User

from admin_panel.telegram.models import TgUser, Mailing


@sync_to_async()
def create_super_user(username, password):
    """Автоматическое создание логина и пароля для суперпользователя"""
    if not Model_User.objects.filter(username=username).exists():
        Model_User.objects.create_superuser(username, password=password)


@sync_to_async()
def get_all_malling():
    """
    Получение неотправленных рассылок,
    у которых время отправления настало или истекло
    """
    now = timezone.now()
    return Mailing.objects.filter(is_sent=False, date_malling__lte=now)


@sync_to_async
def get_and_update_user(user: User):
    """Добавление и/или получение пользователя"""
    tg_user, created = TgUser.objects.get_or_create(id=user.id, url=user.url)
    if (tg_user.username != user.username or
            tg_user.full_name != user.full_name or
            tg_user.bot_unblocked is False):
        # эти данные могут со временем меняться
        tg_user.username = user.username or '-'
        tg_user.full_name = user.full_name
        tg_user.bot_unblocked = True
        tg_user.save()
    return tg_user


@sync_to_async
def set_bot_block(user_id: int):
    """Запись отметки о блокировке пользователем бота"""
    tg_user = TgUser.objects.get(id=user_id)
    tg_user.bot_unblocked = False
    tg_user.save()


@sync_to_async
def users_mailing():
    """Выдача всех пользователей для рассылки"""
    users = TgUser.objects.filter(bot_unblocked=True)
    return users


@sync_to_async
def model_save(model):
    """Сохранение (изменений) модели"""
    model.save()
