from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command

from tg_bot.config import logger
from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser
from tg_bot.keyboards import inline as inline_kb
from tg_bot.keyboards import reply as reply_kb
from tg_bot.db import db_commands as db


base_reg_router = Router()


def ensure_plus_prefix(phone_number: str) -> str:
    """
    Проверяет, начинается ли номер телефона с + и добавляет его, если нет.
    """
    if not phone_number.startswith("+"):
        return f"+{phone_number}"
    return phone_number


@base_reg_router.callback_query(F.data == "back_main_menu")
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


@base_reg_router.message(Command("start"))
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


@base_reg_router.message(StateUser.enter_phone, F.contact)
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


@base_reg_router.message(Command("help"))
async def command_help(message: types.Message):
    """Обработка команды /help."""
    await message.answer("Для запуска или перезапуска бота напишите /start")
