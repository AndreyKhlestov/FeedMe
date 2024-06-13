from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

BUTTON_BACK_MAIN_MENU = InlineKeyboardButton(
    text="Меню 📋", callback_data="back_main_menu"
)
BUTTONS_BACK_STEP = InlineKeyboardButton(
    text="Назад ↩️", callback_data="back_step"
)
ACCEPT = InlineKeyboardButton(text="Принять корм", callback_data="accept_feed")
NOT_ACCEPT = InlineKeyboardButton(text="Отклонить", callback_data="reject")


def inline_keyboards(data: list or dict) -> InlineKeyboardBuilder:
    """
    Универсальная inline клавиатура.
    Получает список или словарь и возвращает inline клавиатуру из его значений.
    Если получен словарь, то текстом кнопки будет значение ключа,
    а возвращаемый результат - ключ словаря
    """
    keyboards = InlineKeyboardBuilder()
    for i_key in data:
        keyboards.add(
            InlineKeyboardButton(
                text=data[i_key] if isinstance(data, dict) else i_key,
                callback_data=str(i_key),
            )
        )
    keyboards.adjust(1)
    return keyboards


def main_menu():
    """Главное меню"""
    buttons = {"lk": "Личный кабинет"}
    keyboard = inline_keyboards(buttons)
    return keyboard.as_markup()


def back_main_menu():
    """Вернуться в главное меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(BUTTON_BACK_MAIN_MENU)
    return keyboard.as_markup()


def back_step():
    """Вернуться на шаг назад и вернуться в главное меню"""
    keyboard = builder_back_step_and_main_menu()
    return keyboard.as_markup()


def builder_back_step_and_main_menu():
    """Builder для кнопок Назад и Меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(BUTTONS_BACK_STEP)
    keyboard.add(BUTTON_BACK_MAIN_MENU)
    return keyboard.adjust(1)


def send_contact_instruction():
    """Инлайн-клавиатура для инструкций по отправке контакта"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Отправить контакт", callback_data="send_contact"
        )
    )
    return keyboard.as_markup()


def accept_or_not():
    """Кнопки Принять или не Принять корм."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Принять корм", callback_data="accept_feed"
        )

    )
    keyboard.add(
        InlineKeyboardButton(
            text="Не принять корм", callback_data="not_accept_feed"
        )

    )
    return keyboard.as_markup()
