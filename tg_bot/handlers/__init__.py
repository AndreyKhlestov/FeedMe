from tg_bot.handlers.base_com_registration import base_reg_router
from tg_bot.handlers.reports import reports_router
from tg_bot.handlers.personal_account import account_router

all_handlers = (
    base_reg_router,
    reports_router,
    account_router
)
