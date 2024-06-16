from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


from tg_bot.config import site_url


URL = f"https://{site_url}" + "/telegram/{slug}/{call.from_user.id}/"

BUTTON_BACK_MAIN_MENU = InlineKeyboardButton(
    text="Меню 📋", callback_data="back_main_menu"
)
BUTTONS_BACK_STEP = InlineKeyboardButton(
    text="Назад ↩️", callback_data="back_step"
)
ACCEPT = InlineKeyboardButton(text="Принять корм ✅", callback_data="accept_feed")
NOT_ACCEPT = InlineKeyboardButton(text="Отклонить ❌", callback_data="reject")


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
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Личный кабинет 🏠", callback_data="personal_account"
        )
    )
    keyboard.row(
        InlineKeyboardButton(text="Забрать корм 🛒", callback_data="get_feed")
    )
    keyboard.row(
        InlineKeyboardButton(text="Кормление 🍽️", callback_data="to_feed")
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Передать корм волонтеру 👥", callback_data="transfer_feed"
        )
    )
    return keyboard.as_markup()


def back_main_menu():
    """Вернуться в главное меню"""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(BUTTON_BACK_MAIN_MENU)
    return keyboard.as_markup()


def personal_account():
    """Личный кабинет"""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Статистика 📊", callback_data="get_statistic")
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Корм на балансе 📦", callback_data="feed_on_balance"
        )
    )
    keyboard.row(BUTTON_BACK_MAIN_MENU)
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


def accept_or_not():
    """Кнопки Принять или не Принять корм."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Принять корм ✅", callback_data="accept_feed")
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Не принять корм ❌", callback_data="not_accept_feed"
        )
    )
    return keyboard.as_markup()


def feed_form(call):
    """Кнопка для формы кормления."""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Форма для списания корма 📝",
            web_app=WebAppInfo(
                url=URL.format(
                    slug="feed_report",
                    call=call,
                )
            ),
        )
    )
    return keyboard


def transfer_form(call):
    """Кнопка формы передачи корма."""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Форма для передачи корма 📝",
            web_app=WebAppInfo(
                url=URL.format(
                    slug="check_phone_number",
                    call=call,
                    reply_markup=keyboard.as_markup(),
                ),
            ),
        )
    )
    return keyboard


def get_feed_form(call):
    """Кнопка формы получения корма."""
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Форма для передачи корма 📝",
            web_app=WebAppInfo(
                url=URL.format(
                    slug="receiving_report",
                    call=call,
                    reply_markup=keyboard.as_markup(),
                ),
            ),
        )
    )
    return keyboard
