import asyncio

from aiogram import Bot, exceptions
from aiogram.types import FSInputFile

from tg_bot.config import logger
from tg_bot.db import db_commands as db


async def start_milling(bot: Bot):
    """Поиск запуск неотправленных (по времени) рассылок"""
    mailings = await db.get_all_malling()
    users = await db.users_mailing()
    for mailing in mailings:
        logger.info(f'Starting mailing №{mailing.pk}')
        file_id = None
        for user in users:
            args = [user.id]
            kwargs = {}
            if mailing.media_type in ['photo', 'video', 'document']:
                kwargs['caption'] = mailing.text
                if file_id:
                    args.append(file_id)
                else:
                    args.append(FSInputFile(mailing.file.path))
            else:
                args.append(mailing.text)
            file_id = await send_message_mailing(bot, mailing.media_type, args, kwargs)
            await asyncio.sleep(1/25)
        mailing.is_sent = True
        mailing.save()


async def send_message_mailing(bot, media, args, kwargs) -> None or int:
    """Универсальная функция для отправки сообщения с вложением"""
    send_methods = {
        'photo': bot.send_photo,
        'video': bot.send_video,
        'document': bot.send_document,
        'no_media': bot.send_message,
    }
    send_method = send_methods.get(media)
    try:
        message = await send_method(*args, **kwargs)
    except exceptions.TelegramForbiddenError as e:
        if e.message == 'Forbidden: bot was blocked by the user':
            logger.info(f'Пользователь {args[0]} заблокировал бота')
            await db.set_bot_block(user_id=args[0])
        else:
            logger.warning(e)
    except exceptions.TelegramRetryAfter as e:
        logger.warning(f'Flood limit is exceeded. Sleep {e.retry_after} seconds.')
        await asyncio.sleep(e.retry_after)
        return await send_message_mailing(bot, media, args, kwargs)
    except (exceptions.TelegramAPIError, exceptions.TelegramBadRequest):
        pass
    else:
        if media == 'photo':
            file_id = message.photo[-1].file_id
        elif media == 'video':
            file_id = message.video.file_id
        elif media == 'document':
            file_id = message.document.file_id
        else:
            return None

        return file_id
