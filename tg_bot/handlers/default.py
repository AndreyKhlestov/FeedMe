import re

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.config import logger, site_url
from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser

from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards import reply as reply_kb

from tg_bot.db import db_commands as db


default_router = Router()


GET_FEED = "get_feed"
FEEDING = "to_feed"
TRANSFER = "transfer_feed"
NOT_ACCEPT_FEED = "not_accept_feed"
ACCEPY_FEED = "accept_feed"
URL = f'https://{site_url}' + '/telegram/{slug}/{call.from_user.id}/'
PERSONAL_ACCOUNT = "personal_account"
STATISTIC = "get_statistic"


def is_valid_phone_number(phone_number: str) -> bool:
    """Валидация ввода номера телефона вручную."""
    pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
    return bool(pattern.match(phone_number))


def ensure_plus_prefix(phone_number: str) -> str:
    """
    Проверяет, начинается ли номер телефона с + и добавляет его, если нет.
    """
    if not phone_number.startswith("+"):
        return f"+{phone_number}"
    return phone_number


async def check_in_base(message, phone_number):
    user = await db.get_user_by_number(phone_number)
    if user.phone_number:
        await message.answer(
            text=(
                "Ура, такой пользователь с номером есть в "
                "базе, ему отправлен запрос на приемку корма"
            )
        )
        tg_id = user.id
        if tg_id:
            await bot.send_message(
                chat_id=tg_id,
                text="Вам отправлен запрос на приемку корма",
                reply_markup=inline_kb.accept_or_not(),
            )
        else:
            await message.answer(
                text=f"Не удалось найти пользователя с id {tg_id}."
            )
    else:
        await message.answer(
            text="Пользователь с таким номером телефона не найден в базе."
        )


@default_router.callback_query(F.data == "back_main_menu")
async def back_main_menu(call: types.CallbackQuery, state: FSMContext):
    """Возращене в главное меню."""
    await call.message.delete()
    await main_menu(call.from_user, state)


async def main_menu(user: types.User, state: FSMContext):
    """Главное меню"""
    await state.clear()
    await bot.send_message(
        chat_id=user.id,
        text="Главное меню",
        reply_markup=inline_kb.main_menu(),
    )


@default_router.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    """Команда /start, отправка контакта."""
    logger.info(
        f"Пользователь {message.from_user.full_name} ввел(a) команду /start"
    )

    if await db.tg_user_exists(message.from_user.id):
        await main_menu(message.from_user, state)
    else:
        await state.set_state(StateUser.enter_phone)
        await message.answer(
            text="Отправьте свой номер телефона при помощи кнопки",
            reply_markup=reply_kb.send_contact(),
        )


@default_router.message(StateUser.enter_phone, F.contact)
async def check_phone(message: types.Message, state: FSMContext):
    """Проверка номера телефона при первом запуске бота."""
    phone_number = ensure_plus_prefix(message.contact.phone_number)
    user = await db.get_user_by_number(phone_number)
    if user and user.phone_number:
        await db.end_registration(
            user=message.from_user, phone_number=phone_number
        )
        await message.answer(
            text="Регистрация завершена",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await main_menu(message.from_user, state)
    else:
        await message.answer(
            text=(
                "Вы не зарегистрированы в программе, "
                "обратитесь к администратору"
            )
        )


@default_router.message(Command("help"))
async def command_help(message: types.Message):
    """Обработка команды /help."""
    await message.answer("Для запуска или перезапуска бота напишите /start")


@default_router.callback_query(F.data == GET_FEED)
async def get_feed(call: types.CallbackQuery):
    """Получение корма."""
    await call.message.delete()
    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(
            text="Форма для передачи корма",
            web_app=WebAppInfo(
                url=URL.format(
                    slug="receiving_report",
                    call=call,
                    reply_markup=markup.as_markup(),
                ),
            ),
        )
    )
    markup.row(inline_kb.BUTTON_BACK_MAIN_MENU)

    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=("Нажмите на кнопу 'Форма для передачи "
              "корма' для оформления передачи"),
        reply_markup=markup.as_markup(),
    )


@default_router.callback_query(F.data == FEEDING)
async def feeding(call: types.CallbackQuery):
    """Кормление."""
    await call.message.delete()
    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(
            text="Форма для списания корма",
            web_app=WebAppInfo(
                url=URL.format(
                    slug="feed_report",
                    call=call,
                )
            ),
        )
    )
    markup.row(inline_kb.BUTTON_BACK_MAIN_MENU)
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=("Нажмите на кнопку 'Форма для списания корма' "
              "для оформления списания"),
        reply_markup=markup.as_markup(),
    )


# @default_router.callback_query(F.data == TRANSFER)
# async def transfer_from_volunteer_to_volunteer(
#     call: types.CallbackQuery, state: FSMContext
# ):
#     """Передача корма от волонтера волонтеру."""
#     await call.message.delete()
#     await state.set_state(StateUser.send_phone)
#     await call.bot.send_message(
#         chat_id=call.from_user.id,
#         text=(
#             "Пожалуйста, выберите контакт из вашей "
#             "телефонной книги и отправьте его сюда. "
#             "Или введите номер вручную по типу +79ХХХХХХХХХ."
#         ),
#     )


# @default_router.message(StateUser.send_phone, F.contact)
# async def check_contact_in_base(message: types.Message):
#     """Проверка волонтера на наличие в базе, если слать контакт."""
#     phone_number = ensure_plus_prefix(message.contact.phone_number)
#     await check_in_base(message, phone_number)


# @default_router.message(StateUser.send_phone, F.text)
# async def check_text_phone_number_in_base(message: types.Message):
#     """Проверка волонтера на наличие в базе при ручном вводе."""
#     phone_number = message.text.strip()

#     if not is_valid_phone_number(phone_number):
#         await message.answer(
#             text=(
#                 "Пожалуйста, введите корректный "
#                 "номер телефона по типу +79ХХХХХХХХХ."
#             )
#         )
#         return
#     await check_in_base(message, phone_number)


# @default_router.callback_query(F.data == NOT_ACCEPT_FEED)
# async def delete_acc_notacc_buttons(call: types.CallbackQuery):
#     """Отколонение запроса на передачу корма."""
#     await call.bot.send_message(
#         chat_id=call.from_user.id,
#         text="Запрос отклонен",
#     )
#     await bot.edit_message_text(
#         text=call.message.text,
#         chat_id=call.from_user.id,
#         message_id=call.message.message_id,
#     )


# @default_router.callback_query(F.data == ACCEPY_FEED)
# async def accept_feed(call: types.CallbackQuery):
#     """Принятие запроса на передачу корма."""
#     await call.bot.send_message(
#         chat_id=call.from_user.id,
#         text="Здесь будет происходить передача корма",
#     )
#     await bot.edit_message_text(
#         text=call.message.text,
#         chat_id=call.from_user.id,
#         message_id=call.message.message_id,
#     )


@default_router.message(Command("report"))
async def command_otchet(message: types.Message):
    """Переход на страницу отчета."""
    markup = InlineKeyboardBuilder()
    url = f"https://{site_url}/telegram/receiving_report/{message.from_user.id}/"
    markup.add(InlineKeyboardButton(text="hello", web_app=WebAppInfo(url=url)))
    return message.answer("Привет", reply_markup=markup.as_markup())


@default_router.callback_query(F.data == PERSONAL_ACCOUNT)
async def personal_account(call: types.CallbackQuery):
    """Личный кабинет."""
    await call.message.delete()
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text="Здесь будет личный кабинет.",
        reply_markup=inline_kb.back_main_menu(),
    )

