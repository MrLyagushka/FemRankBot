from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.keyboards.keyboard_start import keyboard_start_user, keyboard_start_admin
from config import ADMIN_ID

router_start = Router()

@router_start.message(CommandStart())
async def router_start_start(message: Message):
    if message.chat.type == 'private':
        await message.answer_photo(photo="AgACAgIAAxkBAANTam0jEiPZAaUNyQKKOd9gCt6leJwAAr4aaxv_72lLbpKSR281WukBAAMCAAN5AAM9BA")
        if message.from_user.id in ADMIN_ID:
            await message.answer("Приветики, тут будет рейтинги фембой нарядиков и не только)", reply_markup=keyboard_start_admin.markup)
        else:
            await message.answer("Приветики, тут будет рейтинги фембой нарядиков и не только)", reply_markup=keyboard_start_user.markup)

