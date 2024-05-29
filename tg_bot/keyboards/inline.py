from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from admin_panel.telegram.models import Button
# from tg_bot.keyboards.callback_data import ReferralUrlCallback, DealDataCallback, PaginationDealsProcessing


BUTTON_BACK_MAIN_MENU = InlineKeyboardButton(text='Меню 📋', callback_data='back_main_menu')
BUTTONS_BACK_STEP = InlineKeyboardButton(text='Назад ↩️', callback_data='back_step')


def inline_keyboards(data: list or dict) -> InlineKeyboardBuilder:
    """
    Универсальная inline клавиатура.
    Получает список или словарь и возвращает inline клавиатуру из его значений.
    Если получен словарь, то текстом кнопки будет значение ключа,
    а возвращаемый результат - ключ словаря
    """
    keyboards = InlineKeyboardBuilder()
    for i_key in data:
        keyboards.add(InlineKeyboardButton(
            text=data[i_key] if isinstance(data, dict) else i_key,
            callback_data=str(i_key)
        ))
    keyboards.adjust(1)
    return keyboards


def buttons_links(buttons: list[Button]):
    """Клавиатура из кнопок со ссылками"""
    keyboard = InlineKeyboardBuilder()
    for button in buttons:
        keyboard.add(InlineKeyboardButton(text=button.name, url=button.link))
    return keyboard.as_markup()


def main_menu():
    """Главное меню"""
    buttons = {
        # 'all_referral_urls': 'Реферальные ссылки',
        'lk': 'Личный кабинет'
    }
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


# def club_info():
#     """Клавиатура для меню бизнес клуба"""
#     keyboard = InlineKeyboardBuilder()
#     keyboard.add(
#         InlineKeyboardButton(
#             text=_('Сайт'),
#             url='https://t.me/shamayev_business_law/1371'
#         )
#     )
#     keyboard.attach(builder_back_step_and_main_menu())
#     return keyboard.adjust(1).as_markup()

# def builder_button_navigation_deals():
#     """Клавиатура для навигации в сделках"""
#     keyboard = InlineKeyboardBuilder()
#     keyboard.button(text=" ⬅️ ", callback_data=PaginationDealsProcessing(after=1))
#     keyboard.button(text=" ➡️ ", callback_data=PaginationDealsProcessing(after=3))
#     return keyboard.adjust(2)

