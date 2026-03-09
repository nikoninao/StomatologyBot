from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "<b>Доступные команды:</b>\n"
        "/start - Запустить бота\n"
        "/help - Показать справку"
    )
