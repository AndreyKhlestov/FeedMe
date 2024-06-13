from aiogram.fsm.state import StatesGroup, State

from tg_bot.keyboards.reply import send_contact


class StateUser(StatesGroup):
    main_menu = State()
    enter_phone = State()
    send_phone = State()
