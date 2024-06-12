from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command

from tg_bot.config import logger
from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser

from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards import reply as reply_kb

from tg_bot.db import db_commands as db


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


@default_router.message(StateUser.enter_phone, F.contact)
async def check_phone(message: types.Message, state: FSMContext):
    """Проверка номера телефона."""
    phone_number = message.contact.phone_number
    if await db.phone_number_exists(phone_number):
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
    await message.answer("Для запуска или перезапуска бота напишите /start")

