from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.config import site_url
from tg_bot.keyboards import inline as inline_kb
from tg_bot.db import db_commands as db


reports_router = Router()


URL = f"https://{site_url}" + "/telegram/{slug}/{call.from_user.id}/"


@reports_router.callback_query(F.data == "get_feed")
async def get_feed(call: types.CallbackQuery):
    """Получение корма."""
    await call.message.delete()
    markup = inline_kb.get_feed_form(call)
    markup.row(inline_kb.BUTTON_BACK_MAIN_MENU)

    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=(
            "Нажмите на кнопу 'Форма для передачи "
            "корма' для оформления передачи"
        ),
        reply_markup=markup.as_markup(),
    )


@reports_router.callback_query(F.data == "to_feed")
async def feeding(call: types.CallbackQuery):
    """Кормление."""
    await call.message.delete()
    markup = inline_kb.feed_form(call)
    markup.row(inline_kb.BUTTON_BACK_MAIN_MENU)
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=(
            "Нажмите на кнопку 'Форма для списания корма' "
            "для оформления списания"
        ),
        reply_markup=markup.as_markup(),
    )


@reports_router.callback_query(F.data == "transfer_feed")
async def transfer_feed(call: types.CallbackQuery):
    """Передача корма волонтеру."""
    await call.message.delete()
    markup = inline_kb.transfer_form(call)
    markup.row(inline_kb.BUTTON_BACK_MAIN_MENU)

    await call.bot.send_message(
        chat_id=call.from_user.id,
        text=(
            "Нажмите на кнопу 'Форма для передачи "
            "корма' для оформления передачи"
        ),
        reply_markup=markup.as_markup(),
    )


@reports_router.message(Command("report"))
async def command_otchet(message: types.Message):
    """Переход на страницу отчета."""
    markup = InlineKeyboardBuilder()
    url = (
        f"https://{site_url}/telegram/receiving_report/{message.from_user.id}/"
    )
    markup.add(InlineKeyboardButton(text="hello", web_app=WebAppInfo(url=url)))
    return message.answer("Привет", reply_markup=markup.as_markup())


@reports_router.callback_query(F.data.startswith("cancel_report_"))
async def cancel_report(call: types.CallbackQuery):
    """Отмена отчета о передаче корма"""
    await call.message.delete()
    id_report = call.data.split("cancel_report_")[1]
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


@reports_router.callback_query(F.data.startswith("confirm_report_"))
async def confirm_report(call: types.CallbackQuery):
    """Подтверждение отчета о передаче корма"""
    await call.message.delete()
    id_report = call.data.split("confirm_report_")[1]
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
