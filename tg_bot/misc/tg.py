from aiogram import types


async def delete_message(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except Exception:
        pass
