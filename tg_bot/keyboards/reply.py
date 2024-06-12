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
    keyboard.button(text='Отправить контакт', request_contact=True)
    return keyboard.adjust(1).as_markup(resize_keyboard=True)
