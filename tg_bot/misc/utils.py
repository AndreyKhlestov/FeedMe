# import asyncio
# import logging
# from aiogram.types import FSInputFile, InlineKeyboardMarkup
# from aiogram import exceptions as tg_exceptions
# from asgiref.sync import sync_to_async

# from tg_bot.db.db_commands import mailing_send, users_mailing, buttons_mailing
# from tg_bot.loader import bot
# from admin_panel.telegram.models import Mailing, TgUser
# from tg_bot.keyboards.default_inline_keyboards import buttons_links


# # функцию отправки сообщения вынес отдельно, чтобы можно было ею же
# # воспользоваться в случаях повторной отправки сообщений при ошибке
# async def send_mailing_for_user(mail: Mailing, user: TgUser, keyboard: InlineKeyboardMarkup) -> None:
#     """Универсальная функция для отправки сообщения из рассылки (как текста, так и картинки с текстом)"""
#     try:
#         if mail.image:
#             bot_message = await bot.send_photo(chat_id=user.id,
#                                                photo=FSInputFile(mail.image.path),
#                                                caption=mail.text,
#                                                reply_markup=keyboard)
#         else:
#             bot_message = await bot.send_message(chat_id=user.id, text=mail.text, reply_markup=keyboard)
#
#         await bot.pin_chat_message(chat_id=user.id, message_id=bot_message.message_id)
#     except tg_exceptions.TelegramRetryAfter as e:
#         logging.warning(f"Заморозка отправки сообщений ботом на {e.retry_after} сек.")
#         await asyncio.sleep(e.retry_after)
#         await send_mailing_for_user(mail, user, keyboard)
#     except Exception as e:
#         text = (f'Произошла ошибка \n\n'
#                 f'{e} При отправке сообщения пользователю: name: {user.full_name}, tg_id: {user.id}')
#         logging.warning(text)
#
#
# async def checking_mailing():
#     """Рассылка сообщений по всем пользователям"""
#     mail = await mailing_send()
#     if mail:
#         buttons = await buttons_mailing(mail)
#         keyboard_mailing = buttons_links(buttons)
#
#         users = await users_mailing()
#
#         async for user in users:
#             await send_mailing_for_user(mail, user, keyboard_mailing)
#
#         mail.is_send = True
#         await sync_to_async(mail.save)()
