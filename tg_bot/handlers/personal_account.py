from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

from tg_bot.loader import bot
from tg_bot.states.all_states import StateUser

from tg_bot.keyboards import inline as inline_kb
from tg_bot.db import db_commands as db


account_router = Router()


@account_router.callback_query(StateUser.statistics, F.data == "back_step")
@account_router.callback_query(F.data == "personal_account")
async def personal_account(call: types.CallbackQuery):
    """Личный кабинет."""
    await call.message.delete()
    await bot.send_message(
        chat_id=call.from_user.id,
        text="Личный кабинет",
        reply_markup=inline_kb.personal_account(),
    )


@account_router.callback_query(F.data == "get_statistic")
async def get_statistic(
    call: types.CallbackQuery, state: FSMContext
):
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
        text = "Статистика:\n\nЗа все время вы собрали: 0\n"
    else:
        text = (
            f"Статистика:\n\nЗа все время вы собрали: "
            f"{total_amount} кг корма\n\n"
        )
        text += "За этот месяц вами собрано:\n"
        for feed, amount in feed_summary.items():
            text += f"{feed} - {amount} кг\n"

    await call.message.delete()
    await state.set_state(StateUser.statistics)
    keyboard = inline_kb.builder_back_step_and_main_menu()
    await bot.send_message(
        chat_id=call.from_user.id, text=text, reply_markup=keyboard.as_markup()
    )


@account_router.callback_query(F.data == "feed_on_balance")
async def get_balance(call: types.CallbackQuery, state: FSMContext):
    """Баланс пользователя."""
    balance_feed = await db.get_user_feed_amount(call.from_user.id)
    if balance_feed.count() == 0:
        text = "Корм на вашем балансе:\n отсутствует\n"
    else:
        text = "Корм на вашем балансе:\n\n"
        for feed_amount in balance_feed:
            text += f"{feed_amount.feed} - {feed_amount.amount} \n"
    await call.message.delete()
    await state.set_state(StateUser.statistics)
    keyboard = inline_kb.builder_back_step_and_main_menu()
    await bot.send_message(
        chat_id=call.from_user.id, text=text, reply_markup=keyboard.as_markup()
    )
