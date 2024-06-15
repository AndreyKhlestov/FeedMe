from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def reply_keyboards(data: list[str], columns: int = 2) -> ReplyKeyboardMarkup:
    """
    Универсальная reply клавиатура
    Функция получает список, в котором находится текст для каждой кнопки, и
    количество столбцов (сколько будет кнопок в одной строке).
    Возвращает саму клавиатуру
    """
    builder = ReplyKeyboardBuilder()
    for button in data:
        builder.add(KeyboardButton(text=button))
    builder.adjust(columns)
    return builder.as_markup(resize_keyboard=True)


def send_contact():
    """Клавиатура для отправки номера телефона"""
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Отправить контакт", request_contact=True)
    return keyboard.adjust(1).as_markup(resize_keyboard=True)


def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: List[int] = [2],
):
    """
    Parameters request_contact and request_location must be as indexes
    of btns args for buttons you need.
    Example:
    get_keyboard(
            'About us',
            'Registration',
            'Pause communication',
            request_contact=4,
            sizes=[2, 2, 1]
        )
    """
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder
    )
