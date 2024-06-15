import re

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.config import logger
from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser

from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards import reply as reply_kb

from tg_bot.db import db_commands as db


default_router = Router()


GET_FEED = "Забрать корм"
FEEDING = "Кормление"
TRANSFER = "Передать корм волонтеру"
NOT_ACCEPT_FEED = "not_accept_feed"
ACCEPY_FEED = "accept_feed"
URL = 'https://unique-leopard-enhanced.ngrok-free.app/telegram/{slug}/{message.from_user.id}/'

def is_valid_phone_number(phone_number: str) -> bool:
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
    await call.message.delete()
    await main_menu(call.from_user, state)


async def main_menu(user: types.User, state: FSMContext):
    """Главное меню"""
    await state.clear()
    await bot.send_message(
        chat_id=user.id,
        text=f"{user.full_name}, добро пожаловать в главное меню!",
        reply_markup=reply_kb.MAIN_MENU_KBRD,
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


@default_router.message(F.text == GET_FEED)
async def get_feed(message: types.Message):
    """Получение корма."""
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text='hello', web_app=WebAppInfo(
        url=URL.format(
            slug='receiving_report',
            message=message))))  # url=f'http://127.0.0.1:8000/telegram/receiving_report/{message.from_user.id}/'
    return message.answer('Привет', reply_markup=markup.as_markup())


@default_router.message(F.text == FEEDING)
async def feeding(message: types.Message):
    """Кормление."""
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text='hello', web_app=WebAppInfo(
        url=URL.format(
            slug='feed_report',
            message=message,))))  # url=f'http://127.0.0.1:8000/telegram/receiving_report/{message.from_user.id}/'
    return message.answer('Привет', reply_markup=markup.as_markup())


@default_router.message(F.text == TRANSFER)
async def transfer_from_volunteer_to_volunteer(
    message: types.Message, state: FSMContext
):
    """Передача корма от волонтера волонтеру."""
    await state.set_state(StateUser.send_phone)
    await message.answer(
        text=(
            "Пожалуйста, выберите контакт из вашей "
            "телефонной книги и отправьте его сюда. "
            "Или введите номер вручную по типу +79ХХХХХХХХХ."
        )
    )


@default_router.message(StateUser.send_phone, F.contact)
async def check_contact_in_base(message: types.Message):
    """Проверка волонтера на наличие в базе, если слать контакт."""
    phone_number = ensure_plus_prefix(message.contact.phone_number)
    await check_in_base(message, phone_number)


@default_router.message(StateUser.send_phone, F.text)
async def check_text_phone_number_in_base(message: types.Message):
    """Проверка волонтера на наличие в базе при ручном вводе."""
    phone_number = message.text.strip()

    if not is_valid_phone_number(phone_number):
        await message.answer(
            text=(
                "Пожалуйста, введите корректный "
                "номер телефона по типу +79ХХХХХХХХХ."
            )
        )
        return
    await check_in_base(message, phone_number)


@default_router.callback_query(F.data == NOT_ACCEPT_FEED)
async def delete_acc_notacc_buttons(callback_query: types.CallbackQuery):
    """Отколонение запроса на передачу корма."""
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Запрос отклонен",
    )
    await bot.edit_message_text(
        text=callback_query.message.text,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )


@default_router.callback_query(F.data == ACCEPY_FEED)
async def accept_feed(callback_query: types.CallbackQuery):
    """Принятие запроса на передачу корма."""
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Здесь будет происходить передача корма",
    )
    await bot.edit_message_text(
        text=callback_query.message.text,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )
