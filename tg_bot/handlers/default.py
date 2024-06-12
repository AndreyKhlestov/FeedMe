from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, \
    WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.config import logger
from tg_bot.db import db_commands as db
from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards import reply as reply_kb
from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser

default_router = Router()


@default_router.callback_query(F.data == "back_main_menu")
async def back_main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await main_menu(call.from_user, state)


async def main_menu(user: types.User, state: FSMContext):
    """Главное меню"""
    await state.clear()  # сброса состояния (state) для пользователя
    await bot.send_message(
        chat_id=user.id,
        text="Главное меню.",
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


@default_router.message(Command("help"))
async def command_help(message: types.Message):
    await message.answer("Для запуска или перезапуска бота напишите /start")


@default_router.message(Command('otchet'))
async def command_otchet(message: types.Message):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text='hello', web_app=WebAppInfo(
        url=f'http://127.0.0.1:8000/telegram/report/{message.from_user.id}/')))
    return message.answer('Привет', reply_markup=markup.as_markup())

# изменение состояния
# await state.set_state(StateUser.tariff_info)

# сохранение данных в состояние (в функции прописываем  state: FSMContext)
# await state.update_data(booking_date=date.strftime(str_format_date))

# получение данных в состояния (в функции прописываем  state: FSMContext)
# state_data = await state.get_data()
# date_string = state_data.get('booking_date')
