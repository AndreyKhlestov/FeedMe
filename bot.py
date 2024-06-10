import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import BotCommand

from tg_bot.loader import dp, bot
from tg_bot.config import bot_logger, super_user_name, super_user_pass
from tg_bot.misc.mailing import start_milling
from tg_bot.db.db_commands import create_super_user





async def set_commands():
    commands = [BotCommand(command="/start", description="Запустить бота")]
    await bot.set_my_commands(commands=commands)


async def main():
    bot_logger.info('Запуск бота')

    await create_super_user(super_user_name, super_user_pass)

    await set_commands()

    # dp.message.outer_middleware(UserMiddleware())
    # dp.callback_query.outer_middleware(UserMiddleware())

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        start_milling,
        'interval',
        minutes=1,
        kwargs={'bot': bot}
    )
    scheduler.start()  # Запуск планировщика

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

