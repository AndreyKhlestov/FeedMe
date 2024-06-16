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


URL = f'https://{site_url}' + '/telegram/{slug}/{call.from_user.id}/'
PERSONAL_ACCOUNT = "personal_account"
STATISTIC = "get_statistic"



def ensure_plus_prefix(phone_number: str) -> str:
    """
    Проверяет, начинается ли номер телефона с + и добавляет его, если нет.
    """
    if not phone_number.startswith("+"):
        return f"+{phone_number}"
    return phone_number


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


@default_router.callback_query(F.data == "get_feed")
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


@default_router.callback_query(F.data == "to_feed")
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



# @default_router.message(Command('check'))
# async def feeding(message: types.Message):
#     """Проверка номера телефона."""
#     markup = InlineKeyboardBuilder()
#     markup.add(InlineKeyboardButton(text='check', web_app=WebAppInfo(
#         url=URL.format(
#             slug='check_phone_number',
#             message=message,))))
#     return message.answer('check', reply_markup=markup.as_markup())



@default_router.message(Command("report"))
async def command_otchet(message: types.Message):
    """Переход на страницу отчета."""
    markup = InlineKeyboardBuilder()
    url = f"https://{site_url}/telegram/receiving_report/{message.from_user.id}/"
    markup.add(InlineKeyboardButton(text="hello", web_app=WebAppInfo(url=url)))
    return message.answer("Привет", reply_markup=markup.as_markup())


@default_router.callback_query(StateUser.statistics, F.data == "back_step")
@default_router.callback_query(F.data == "personal_account")
async def personal_account(call: types.CallbackQuery):
    """Личный кабинет."""
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Личный кабинет",
        reply_markup=inline_kb.personal_account(),
    )


@default_router.callback_query(F.data == 'get_statistic')
async def get_statistic(call: types.CallbackQuery, state: FSMContext):
    """Статистика"""
    balance_feed = await db.get_user_statistic(call.from_user.id)
    feed_summary = {}
    total_amount = 0

    for feed_amount in balance_feed:
        feed = feed_amount.feed.name
        amount = feed_amount.amount
        total_amount += amount

        if feed in feed_summary:
            feed_summary[feed] += amount
        else:
            feed_summary[feed] = amount

    if not feed_summary:
        text = 'Статистика:\n\nЗа все время вы собрали: 0\n'
    else:
        text = (f'Статистика:\n\nЗа все время вы собрали: '
                f'{total_amount} кг корма\n\n')
        text += 'За этот месяц вами собрано:\n'
        for feed, amount in feed_summary.items():
            text += f'{feed} - {amount} кг\n'

    await call.message.delete()
    await state.set_state(StateUser.statistics)
    keyboard = inline_kb.builder_back_step_and_main_menu()
    await bot.send_message(
        chat_id=call.from_user.id,
        text=text,
        reply_markup=keyboard.as_markup()
    )


@default_router.callback_query(F.data.startswith('cancel_report_'))
async def cancel_report(call: types.CallbackQuery):
    """Отмена отчета о передаче корма"""
    await call.message.delete()
    id_report = call.data.split('cancel_report_')[1]
    report = await db.get_transfer_report(id_report)
    report.delete()
    await call.bot.send_message(
        chat_id=report.user.id,
        text="Указанный вами волонтер отклонил заявку. Отчет аннулирован",
    )
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text="Отчет отклонен.",
    )


@default_router.callback_query(F.data.startswith('confirm_report_'))
async def confirm_report(call: types.CallbackQuery):
    """Подтверждение отчета о передаче корма"""
    await call.message.delete()
    id_report = call.data.split('confirm_report_')[1]
    report = await db.get_transfer_report(id_report)
    report.approval = True
    await db.model_save(report)
    await call.bot.send_message(
        chat_id=report.user.id,
        text="Указанный вами волонтер принял заявку. Отчет создан.",
    )
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text="На ваш баланс добавлен новый корм.",
    )


@default_router.callback_query(F.data == 'feed_on_balance')
async def get_balance(call: types.CallbackQuery, state: FSMContext):
    """Баланс пользователя."""
    balance_feed = await db.get_user_feed_amount(call.from_user.id)
    if balance_feed.count() == 0:
        text = 'Корм на вашем балансе:\n отсутствует\n'
    else:
        text = 'Корм на вашем балансе:\n\n'
        for feed_amount in balance_feed:
            text += f'{feed_amount.feed} - {feed_amount.amount} \n'
    await call.message.delete()
    await state.set_state(StateUser.statistics)
    keyboard = inline_kb.builder_back_step_and_main_menu()
    await bot.send_message(
        chat_id=call.from_user.id,
        text=text,
        reply_markup=keyboard.as_markup()
    )
