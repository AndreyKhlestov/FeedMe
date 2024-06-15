from aiogram.fsm.state import StatesGroup, State


class StateUser(StatesGroup):
    main_menu = State()
    enter_phone = State()
    send_phone = State()
    statistics = State()
